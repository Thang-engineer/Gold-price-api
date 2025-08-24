from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/gold-price', methods=['GET'])
def get_gold_price():
    data = {
        "buy": "78,000",
        "sell": "79,000"
    }
    return jsonify(data)