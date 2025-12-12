from flask import Flask
import telebot
import os
import threading

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 MDH Trade Bot çalışıyor!")

def run_bot():
    bot.infinity_polling()

@app.route("/")
def home():
    return "Bot aktif 🚀"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
@bot.message_handler(func=lambda message: True)
def all_messages(message):
    bot.reply_to(
        message,
        "🤖 MDH Trade Bot çalışıyor!\n\nKomutlar:\n/start\n/btc"
    )
