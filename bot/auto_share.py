import os
import sys
import io
import json
import time
import random
import hashlib
import requests
import telebot

os.environ['PYTHONUTF8'] = '1'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Config
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8639397827:AAGYU6QP4O9vJsntItmgtB0MARyHwGWoj-0')
CHANNEL_ID = os.getenv('CHANNEL_ID', '@aliexpress25c')
ALI_APP_KEY = os.getenv('ALI_APP_KEY', '502678')
ALI_APP_SECRET = os.getenv('ALI_APP_SECRET', 'Ds7f3NQm0EpuK5VUsTVKlS3sRnOkkXoH')
TRACKING_ID = os.getenv('TRACKING_ID', 'hixem')
WEBSITE_URL = os.getenv('WEBSITE_URL', 'https://aliexhelper.store')
API_SECRET = os.getenv('API_SECRET', 'dzexpress-secret-2024')
SHARE_INTERVAL = int(os.getenv('SHARE_INTERVAL', '1800'))

# Search queries
SEARCH_QUERIES = [
    'phone accessories',
    'bluetooth earbuds',
    'smart watch',
    'USB cable',
    'power bank',
    'phone case',
    'LED lights',
    'kitchen gadget',
    'car accessories',
    'gaming controller',
    'wireless mouse',
    'ring light',
    'laptop stand',
    'fitness band',
    'portable speaker',
    'charger',
    'headphone',
    'keyboard',
    'selfie stick',
    'webcam',
    't-shirt men',
    'dress women',
    'shoes',
    'bag',
    'sunglasses',
    'wallet',
    'jacket',
    'hat cap',
]

bot = telebot.TeleBot(TELEGRAM_TOKEN)


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


def generate_affiliate_link(product_url):
    """Generate product-specific affiliate link"""
    try:
        params = {
            'method': 'aliexpress.affiliate.link.generate',
            'app_key': ALI_APP_KEY,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'format': 'json',
            'v': '2.0',
            'sign_method': 'md5',
            'source': 'affiliate_link',
            'promotion_url': product_url,
            'tracking_id': TRACKING_ID,
            'promotion_link_type': '2',
            'source_values': product_url,
        }
        params['sign'] = generate_api_sign(params, ALI_APP_SECRET)

        resp = requests.get("https://api-sg.aliexpress.com/sync", params=params, timeout=30)
        data = resp.json()

        result = data.get('aliexpress_affiliate_link_generate_response', {})
        resp_result = result.get('resp_result', {})
        link_result = resp_result.get('result', {})
        promotion_links = link_result.get('promotion_links', {}).get('promotion_link', [])

        if promotion_links and len(promotion_links) > 0:
            link = promotion_links[0].get('promotion_link', '')
            if link:
                return link

        return product_url
    except Exception as e:
        print(f"Error generating link: {e}")
        return product_url


