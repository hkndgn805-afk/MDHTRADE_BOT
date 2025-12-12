from flask import Flask
import telebot
import os
import threading
import requests
import time

# BTC cache
btc_cache = {"price": None, "time": 0}

def get_btc_price_cached():
    global btc_cache
    try:
        if time.time() - btc_cache["time"] > 20 or btc_cache["price"] is None:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {"ids": "bitcoin", "vs_currencies": "usd"}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            btc_cache["price"] = response.json()["bitcoin"]["usd"]
            btc_cache["time"] = time.time()
    except Exception as e:
        # Eğer API 429 veya başka hata verirse, eski fiyatı kullan
        if btc_cache["price"] is None:
            raise e
    return btc_cache["price"]

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# 1️⃣ /start handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "🤖 MDH Trade Bot aktif!\n\nKomutlar:\n/btc\n/help"
    )

# 2️⃣ Selamlaşma handler
@bot.message_handler(func=lambda message: message.text and message.text.lower().strip() in ["merhaba", "selam", "naber"])
def greeting(message):
    bot.reply_to(message, "👋 Merhaba! Sana piyasa verileri sunabilirim.")

# 3️⃣ BTC handler
@bot.message_handler(func=lambda message: message.text and message.text.lower().strip() in ["/btc", "btc"])
def btc_handler(message):
    try:
        price_usd = get_btc_price_cached()
        bot.reply_to(
            message,
            f"📈 *Bitcoin (BTC)*\n💰 Fiyat: *${price_usd}*",
            parse_mode="Markdown"
        )
    except Exception as e:
        bot.reply_to(message, f"⚠️ Fiyat alınamadı.\nHata: {str(e)}")

# 4️⃣ Fallback handler
@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.reply_to(
        message,
        "🤖 Komutu anlayamadım.\n\nKullanılabilir:\n/btc\n/help"
    )

def run_bot():
    bot.infinity_polling()

@app.route("/")
def home():
    return "Bot aktif 🚀"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
