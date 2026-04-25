import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID   = os.environ.get("CHAT_ID")

def send_telegram(message, image_url=None):
    base = f"https://api.telegram.org/bot{BOT_TOKEN}"
    if image_url:
        requests.post(f"{base}/sendPhoto", data={
            "chat_id":    CHAT_ID,
            "photo":      image_url,
            "caption":    message,
            "parse_mode": "HTML"
        })
    else:
        requests.post(f"{base}/sendMessage", data={
            "chat_id":    CHAT_ID,
            "text":       message,
            "parse_mode": "HTML"
        })

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}

    symbol    = data.get("symbol",    "N/A")
    action    = data.get("action",    "N/A").upper()
    price     = data.get("price",     "N/A")
    tf        = data.get("timeframe", "N/A")
    note      = data.get("message",   "")
    chart_url = data.get("chart_url", None)

    emoji = "🟢" if action == "BUY" else "🔴"

    msg = (
        f"{emoji} {action} — {symbol}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"💰 Giá    : {price}\n"
        f"⏱ Khung  : {tf}\n"
        f"📝 Ghi chú: {note}"
    )

    send_telegram(msg, chart_url)
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
