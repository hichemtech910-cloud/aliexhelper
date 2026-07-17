import os
import json
import hashlib
import time
import uuid
import urllib.request
import urllib.parse
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler

API_SECRET = os.environ.get("API_SECRET", "dzexpress-secret-2024")
PRODUCTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.json")


def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)


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


class DZExpressHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-Secret")
        self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self.path = "/index.html"

        if self.path == "/api/products":
            products = load_products()
            self.send_json(products)
            return

        super().do_GET()

    def do_POST(self):
        if self.path == "/api/products":
            secret = self.headers.get("X-API-Secret", "")
            if secret != API_SECRET:
                self.send_json({"error": "Unauthorized"}, 401)
                return

            body = self.read_body()
            if not body:
                self.send_json({"error": "No body"}, 400)
                return

            products = load_products()
            product = body
            product["id"] = int(time.time() * 1000)
            product["addedAt"] = time.strftime("%Y-%m-%d %H:%M:%S")

            if "affiliateLink" in product:
                pid = extract_product_id(product["affiliateLink"])
                if pid:
                    product["aliId"] = pid

            products.insert(0, product)
            save_products(products)
            self.send_json({"ok": True, "product": product})
            return

        self.send_json({"error": "Not found"}, 404)

    def do_DELETE(self):
        if self.path.startswith("/api/products/"):
            secret = self.headers.get("X-API-Secret", "")
            if secret != API_SECRET:
                self.send_json({"error": "Unauthorized"}, 401)
                return

            pid = self.path.split("/")[-1]
            products = load_products()
            products = [p for p in products if str(p.get("id")) != pid]
            save_products(products)
            self.send_json({"ok": True})
            return

        self.send_json({"error": "Not found"}, 404)

    def do_PUT(self):
        if self.path.startswith("/api/products/"):
            secret = self.headers.get("X-API-Secret", "")
            if secret != API_SECRET:
                self.send_json({"error": "Unauthorized"}, 401)
                return

            pid = self.path.split("/")[-1]
            body = self.read_body()
            if not body:
                self.send_json({"error": "No body"}, 400)
                return

            products = load_products()
            for i, p in enumerate(products):
                if str(p.get("id")) == pid:
                    body["id"] = p.get("id")
                    body["addedAt"] = p.get("addedAt")
                    products[i] = body
                    save_products(products)
                    self.send_json({"ok": True, "product": body})
                    return

            self.send_json({"error": "Not found"}, 404)
            return

        self.send_json({"error": "Not found"}, 404)

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Frame-Options", "ALLOWALL")
        self.send_header("Content-Security-Policy", "frame-anceors *")
        super().end_headers()

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    if not os.path.exists(PRODUCTS_FILE):
        save_products([])
    server = HTTPServer(("0.0.0.0", port), DZExpressHandler)
    print(f"DZ Express running on port {port}")
    server.serve_forever()
