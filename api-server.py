import http.server
import json
import hashlib
import time
import urllib.request
import urllib.parse
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler

# AliExpress Affiliate API credentials
# سجل في: https://portals.aliexpress.com
APP_KEY = "502678"
APP_SECRET = "79wEXy290DEyur5A7wcpsQ2H8OmwmuFz"
TRACKING_ID = "hixem"

API_URL = "https://gw.api.taobao.com/router/rest"


def generate_sign(params, secret):
    sorted_params = sorted(params.items())
    sign_str = secret + "".join(f"{k}{v}" for k, v in sorted_params) + secret
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()


def extract_product_id(url):
    patterns = [
        r'/item/(\d+)\.html',
        r'/item/(\d+)',
        r'productId=(\d+)',
        r'/(\d{10,})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_product_info(product_id):
    timestamp = str(int(time.time() * 1000))
    params = {
        "method": "aliexpress.affiliate.productdetail.get",
        "app_key": APP_KEY,
        "timestamp": timestamp,
        "format": "json",
        "v": "2.0",
        "sign_method": "md5",
        "product_ids": product_id,
        "tracking_id": TRACKING_ID
    }
    params["sign"] = generate_sign(params, APP_SECRET)

    try:
        url = f"{API_URL}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"User-Agent": "DZExpress/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            product = data.get("aliexpress_affiliate_product_info_get_response", {}).get("resp_result", {}).get("result", {}).get("product_info", {})
            if not product:
                product = data.get("aliexpress_affiliate_product_info_get_response", {}).get("resp_result", {}).get("result", {})
            return product
    except Exception as e:
        return {"error": str(e)}


class APIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/product"):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            url = query.get("url", [""])[0]

            product_id = extract_product_id(url)
            if not product_id:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid AliExpress URL"}).encode())
                return

            result = fetch_product_info(product_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode())
        else:
            super().do_GET()

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


if __name__ == "__main__":
    port = 8001
    server = HTTPServer(("localhost", port), APIHandler)
    print(f"API Server running at http://localhost:{port}")
    print(f"Make sure to update APP_KEY and APP_SECRET in this file")
    server.serve_forever()
