from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import threading
import time

app = Flask(__name__)

# Biến lưu dữ liệu giá vàng
cached_price = {"buy": "Đang tải...", "sell": "Đang tải..."}

# Hàm lấy dữ liệu từ trang SJC
def fetch_gold_price():
    try:
        url = "https://sjc.com.vn/giavang/textContent.php"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.select("table tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3 and "SJC" in cols[0].text:
                buy = cols[1].text.strip()
                sell = cols[2].text.strip()
                return {"buy": buy, "sell": sell}
    except Exception as e:
        print("Lỗi khi lấy dữ liệu:", e)
    return {"buy": "N/A", "sell": "N/A"}

# Luồng nền tự động cập nhật mỗi giờ
def auto_update():
    while True:
        print("Đang cập nhật giá vàng...")
        cached_price.update(fetch_gold_price())
        time.sleep(3600)  # 1 giờ

# Khởi động luồng nền khi app chạy
threading.Thread(target=auto_update, daemon=True).start()

# API trả về dữ liệu giá vàng
@app.route('/api/gold-price', methods=['GET'])
def get_gold_price():
    return jsonify(cached_price)