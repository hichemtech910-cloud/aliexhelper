import json
import os
import telebot
import threading
import sys
import io
os.environ['PYTHONUTF8'] = '1'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from telebot import types
from aliexpress_api import AliexpressApi, models
import re
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import urllib.parse

load_dotenv()

TELEGRAM_TOKEN_BOT = os.getenv('TELEGRAM_BOT_TOKEN')
ALIEXPRESS_API_PUBLIC = os.getenv('ALIEXPRESS_API_PUBLIC')
ALIEXPRESS_API_SECRET = os.getenv('ALIEXPRESS_API_SECRET')
WEBSITE_URL = os.getenv('WEBSITE_URL', 'http://localhost:10000')
API_SECRET = os.getenv('API_SECRET', 'dzexpress-secret-2024')

if not TELEGRAM_TOKEN_BOT:
    print("Error: TELEGRAM_BOT_TOKEN not set!")
    exit(1)

if not ALIEXPRESS_API_PUBLIC or not ALIEXPRESS_API_SECRET:
    print("Error: ALIEXPRESS_API_PUBLIC/SECRET not set!")
    exit(1)

bot = telebot.TeleBot(TELEGRAM_TOKEN_BOT)

try:
    aliexpress = AliexpressApi(ALIEXPRESS_API_PUBLIC, ALIEXPRESS_API_SECRET,
                               models.Language.AR, models.Currency.EUR, 'default')
    print("AliExpress API initialized.")
except Exception as e:
    print(f"Error initializing AliExpress API: {e}")

keyboardStart = types.InlineKeyboardMarkup(row_width=1)
keyboardStart.add(
    types.InlineKeyboardButton("صفحة عرض العملات", url="https://s.click.aliexpress.com/e/_c43Op9M3"),
    types.InlineKeyboardButton("اشترك في القناة", url="https://t.me/aliexpress25c")
)

keyboard = types.InlineKeyboardMarkup(row_width=1)

# User state tracking for coupon input
user_states = {}
pending_products = {}
keyboard.add(
    types.InlineKeyboardButton("صفحة عرض العملات", url="https://s.click.aliexpress.com/e/_c43Op9M3"),
    types.InlineKeyboardButton("اشترك في القناة", url="https://t.me/aliexpress25c")
)


def get_usd_to_dzd_rate():
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()
        return data['rates']['DZD']
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None


