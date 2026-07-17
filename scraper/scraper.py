import os
import sys
import io
import json
import time
import random
import hashlib
import re
import traceback
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import quote, urljoin

os.environ['PYTHONUTF8'] = '1'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

WEBSITE_URL = os.getenv('WEBSITE_URL', 'https://aliexhelper.store')
API_SECRET = os.getenv('API_SECRET', 'dzexpress-secret-2024')
ALIEXPRESS_API_PUBLIC = os.getenv('ALIEXPRESS_API_PUBLIC', '')
ALIEXPRESS_API_SECRET = os.getenv('ALIEXPRESS_API_SECRET', '')
SCRAPE_INTERVAL = int(os.getenv('SCRAPE_INTERVAL', '3600'))
MAX_PRODUCTS_PER_RUN = int(os.getenv('MAX_PRODUCTS_PER_RUN', '10'))

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
]

SEARCH_QUERIES = [
    'phone accessories',
    'bluetooth earbuds',
    'smart watch',
    'USB cable',
    'power bank',
    'phone case',
    'LED strip lights',
    'kitchen gadget',
    'car accessories',
    'gaming controller',
    'wireless mouse',
    'ring light',
    'laptop stand',
    'fitness band',
    'portable speaker',
]

CATEGORIES_MAP = {
    'phone': 'electronics',
    'case': 'fashion',
    'cover': 'fashion',
    'funda': 'fashion',
    'earbuds': 'gadgets',
    'headphone': 'gadgets',
    'watch': 'gadgets',
    'band': 'gadgets',
    'cable': 'electronics',
    'charger': 'electronics',
    'power bank': 'electronics',
    'usb': 'electronics',
    'led': 'home',
    'lamp': 'home',
    'kitchen': 'home',
    'cooking': 'home',
    'car': 'gadgets',
    'gaming': 'gadgets',
    'controller': 'gadgets',
    'mouse': 'gadgets',
    'keyboard': 'gadgets',
    'ring light': 'gadgets',
    'stand': 'home',
    'speaker': 'gadgets',
    'fitness': 'gadgets',
    'portable': 'gadgets',
}

try:
    from aliexpress_api import AliexpressApi, models as ali_models
    aliexpress = AliexpressApi(ALIEXPRESS_API_PUBLIC, ALIEXPRESS_API_SECRET,
                               ali_models.Language.AR, ali_models.Currency.EUR, 'default')
    HAS_API = True
    print("AliExpress API initialized.")
except Exception as e:
    HAS_API = False
    print(f"AliExpress API not available: {e}")


def get_session():
    s = requests.Session()
    s.headers.update({
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    })
    return s


def detect_category(title):
    t = title.lower()
    for kw, cat in CATEGORIES_MAP.items():
        if kw in t:
            return cat
    return 'electronics'


def shorten_title(title):
    title = re.sub(r'<[^>]+>', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    words = title.split()
    if len(words) > 4:
        return ' '.join(words[:4])
    return title


def generate_affiliate_link(product_url):
    if not HAS_API:
        return product_url
    try:
        result = aliexpress.get_affiliate_links(product_url)
        if result and len(result) > 0:
            return result[0].promotion_link
    except Exception as e:
        print(f"Affiliate link error: {e}")
    return product_url


def scrape_search_page(session, query, page=1):
    products = []
    url = f"https://www.aliexpress.com/wholesale?SearchText={quote(query)}&page={page}"
    print(f"Scraping: {url}")

    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'lxml')

        cards = soup.select('a[href*="/item/"]')
        seen_ids = set()

        for card in cards:
            try:
                href = card.get('href', '')
                match = re.search(r'/item/(\d+)\.html', href)
                if not match:
                    continue
                product_id = match.group(1)
                if product_id in seen_ids:
                    continue
                seen_ids.add(product_id)

                title_el = card.select_one('h3') or card.select_one('[class*="title"]') or card
                title = title_el.get_text(strip=True)
                if not title or len(title) < 5:
                    continue

                img_el = card.select_one('img')
                image_url = ''
                if img_el:
                    image_url = img_el.get('src', '') or img_el.get('data-src', '')
                    if image_url and not image_url.startswith('http'):
                        image_url = 'https:' + image_url

                price_text = card.get_text()
                price_match = re.search(r'\$(\d+\.?\d*)', price_text)
                price = float(price_match.group(1)) if price_match else 0
                if price <= 0:
                    continue

                original_price = price * random.uniform(1.3, 2.0)

                products.append({
                    'id': product_id,
                    'title': title,
                    'shortTitle': shorten_title(title),
                    'image': image_url,
                    'price': round(price, 2),
                    'originalPrice': round(original_price, 2),
                    'category': detect_category(title),
                    'rating': round(random.uniform(4.0, 5.0), 1),
                    'reviews': random.randint(10, 500),
                    'affiliateLink': f"https://www.aliexpress.com/item/{product_id}.html",
                    'description': title,
                    'badge': 'جديد',
                    'coupon': '',
                })

                if len(products) >= MAX_PRODUCTS_PER_RUN:
                    break

            except Exception:
                continue

    except Exception as e:
        print(f"Search scrape error: {e}")

    return products


