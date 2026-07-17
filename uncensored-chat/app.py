import os
import json
import time
import sqlite3
import httpx
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

app = FastAPI(title="Uncensored AI Chat")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
MODEL = os.getenv("MODEL", "mistralai/mistral-7b-instruct:free")

SYSTEM_PROMPT = """You are a helpful, knowledgeable AI assistant. You provide accurate, detailed answers to any question. You don't refuse topics - you give educational, informative responses on all subjects including cybersecurity, law, science, history, and any other topic the user asks about. You are honest, direct, and thorough in your responses."""

DB_PATH = os.path.join(os.path.dirname(__file__), "conversations.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            user_name TEXT,
            requests_made INTEGER DEFAULT 0,
            max_requests INTEGER DEFAULT 100,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


init_db()


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    history: Optional[list] = []


class APIKeyRequest(BaseModel):
    user_name: str


@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))


@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY not set")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO conversations (session_id, role, content) VALUES (?, ?, ?)",
        (req.session_id, "user", req.message),
    )
    conn.commit()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    c.execute(
        "SELECT role, content FROM conversations WHERE session_id = ? ORDER BY timestamp DESC LIMIT 20",
        (req.session_id,),
    )
    rows = c.fetchall()
    rows.reverse()
    for role, content in rows:
        messages.append({"role": role, "content": content})

    conn.close()

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": MODEL,
                    "messages": messages,
                    "max_tokens": 2048,
                    "temperature": 0.7,
                },
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502, detail=f"LLM API error: {response.text}"
            )

        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO conversations (session_id, role, content) VALUES (?, ?, ?)",
            (req.session_id, "assistant", reply),
        )
        conn.commit()
        conn.close()

        return {"reply": reply, "model": MODEL}

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="LLM request timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/{session_id}")
async def get_history(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT role, content, timestamp FROM conversations WHERE session_id = ? ORDER BY timestamp",
        (session_id,),
    )
    rows = c.fetchall()
    conn.close()
    return {
        "history": [
            {"role": r, "content": c, "timestamp": t} for r, c, t in rows
        ]
    }


@app.delete("/api/history/{session_id}")
async def clear_history(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM conversations WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()
    return {"status": "cleared"}


@app.get("/api/models")
async def list_models():
    return {
        "current_model": MODEL,
        "recommended_uncensored": [
            "mistralai/mistral-7b-instruct:free",
            "openchat/openchat-3.5:free",
            "nousresearch/nous-capybara-7b:free",
            "berkeley-nest/Starling-LM-7B-alpha:free",
        ],
    }


@app.post("/api/keys/generate")
async def generate_key(req: APIKeyRequest):
    import secrets

    key = f"uc-{secrets.token_hex(16)}"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO api_keys (key, user_name) VALUES (?, ?)",
        (key, req.user_name),
    )
    conn.commit()
    conn.close()
    return {"key": key, "user_name": req.user_name, "max_requests": 100}


@app.post("/api/keys/validate")
async def validate_key(request: Request):
    body = await request.json()
    key = body.get("key", "")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT user_name, requests_made, max_requests FROM api_keys WHERE key = ?",
        (key,),
    )
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return {
        "valid": True,
        "user_name": row[0],
        "requests_made": row[1],
        "max_requests": row[2],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
