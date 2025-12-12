from flask import Flask
import telebot
import os
import threading

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "🤖 MDH Trade Bot'a hoş geldin!\n\nKomutlar:\n/start\n/btc\n/help"
    )

# /help
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(
        message,
        "📌 Kullanılabilir komutlar:\n\n/btc → BTC fiyatı\n/eth → ETH fiyatı"
    )

# Anahtar kelime: merhaba, selam
@bot.message_handler(func=lambda message: message.text.lower() in ["merhaba", "selam", "hello"])
def greeting(message):
    bot.reply_to(message, "👋 Merhaba! Sana piyasa verileri sunabilirim 📊")

# BTC yazılırsa
@bot.message_handler(func=lambda message: "btc" in message.text.lower())
def btc_text(message):
    bot.reply_to(message, "📈 BTC fiyatını istiyorsun. Yakında canlı veri gelecek!")

# Fallback – anlamazsa
@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.reply_to(
        message,
        "🤖 Bunu anlayamadım.\n\nKomutlar:\n/start\n/btc\n/help"
    )

def run_bot():
    bot.infinity_polling()

@app.route("/")
def home():
    return "Bot aktif 🚀"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
