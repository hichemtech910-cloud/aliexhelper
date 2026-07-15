import asyncio
import os
import random
from datetime import datetime
from playwright.async_api import async_playwright

BROWSERLESS_TOKEN = os.getenv("BROWSERLESS_TOKEN", "")
WS_URL = f"wss://production-sfo.browserless.io?token={BROWSERLESS_TOKEN}"

TARGET_SITES = [
    "https://aliexhelper.store",
]

MIN_VISIT = 15
MAX_VISIT = 45

async def visit_site(p, url, visit_num):
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Visit #{visit_num}: {url}", flush=True)

        browser = await p.chromium.connect_over_cdp(WS_URL)
        context = await browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            locale="ar-DZ",
            timezone_id="Africa/Algiers"
        )
        page = await context.new_page()

        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(random.uniform(3, 6))

        await page.evaluate("""
            () => {
                const h = document.body.scrollHeight;
                window.scrollTo({ top: Math.random() * h * 0.5, behavior: 'smooth' });
            }
        """)

        wait_time = random.uniform(MIN_VISIT, MAX_VISIT)
        print(f"  Waiting {wait_time:.1f}s...", flush=True)
        await asyncio.sleep(wait_time)

        await page.evaluate("window.scrollTo({ top: document.body.scrollHeight * 0.8, behavior: 'smooth' })")
        await asyncio.sleep(random.uniform(2, 5))

        print(f"  Visit #{visit_num} done", flush=True)

        try:
            await context.close()
        except:
            pass
        try:
            await browser.close()
        except:
            pass

        return True
    except Exception as e:
        print(f"  Error: {e}", flush=True)
        return False

async def run():
    if not BROWSERLESS_TOKEN:
        print("ERROR: Set BROWSERLESS_TOKEN env var", flush=True)
        return

    print("=" * 50, flush=True)
    print("Browserless Autosurf - AliExHelper", flush=True)
    print("=" * 50, flush=True)
    print(f"Token: {BROWSERLESS_TOKEN[:8]}...", flush=True)
    print(f"Target: {TARGET_SITES[0]}", flush=True)
    print("Starting autosurf...\n", flush=True)

    visit_count = 0

    async with async_playwright() as p:
        while True:
            url = random.choice(TARGET_SITES)
            success = await visit_site(p, url, visit_count)
            if success:
                visit_count += 1
            pause = random.uniform(5, 12)
            print(f"  Pausing {pause:.0f}s before next visit...\n", flush=True)
            await asyncio.sleep(pause)

            if visit_count % 5 == 0:
                print(f"--- Total visits: {visit_count} ---\n", flush=True)

if __name__ == "__main__":
    asyncio.run(run())