def resolve_full_redirect_chain(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        session_req = requests.Session()
        response = session_req.get(link, allow_redirects=True, timeout=10, headers=headers)
        final_url = response.url
        print(f"Resolved URL: {link} -> {final_url}")

        if "star.aliexpress.com" in final_url:
            parsed_url = urlparse(final_url)
            params = parse_qs(parsed_url.query)
            if 'redirectUrl' in params:
                return params['redirectUrl'][0]

        return final_url
    except requests.RequestException as e:
        print(f"Error resolving redirect chain: {e}")
        return link


def extract_product_id(link):
    resolved_link = resolve_full_redirect_chain(link)

    match = re.search(r'/item/(\d+)\.html', resolved_link)
    if match:
        return match.group(1)

    match = re.search(r'productIds=(\d+)', resolved_link)
    if match:
        return match.group(1)

    match = re.search(r'(\d{13,})', resolved_link)
    if match:
        return match.group(1)

    return None


def generate_affiliate_link(product_id):
    try:
        clean_url = f'https://www.aliexpress.com/item/{product_id}.html'
        result = aliexpress.get_affiliate_links(clean_url)
        link = result[0].promotion_link
        # If the returned link is s.click, use direct link with aff_id instead
        if 's.click.aliexpress.com' in link and 'aff_id=' not in link:
            return f'https://www.aliexpress.com/item/{product_id}.html?aff_id=hixem'
        return link
    except Exception as e:
        print(f"Error generating affiliate link: {e}")
        return f"https://www.aliexpress.com/item/{product_id}.html?aff_id=hixem"


def is_duplicate(product_data):
    try:
        resp = requests.get(f"{WEBSITE_URL}/api/products", timeout=5)
        products = resp.json()
        for p in products:
            if p.get('affiliateLink') == product_data.get('affiliateLink'):
                return p.get('id')
            if p.get('title') == product_data.get('title') and product_data.get('title') != 'منتج جديد':
                return p.get('id')
        return None
    except Exception:
        return None


def post_to_website(product_data):
    existing_id = is_duplicate(product_data)
    try:
        if existing_id:
            resp = requests.put(
                f"{WEBSITE_URL}/api/products/{existing_id}",
                json=product_data,
                headers={
                    'Content-Type': 'application/json',
                    'X-API-Secret': API_SECRET
                },
                timeout=10
            )
        else:
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
        print(f"Website API response: {result}")
        return result
    except Exception as e:
        print(f"Error posting to website: {e}")
        return None


def shorten_title(title):
    if 'غطاء' in title or 'Funda' in title:
        if 'آيفون' in title or 'iPhone' in title.lower():
            return 'غطاء هاتف آيفون'
        elif 'سامسونج' in title:
            return 'غطاء هاتف سامسونج'
        return 'غطاء هاتف'
    if 'نوبيا' in title or 'Z70' in title:
        return 'هاتف نوبيا Z70S'
    if 'Xbox' in title or 'xbox' in title.lower():
        return 'وحدة تحكم Xbox RGB'
    if 'طقم رياضي' in title:
        return 'طقم رياضي رجالي'
    if 'رز' in title or 'طبخ' in title:
        return 'وعاء طبخ أرز'
    if 'سماع' in title:
        return 'سماعات بلوتوث لاسلكية'
    words = title.split()
    return ' '.join(words[:3])


def detect_category(title):
    t = title.lower()
    if any(kw in t for kw in ['funda', 'case', 'cover', 'غطاء', 'حقيبة', 'ساعة', 'نظارات', 'عطر', 'perfume', 'dress', 'shirt', 'pants', 'shoes', 'sneakers', 'bag', 'handbag', 'wallet', 'jacket', 'coat', 'fashion', 'socks', 'hat', 'cap', 'scarf', 'belt', 'sunglasses', 'fragrance', 'parfum', 'jeans', 'hoodie', 'sweater', 'polo', 'suit', 'blazer', 'boots', 'sandals', 'slippers', 'giorgio', 'armani', 'طقم رياضي', 'قميص', 'بنطلون', 'حذاء', 'فستان', 'تيشيرت', 'جاكيت', 'ملابس', 'أزياء', 'رجالي', 'نسائي', 'سترة']):
        return 'fashion'
    if any(kw in t for kw in ['kitchen', 'cooking', 'rice cooker', 'pot', 'pan', 'blender', 'mixer', 'vacuum', 'lamp', 'chair', 'table', 'bed', 'pillow', 'curtain', 'rug', 'towel', 'storage', 'organizer', 'shelf', 'hook', 'hanger', 'mop', 'broom', 'iron', 'steamer', 'humidifier', 'fan', 'heater', 'air purifier', 'bottle', 'cup', 'mug', 'plate', 'bowl', 'spoon', 'fork', 'knife', 'cutting board', 'طبخ', 'رز', 'مطبخ', 'قلاية', 'وعاء طبخ', 'طباخ', 'غير لاصق', 'بخار']):
        return 'home'
    if any(kw in t for kw in ['beauty', 'skincare', 'makeup', 'cosmetic', 'cream', 'serum', 'shampoo', 'conditioner', 'brush', 'nail', 'lip', 'face mask', 'moisturizer', 'sunscreen', 'lotion', 'soap', 'scrub']):
        return 'beauty'
    if any(kw in t for kw in ['mouse', 'keyboard', 'usb', 'cable', 'charger', 'power bank', 'speaker', 'headphone', 'earphone', 'earbuds', 'adapter', 'hub', 'drive', 'ssd', 'flash', 'webcam', 'microphone', 'ring light', 'tripod', 'selfie', 'controller', 'gamepad', 'gaming', 'console', 'xbox', 'playstation', 'nintendo', 'switch', 'وحدة تحكم', 'rgb', 'سماع', 'شاحن']):
        return 'gadgets'
    return 'electronics'


@bot.message_handler(commands=['start'])
def welcome_user(message):
    bot.send_message(
        message.chat.id,
        "يرجى إرسال رابط منتج علي إكسبرس، وسأتولى مهمة البحث عن أفضل الأسعار 😁",
        reply_markup=keyboardStart)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        chat_id = message.chat.id

        # Check if waiting for coupon
        if chat_id in user_states and user_states[chat_id] == 'waiting_coupon':
            raw_coupon = message.text.strip()
            if raw_coupon == '0' or not raw_coupon or raw_coupon.startswith('http') or 'aliexpress' in raw_coupon.lower():
                coupon = ''
            else:
                coupon = raw_coupon
            product_data = pending_products.pop(chat_id, None)
            user_states.pop(chat_id, None)

            if product_data:
                result = post_to_website({
                    **product_data,
                    'badge': 'جديد',
                    'coupon': coupon,
                    'reviews': 0
                })
                if result:
                    bot.send_message(chat_id, f"✅ تم نشر المنتج بنجاح")
                else:
                    bot.send_message(chat_id, "❌ حدث خطأ أثناء النشر")
            else:
                bot.send_message(chat_id, "حدث خطأ، أرسل الرابط مرة أخرى")
            return

        print(f"Message received: {message.text}")
        link = extract_link(message.text)
        sent_message = bot.send_message(chat_id, 'إنتظر قليلا 😁 ... أنا أبحث عن أفضل العروض 🔎')
        message_id = sent_message.message_id
        if link and "aliexpress.com" in link and not ("p/shoppingcart" in message.text.lower()):
            if "availableproductshopcartids" in message.text.lower():
                get_affiliate_shopcart_link(link, message)
                return
            get_affiliate_links(message, message_id, link)
        else:
            bot.delete_message(chat_id, message_id)
            bot.send_message(chat_id,
                           "الرابط غير صحيح ❌️ تأكد من رابط المنتج.\n"
                           "قم بإرسال الرابط فقط بدون عنوان المنتج",
                           parse_mode='HTML')
    except Exception as e:
        print(f"Error in echo_all handler: {e}")


def extract_link(text):
    links = re.findall(r'https?://\S+|www\.\S+', text)
    return links[0] if links else None


def get_affiliate_links(message, message_id, link):
    try:
        resolved_link = resolve_full_redirect_chain(link)
        product_id = extract_product_id(resolved_link)

        if not product_id:
            bot.delete_message(message.chat.id, message_id)
            bot.send_message(message.chat.id, "لم أتمكن من استخراج معرف المنتج.")
            return

        affiliate_link = generate_affiliate_link(product_id)

        if not affiliate_link:
            bot.delete_message(message.chat.id, message_id)
            bot.send_message(message.chat.id, "لم أتمكن من إنشاء رابط الإحالة.")
            return

        try:
            product_details = aliexpress.get_products_details(
                [product_id],
                fields=["target_sale_price", "target_original_price", "product_title",
                        "product_main_image_url", "coupon_promotion_code",
                        "evaluate_rate", "first_level_category_name"]
            )

            if product_details and len(product_details) > 0:
                product = product_details[0]
                price_usd = float(product.target_sale_price)
                original_price = float(product.target_original_price) if hasattr(product, 'target_original_price') and product.target_original_price else price_usd * 1.5
                title = product.product_title
                image_url = product.product_main_image_url
                coupon_code = getattr(product, 'coupon_promotion_code', '') or ''

                exchange_rate = get_usd_to_dzd_rate()
                price_dzd = price_usd * exchange_rate if exchange_rate else price_usd

                bot.delete_message(message.chat.id, message_id)

                message_text = (
                    f" {title} \n"
                    f" {price_usd:.2f}$ / {price_dzd:.2f} دج\n"
                )

                if coupon_code:
                    message_text += f" كوبون: {coupon_code}\n"

                message_text += f"\nرابط الشراء: {affiliate_link}"

                bot.send_photo(message.chat.id, image_url, caption=message_text, reply_markup=keyboard)

                rating = getattr(product, 'evaluate_rate', None)
                if rating is None:
                    rating = 4.5
                else:
                    try:
                        rating = min(5.0, max(1.0, float(rating)))
                    except (ValueError, TypeError):
                        rating = 4.5

                pending_products[message.chat.id] = {
                    'title': title,
                    'shortTitle': shorten_title(title),
                    'image': image_url,
                    'price': price_usd,
                    'originalPrice': original_price,
                    'category': detect_category(title),
                    'rating': round(rating, 1),
                    'affiliateLink': affiliate_link,
                    'description': title
                }
                user_states[message.chat.id] = 'waiting_coupon'

                bot.send_message(message.chat.id,
                    "أرسل لي الكوبون (إن وُجد) أو اكتب 0 إذا لا يوجد كوبون")
            else:
                bot.delete_message(message.chat.id, message_id)
                bot.send_message(message.chat.id, f"رابط الشراء: {affiliate_link}", reply_markup=keyboard)

                pending_products[message.chat.id] = {
                    'title': 'منتج جديد',
                    'shortTitle': 'منتج جديد',
                    'image': '',
                    'price': 0,
                    'originalPrice': 0,
                    'category': 'electronics',
                    'rating': 4.5,
                    'affiliateLink': affiliate_link,
                    'description': 'منتج من علي إكسبرس'
                }
                user_states[message.chat.id] = 'waiting_coupon'
                bot.send_message(message.chat.id,
                    "أرسل لي الكوبون (إن وُجد) أو اكتب 0 إذا لا يوجد كوبون")

        except Exception as e:
            print(f"Error fetching product details: {e}")
            bot.delete_message(message.chat.id, message_id)
            bot.send_message(message.chat.id, f"رابط الشراء: {affiliate_link}", reply_markup=keyboard)

            pending_products[message.chat.id] = {
                'title': 'منتج جديد',
                'shortTitle': 'منتج جديد',
                'image': '',
                'price': 0,
                'originalPrice': 0,
                'category': 'electronics',
                'rating': 4.5,
                'affiliateLink': affiliate_link,
                'description': 'منتج من علي إكسبرس'
            }
            user_states[message.chat.id] = 'waiting_coupon'
            bot.send_message(message.chat.id,
                "أرسل لي الكوبون (إن وُجد) أو اكتب 0 إذا لا يوجد كوبون")

    except Exception as e:
        print(f"Error in get_affiliate_links: {e}", flush=True)
        import traceback; traceback.print_exc()
        bot.send_message(message.chat.id, f"حدث خطأ: {str(e)[:100]}")


def get_affiliate_shopcart_link(link, message):
    try:
        parsed_url = urlparse(link)
        params = parse_qs(parsed_url.query)
        shop_cart_link = "https://www.aliexpress.com/p/trade/confirm.html?"
        shop_cart_params = {
            "availableProductShopcartIds": ",".join(params.get("availableProductShopcartIds", [])),
            "extraParams": json.dumps({"channelInfo": {"sourceType": "620"}}, separators=(',', ':'))
        }
        full_link = shop_cart_link + urllib.parse.urlencode(shop_cart_params)
        affiliate_link = aliexpress.get_affiliate_links(full_link)[0].promotion_link
        bot.send_photo(message.chat.id,
                       "https://i.postimg.cc/1Xrk1RJP/Copy-of-Basket-aliexpress-telegram.png",
                       caption=f"رابط تخفيض السلة\n{affiliate_link}")
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "حدث خطأ")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    try:
        if call.data == 'click':
            link = 'https://www.aliexpress.com/p/shoppingcart/index.html?'
            get_affiliate_shopcart_link(link, call.message)
        else:
            keyboard_games = types.InlineKeyboardMarkup(row_width=1)
            keyboard_games.add(
                types.InlineKeyboardButton("لعبة Merge boss", url="https://s.click.aliexpress.com/e/_DlCyg5Z"),
                types.InlineKeyboardButton("لعبة Fantastic Farm", url="https://s.click.aliexpress.com/e/_DBBkt9V"),
                types.InlineKeyboardButton("لعبة قلب الاوراق Flip", url="https://s.click.aliexpress.com/e/_DdcXZ2r"),
                types.InlineKeyboardButton("لعبة GoGo Match", url="https://s.click.aliexpress.com/e/_DDs7W5D")
            )
            bot.send_photo(call.message.chat.id,
                           "https://i.postimg.cc/VvmhgQ1h/Basket-aliexpress-telegram.png",
                           caption="روابط ألعاب جمع العملات",
                           reply_markup=keyboard_games)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    webhook_url = os.getenv('WEBHOOK_URL')

    if webhook_url:
        from flask import Flask, request
        app = Flask(__name__)

        @app.route('/webhook', methods=['POST'])
        def webhook():
            json_str = request.get_data().decode('UTF-8')
            update = telebot.types.Update.de_json(json_str)
            bot.process_new_updates([update])
            return 'OK', 200

        def run_flask():
            app.run(host='0.0.0.0', port=5000)

        threading.Thread(target=run_flask).start()
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)
        print(f"Webhook set to: {webhook_url}")
    else:
        import requests as _req
        _req.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN_BOT}/deleteWebhook?drop_pending_updates=true")
        print("Bot running in polling mode...")
        bot.infinity_polling(none_stop=True, timeout=10, long_polling_timeout=5)
