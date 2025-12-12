from flask import Flask
import telebot
import os
import threading
import requests

def get_btc_price_usd():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["bitcoin"]["usd"]

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "🤖 MDH Trade Bot aktif!\n\nKomutlar:\n/btc\n/help"
    )

# Sadece "btc" yazılırsa
@bot.message_handler(func=lambda message: message.text and message.text.lower() in ["/btc", "btc"])
def btc_handler(message):
    try:
        price_usd = get_btc_price_usd()
        bot.reply_to(
            message,
            f"📈 *Bitcoin (BTC)*\n💰 Fiyat: *${price_usd}*",
            parse_mode="Markdown"
        )
    except Exception as e:
    bot.reply_to(message, f"⚠️ Fiyat alınamadı.\nHata: {str(e)}")



# Selamlaşma
@bot.message_handler(func=lambda message: message.text and message.text.lower() in ["merhaba", "selam", "naber"])
def greeting(message):
    bot.reply_to(message, "👋 Merhaba! Sana piyasa verileri sunabilirim.")

# Fallback
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
