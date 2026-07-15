FROM python:3.11-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps chromium

COPY autosurf.py .

ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1

# Cloud Run requires the container to listen on $PORT
# But we don't need a web server - just run the autosurf
# Cloud Run will keep the container alive as long as it's running

CMD ["python", "autosurf.py"]
