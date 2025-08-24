from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/gold-price')
def get_gold_price():
    url = "https://sjc.com.vn/giavang/textContent.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('tr')
    for row in rows:
        if "SJC TP HCM" in row.text:
            cols = row.find_all('td')
            buy = cols[1].text.strip()
            sell = cols[2].text.strip()
            return jsonify({
                "buy": buy,
                "sell": sell
            })

    return jsonify({"error": "Không tìm thấy giá vàng"})
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)