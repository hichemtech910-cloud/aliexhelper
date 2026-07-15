import asyncio
import os
import random
import time
from datetime import datetime
from playwright.async_api import async_playwright

# Target sites
TARGET_SITES = [
    "https://aliexhelper.store",
    "https://aliexhelper.store/#products",
    "https://aliexhelper.store/#categories",
]

# Visit duration range (seconds)
MIN_VISIT = 15
MAX_VISIT = 45

async def visit_site(page, url, visit_num):
    """Visit a single site with human-like behavior"""
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Visit #{visit_num}: {url}")
        
        await page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Random scroll to simulate reading
        await page.evaluate("""
            () => {
                const height = document.body.scrollHeight;
                const scrollTo = Math.random() * height * 0.5;
                window.scrollTo({ top: scrollTo, behavior: 'smooth' });
            }
        """)
        
        # Wait random duration (human-like)
        wait_time = random.uniform(MIN_VISIT, MAX_VISIT)
        print(f"  Waiting {wait_time:.1f}s...")
        await asyncio.sleep(wait_time)
        
        # Scroll more
        await page.evaluate("window.scrollTo({ top: document.body.scrollHeight * 0.8, behavior: 'smooth' })")
        await asyncio.sleep(random.uniform(2, 5))
        
        print(f"  Visit #{visit_num} complete")
        return True
        
    except Exception as e:
        print(f"  Error: {e}")
        return False

async def run_cloud_run():
    """Main autosurf loop for Google Cloud Run"""
    print("=" * 50)
    print("Google Cloud Run Autosurf - AliExHelper")
    print("=" * 50)
    print(f"Target: {TARGET_SITES[0]}")
    print()
    
    visit_count = 0
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
            ]
        )
        
        context = await browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            locale="ar-DZ",
            timezone_id="Africa/Algiers"
        )
        
        page = await context.new_page()
        
        # Visit loop
        while True:
            url = random.choice(TARGET_SITES)
            success = await visit_site(page, url, visit_count)
            
            if success:
                visit_count += 1
            
            # Pause between visits
            pause = random.uniform(3, 8)
            await asyncio.sleep(pause)
            
            # Log progress
            if visit_count % 10 == 0:
                print(f"\n--- Total visits: {visit_count} ---\n")
            
            # Cloud Run has time limits, so we run continuously
            # The container will restart if it exceeds limits

if __name__ == "__main__":
    asyncio.run(run_cloud_run())
