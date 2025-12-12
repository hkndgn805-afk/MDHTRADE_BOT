from flask import Flask
import telebot
import os
import threading
import requests


def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)
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

# /btc komutu
@bot.message_handler(commands=['btc'])
def btc_price(message):
    try:
        price = get_btc_price()
        bot.reply_to(
            message,
            f"📈 *Bitcoin (BTC)*\n\n💰 Fiyat: *${price}*",
            parse_mode="Markdown"
        )
    except:
        bot.reply_to(message, "⚠️ Fiyat alınamadı, tekrar dene.")


# BTC kelimesi yazılırsa
@bot.message_handler(func=lambda message: message.text and message.text.lower() == "btc")
def btc_text(message):
    bot.reply_to(message, "📈 BTC yazdın. Canlı veri hazırlanıyor!")

# Selamlaşma
@bot.message_handler(func=lambda message: message.text and message.text.lower() in ["merhaba", "selam", "hello"])
def greeting(message):
    bot.reply_to(message, "👋 Merhaba! Sana piyasa verileri sunabilirim.")

# Fallback (EN SONDA!)
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
