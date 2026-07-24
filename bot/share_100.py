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

# Campaign search queries - various categories from the campaign
CAMPAIGN_QUERIES = [
    'phone case', 'earbuds', 'smart watch', 'USB cable', 'power bank',
    'LED lights', 'kitchen gadget', 'car accessories', 'gaming controller',
    'wireless mouse', 'ring light', 'laptop stand', 'fitness band',
    'portable speaker', 'charger', 'headphone', 'keyboard', 'selfie stick',
    'webcam', 't-shirt', 'dress', 'shoes', 'bag', 'sunglasses', 'wallet',
    'jacket', 'hat', 'phone holder', 'screen protector', 'camera',
    'tripod', 'microphone', 'speaker', 'tablet stand', 'mouse pad',
    'water bottle', 'umbrella', 'watch band', 'ring', 'necklace',
    'bracelet', 'earring', 'makeup', 'skincare', 'hair dryer',
    'straightener', 'curling iron', 'flashlight', 'power tool',
    'drill', 'screwdriver', 'wrench', 'pliers', 'tape measure',
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
        print(f"API error: {e}")
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
    words = title.split()
    return ' '.join(words[:4])


def post_to_website(product_data):
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
        return result.get('ok', False)
    except Exception as e:
        print(f"Website error: {e}")
        return False


def share_to_telegram(product, affiliate_link):
    title = product.get('product_title', '')
    image_url = product.get('product_main_image_url', '')
    price = product.get('target_sale_price', '0')
    original_price = product.get('target_original_price', '0')
    discount = product.get('discount', '')

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

    try:
        if image_url:
            bot.send_photo(CHANNEL_ID, image_url, caption=message, parse_mode='Markdown')
        else:
            bot.send_message(CHANNEL_ID, message, parse_mode='Markdown')
        return True
    except Exception as e:
        print(f"Telegram error: {e}")
        return False


def share_100_products():
    print(f"\n{'='*60}")
    print(f"Sharing 100 products from campaign")
    print(f"Channel: {CHANNEL_ID}")
    print(f"{'='*60}\n")

    all_products = []
    shared = 0
    failed = 0

    # Get products from various queries
    queries = random.sample(CAMPAIGN_QUERIES, min(15, len(CAMPAIGN_QUERIES)))

    for query in queries:
        if len(all_products) >= 100:
            break

        print(f"Searching: {query}")
        products = search_products(query)

        for p in products:
            if len(all_products) >= 100:
                break

            product_id = str(p.get('product_id', ''))
            title = p.get('product_title', '')

            if product_id and title:
                all_products.append(p)

        time.sleep(0.5)

    print(f"\nCollected {len(all_products)} products")
    print(f"Starting to share...\n")

    for i, product in enumerate(all_products):
        if shared >= 100:
            break

        product_id = str(product.get('product_id', ''))
        title = product.get('product_title', '')
        affiliate_link = product.get('promotion_link', '')

        if not affiliate_link:
            affiliate_link = product.get('product_detail_url', f"https://www.aliexpress.com/item/{product_id}.html")

        print(f"[{shared+1}/100] {title[:50]}...")

        # Share to Telegram
        if share_to_telegram(product, affiliate_link):
            shared += 1

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
                    'image': product.get('product_main_image_url', ''),
                    'price': float(product.get('target_sale_price', 0)),
                    'originalPrice': float(product.get('target_original_price', 0)) or float(product.get('target_sale_price', 0)) * 1.5,
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
                print(f"Website error: {e}")

            time.sleep(2)
        else:
            failed += 1
            print(f"Failed to share: {title[:50]}")

    print(f"\n{'='*60}")
    print(f"Done! Shared: {shared}/100, Failed: {failed}")
    print(f"{'='*60}")

    return shared


if __name__ == "__main__":
    share_100_products()
