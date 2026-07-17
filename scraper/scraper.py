import os
import sys
import io
import json
import time
import random
import hashlib
import hmac
import traceback
import requests
from urllib.parse import quote

os.environ['PYTHONUTF8'] = '1'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

WEBSITE_URL = os.getenv('WEBSITE_URL', 'https://aliexhelper.store')
API_SECRET = os.getenv('API_SECRET', 'dzexpress-secret-2024')
ALI_APP_KEY = os.getenv('ALI_APP_KEY', '502678')
ALI_APP_SECRET = os.getenv('ALI_APP_SECRET', 'Ds7f3NQm0EpuK5VUsTVKlS3sRnOkkXoH')
SCRAPE_INTERVAL = int(os.getenv('SCRAPE_INTERVAL', '3600'))
MAX_PRODUCTS_PER_RUN = int(os.getenv('MAX_PRODUCTS_PER_RUN', '10'))
TRACKING_ID = os.getenv('TRACKING_ID', 'hixem')

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
    'phone': 'electronics', 'case': 'fashion', 'cover': 'fashion',
    'funda': 'fashion', 'earbuds': 'gadgets', 'headphone': 'gadgets',
    'watch': 'gadgets', 'band': 'gadgets', 'cable': 'electronics',
    'charger': 'electronics', 'power bank': 'electronics', 'usb': 'electronics',
    'led': 'home', 'lamp': 'home', 'kitchen': 'home', 'cooking': 'home',
    'car': 'gadgets', 'gaming': 'gadgets', 'controller': 'gadgets',
    'mouse': 'gadgets', 'keyboard': 'gadgets', 'ring light': 'gadgets',
    'stand': 'home', 'speaker': 'gadgets', 'fitness': 'gadgets',
    'portable': 'gadgets',
}


def generate_api_sign(params, secret):
    sorted_params = sorted(params.items())
    sign_str = secret + ''.join(f'{k}{v}' for k, v in sorted_params) + secret
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()


def aliexpress_api_call(method, extra_params=None):
    url = "https://api-sg.aliexpress.com/sync"
    params = {
        'method': method,
        'app_key': ALI_APP_KEY,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'format': 'json',
        'v': '2.0',
        'sign_method': 'md5',
    }
    if extra_params:
        params.update(extra_params)
    params['sign'] = generate_api_sign(params, ALI_APP_SECRET)

    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"API call error: {e}")
        return None


def search_products(query, page=1):
    params = {
        'keywords': query,
        'tracking_id': TRACKING_ID,
        'page_size': '20',
        'page_no': str(page),
        'target_language': 'AR',
        'target_currency': 'USD',
        'sort': 'SALE_PRICE_ASC',
    }

    data = aliexpress_api_call('aliexpress.affiliate.product.query', params)
    if not data:
        return []

    result = data.get('aliexpress_affiliate_product_query_response', {})
    products_result = result.get('resp_result', {})
    products_data = products_result.get('result', {})
    products = products_data.get('products', {})
    product_list = products.get('product', []) if isinstance(products, dict) else []

    print(f"API returned {len(product_list)} products for '{query}'")
    return product_list


def convert_product(raw):
    product_id = str(raw.get('product_id', ''))
    title = raw.get('product_title', '')
    if not title or not product_id:
        return None

    image_url = raw.get('product_main_image_url', '')
    if not image_url:
        image_url = raw.get('product_image', '')

    price = 0
    try:
        price = float(raw.get('target_sale_price', '0'))
    except (ValueError, TypeError):
        pass
    if price <= 0:
        try:
            price = float(raw.get('min_sale_price', '0'))
        except (ValueError, TypeError):
            pass
    if price <= 0:
        return None

    original_price = 0
    try:
        original_price = float(raw.get('target_original_price', '0'))
    except (ValueError, TypeError):
        pass
    if original_price <= 0:
        original_price = round(price * random.uniform(1.3, 2.0), 2)

    rating = 0
    try:
        rating = float(raw.get('evaluation_rate', '0'))
        if rating > 5:
            rating = rating / 20.0
    except (ValueError, TypeError):
        rating = round(random.uniform(4.0, 5.0), 1)

    reviews = 0
    try:
        reviews = int(raw.get('booked_count', '0'))
    except (ValueError, TypeError):
        reviews = random.randint(10, 500)
    if reviews <= 0:
        reviews = random.randint(10, 500)

    affiliate_link = raw.get('product_detail_url', f"https://www.aliexpress.com/item/{product_id}.html")
    tracking_url = raw.get('promotion_link', '')
    if tracking_url:
        affiliate_link = tracking_url

    short_title = title
    words = title.split()
    if len(words) > 4:
        short_title = ' '.join(words[:4])

    category = 'electronics'
    t_lower = title.lower()
    for kw, cat in CATEGORIES_MAP.items():
        if kw in t_lower:
            category = cat
            break

    return {
        'id': product_id,
        'title': title,
        'shortTitle': short_title,
        'image': image_url,
        'price': round(price, 2),
        'originalPrice': round(original_price, 2),
        'category': category,
        'rating': round(rating, 1) if rating > 0 else round(random.uniform(4.0, 5.0), 1),
        'reviews': reviews,
        'affiliateLink': affiliate_link,
        'description': title,
        'badge': 'جديد',
        'coupon': '',
    }


def check_duplicate(affiliate_link):
    try:
        resp = requests.get(f"{WEBSITE_URL}/api/products", timeout=10)
        if resp.status_code == 200:
            existing = resp.json()
            for p in existing:
                if p.get('affiliateLink') == affiliate_link:
                    return True
                if p.get('id') and str(p.get('id')) == str(affiliate_link.split('/')[-1].replace('.html', '')):
                    return True
    except Exception:
        pass
    return False


def post_product(product):
    if check_duplicate(product['affiliateLink']):
        print(f"Duplicate skipped: {product['title'][:50]}")
        return False

    try:
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
            print(f"Posted: {product['title'][:50]}")
            return True
        else:
            print(f"Post failed: {result}")
            return False
    except Exception as e:
        print(f"Post error: {e}")
        return False


def run_scraper():
    print(f"\n{'='*60}")
    print(f"AliExpress API Scraper - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    queries = random.sample(SEARCH_QUERIES, min(3, len(SEARCH_QUERIES)))
    all_products = []
    posted = 0

    for query in queries:
        print(f"\n--- Searching: {query} ---")
        raw_products = search_products(query)
        for raw in raw_products[:MAX_PRODUCTS_PER_RUN]:
            product = convert_product(raw)
            if product:
                all_products.append(product)
        time.sleep(random.uniform(1, 3))

    random.shuffle(all_products)
    print(f"\nTotal valid products: {len(all_products)}")

    for product in all_products[:MAX_PRODUCTS_PER_RUN]:
        if post_product(product):
            posted += 1
        time.sleep(random.uniform(1, 3))

    print(f"\n{'='*60}")
    print(f"Done! Posted {posted}/{min(len(all_products), MAX_PRODUCTS_PER_RUN)} products")
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