def search_products(query, page=1):
    params = {
        'keywords': query,
        'tracking_id': TRACKING_ID,
        'page_size': '10',
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


def format_price(price):
    try:
        return f"${float(price):.2f}"
    except:
        return "$0.00"


def detect_category(title):
    t = title.lower()
    # Check each keyword against the title
    categories_keywords = {
        'fashion': ['dress', 'shirt', 'pants', 'shoes', 'bag', 'wallet', 'jacket', 'hat', 'sunglasses', 'fashion', 'socks', 'belt', 'scarf', 'boots', 'sandals', 'slippers', 'jeans', 'hoodie', 'sweater', 'polo', 'suit', 'blazer', 't-shirt', 'funda', 'case', 'cover'],
        'home': ['kitchen', 'cooking', 'pot', 'pan', 'blender', 'lamp', 'chair', 'table', 'bed', 'pillow', 'curtain', 'rug', 'towel', 'storage', 'organizer', 'shelf', 'hook', 'hanger', 'mop', 'broom', 'iron', 'humidifier', 'fan', 'heater', 'bottle', 'cup', 'mug', 'plate', 'bowl'],
        'beauty': ['beauty', 'skincare', 'makeup', 'cosmetic', 'cream', 'serum', 'shampoo', 'brush', 'nail', 'lip', 'face mask', 'moisturizer', 'sunscreen', 'lotion', 'soap', 'hair dryer', 'straightener'],
        'gadgets': ['earbuds', 'headphone', 'speaker', 'earphone', 'airpod', 'gaming', 'controller', 'mouse', 'keyboard', 'gamepad', 'selfie stick', 'ring light', 'tripod', 'webcam', 'microphone'],
        'electronics': ['phone', 'watch', 'band', 'fitness', 'smartwatch', 'cable', 'charger', 'power bank', 'usb', 'adapter', 'led', 'strip lights', 'car', 'vehicle', 'auto', 'laptop', 'stand', 'camera'],
    }
    
    for category, keywords in categories_keywords.items():
        if any(kw in t for kw in keywords):
            return category
    return 'other'


def shorten_title(title):
    if 'غطاء' in title or 'Funda' in title:
        if 'آيفون' in title or 'iPhone' in title.lower():
            return 'غطاء هاتف آيفون'
        elif 'سامسونج' in title:
            return 'غطاء هاتف سامسونج'
        return 'غطاء هاتف'
    words = title.split()
    return ' '.join(words[:4])


def post_to_website(product_data):
    """Post product to website via API"""
    try:
        resp = requests.post(
            f"{WEBSITE_URL}/api/products",
            json=product_data,
            headers={
                'Content-Type': 'application/json',
                'X-API-Secret': API_SECRET
            },
            timeout=10
        )
        result = resp.json()
        if result.get('ok'):
            print(f"Posted to website: {product_data.get('title', '')[:50]}")
            return True
        else:
            print(f"Website API error: {result}")
            return False
    except Exception as e:
        print(f"Error posting to website: {e}")
        return False


def share_product():
    query = random.choice(SEARCH_QUERIES)
    products = search_products(query)

    if not products:
        print("No products found")
        return False

    product = random.choice(products)

    product_id = str(product.get('product_id', ''))
    title = product.get('product_title', '')
    image_url = product.get('product_main_image_url', '')
    price = product.get('target_sale_price', '0')
    original_price = product.get('target_original_price', '0')
    discount = product.get('discount', '')

    # Get product URL and generate affiliate link
    product_url = product.get('product_detail_url', f"https://www.aliexpress.com/item/{product_id}.html")
    affiliate_link = generate_affiliate_link(product_url)

    print(f"Affiliate link: {affiliate_link[:80]}...")

    if not product_id or not title:
        print("Invalid product data")
        return False

    # Format message
    category = detect_category(title)
    category_names = {
        'fashion': 'أزياء',
        'home': 'المنزل',
        'beauty': 'جمال',
        'gadgets': 'أجهزة',
        'electronics': 'إلكترونيات',
        'other': 'أخرى'
    }
    category_ar = category_names.get(category, category)
    price_formatted = format_price(price)
    original_formatted = format_price(original_price)

    # Build caption
    lines = [f"🔥 *{title}*"]
    lines.append("")
    lines.append(f"💰 Price: *{price_formatted}*")

    if original_price and original_price != price:
        lines.append(f"💸 Was: ~{original_formatted}~")

    if discount:
        lines.append(f"🏷️ Discount: *{discount}*")

    lines.append(f"📂 التصنيف: {category_ar}")
    lines.append("")
    lines.append(f"🛒 [Buy Now on AliExpress]({affiliate_link})")
    lines.append(f"🌐 [Visit our Store]({WEBSITE_URL})")
    lines.append("")
    lines.append("#AliExpress #Deals")

    message = "\n".join(lines)

    # Post to Telegram channel
    try:
        if image_url:
            bot.send_photo(
                CHANNEL_ID,
                image_url,
                caption=message,
                parse_mode='Markdown'
            )
        else:
            bot.send_message(
                CHANNEL_ID,
                message,
                parse_mode='Markdown'
            )
        print(f"Shared to Telegram: {title[:50]}...")
    except Exception as e:
        print(f"Error sharing to Telegram: {e}")
        return False

    # Post to website
    try:
        rating = product.get('evaluation_rate', '4.5')
        try:
            rating = min(5.0, max(1.0, float(rating)))
        except:
            rating = 4.5

        reviews = product.get('booked_count', '0')
        try:
            reviews = int(reviews)
        except:
            reviews = 0

        website_data = {
            'title': title,
            'shortTitle': shorten_title(title),
            'image': image_url,
            'price': float(price) if price else 0,
            'originalPrice': float(original_price) if original_price else float(price) * 1.5,
            'category': detect_category(title).split(' ', 1)[-1].lower() if ' ' in detect_category(title) else 'electronics',
            'rating': round(rating, 1),
            'reviews': reviews,
            'affiliateLink': affiliate_link,
            'description': title,
            'badge': 'جديد',
            'coupon': '',
        }
        post_to_website(website_data)
    except Exception as e:
        print(f"Error posting to website: {e}")

    return True


def run_auto_share():
    print(f"\n{'='*60}")
    print(f"Auto Share Bot - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Channel: {CHANNEL_ID}")
    print(f"Interval: {SHARE_INTERVAL}s ({SHARE_INTERVAL//60} min)")
    print(f"{'='*60}\n")

    shared = 0
    max_per_run = 3

    for i in range(max_per_run):
        try:
            if share_product():
                shared += 1
            time.sleep(random.uniform(5, 10))
        except Exception as e:
            print(f"Error: {e}")

    print(f"\nShared {shared}/{max_per_run} products")
    return shared


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        run_auto_share()
    else:
        print("Starting auto-share bot...")
        print("Press Ctrl+C to stop\n")

        while True:
            try:
                run_auto_share()
                print(f"\nSleeping {SHARE_INTERVAL}s ({SHARE_INTERVAL//60} min)...")
                time.sleep(SHARE_INTERVAL)
            except KeyboardInterrupt:
                print("\nStopped by user")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(60)