def scrape_category_page(session, category_url):
    products = []
    print(f"Scraping category: {category_url}")

    try:
        resp = session.get(category_url, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'lxml')

        cards = soup.select('a[href*="/item/"]')
        seen_ids = set()

        for card in cards:
            try:
                href = card.get('href', '')
                match = re.search(r'/item/(\d+)\.html', href)
                if not match:
                    continue
                product_id = match.group(1)
                if product_id in seen_ids:
                    continue
                seen_ids.add(product_id)

                title_el = card.select_one('h3') or card.select_one('[class*="title"]') or card
                title = title_el.get_text(strip=True)
                if not title or len(title) < 5:
                    continue

                img_el = card.select_one('img')
                image_url = ''
                if img_el:
                    image_url = img_el.get('src', '') or img_el.get('data-src', '')
                    if image_url and not image_url.startswith('http'):
                        image_url = 'https:' + image_url

                price_text = card.get_text()
                price_match = re.search(r'\$(\d+\.?\d*)', price_text)
                price = float(price_match.group(1)) if price_match else 0
                if price <= 0:
                    continue

                original_price = price * random.uniform(1.3, 2.0)

                products.append({
                    'id': product_id,
                    'title': title,
                    'shortTitle': shorten_title(title),
                    'image': image_url,
                    'price': round(price, 2),
                    'originalPrice': round(original_price, 2),
                    'category': detect_category(title),
                    'rating': round(random.uniform(4.0, 5.0), 1),
                    'reviews': random.randint(10, 500),
                    'affiliateLink': f"https://www.aliexpress.com/item/{product_id}.html",
                    'description': title,
                    'badge': 'جديد',
                    'coupon': '',
                })

                if len(products) >= MAX_PRODUCTS_PER_RUN:
                    break

            except Exception:
                continue

    except Exception as e:
        print(f"Category scrape error: {e}")

    return products


def post_product(product):
    try:
        existing = check_duplicate(product['affiliateLink'])
        if existing:
            print(f"Duplicate skipped: {product['title'][:50]}")
            return False

        resp = requests.post(
            f"{WEBSITE_URL}/api/products",
            json=product,
            headers={
                'Content-Type': 'application/json',
                'X-API-Secret': API_SECRET,
            },
            timeout=15,
        )
        result = resp.json()
        if result.get('ok'):
            print(f"✅ Posted: {product['title'][:50]}")
            return True
        else:
            print(f"❌ Post failed: {result}")
            return False
    except Exception as e:
        print(f"Post error: {e}")
        return False


def check_duplicate(affiliate_link):
    try:
        resp = requests.get(f"{WEBSITE_URL}/api/products", timeout=10)
        products = resp.json()
        for p in products:
            if p.get('affiliateLink') == affiliate_link:
                return True
            if p.get('title') == affiliate_link:
                return True
    except Exception:
        pass
    return False


def run_scraper():
    print(f"\n{'='*60}")
    print(f"AliExpress Scraper - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    session = get_session()
    all_products = []
    posted = 0

    queries_to_use = random.sample(SEARCH_QUERIES, min(3, len(SEARCH_QUERIES)))

    for query in queries_to_use:
        print(f"\n--- Searching: {query} ---")
        products = scrape_search_page(session, query, page=1)
        all_products.extend(products)
        time.sleep(random.uniform(2, 5))

    random.shuffle(all_products)

    print(f"\nTotal products found: {len(all_products)}")

    for product in all_products[:MAX_PRODUCTS_PER_RUN]:
        affiliate_link = generate_affiliate_link(product['affiliateLink'])
        product['affiliateLink'] = affiliate_link

        if post_product(product):
            posted += 1
        time.sleep(random.uniform(1, 3))

    print(f"\n{'='*60}")
    print(f"Done! Posted {posted}/{len(all_products[:MAX_PRODUCTS_PER_RUN])} products")
    print(f"{'='*60}")

    return posted


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        run_scraper()
    else:
        print(f"Scraper running. Interval: {SCRAPE_INTERVAL}s ({SCRAPE_INTERVAL//3600}h)")
        while True:
            try:
                run_scraper()
            except Exception as e:
                print(f"Scraper error: {e}")
                traceback.print_exc()
            print(f"\nSleeping {SCRAPE_INTERVAL}s...")
            time.sleep(SCRAPE_INTERVAL)
