import os
import telebot
from google import genai
from flask import Flask
from threading import Thread

# وب‌سرور برای فعال نگه داشتن سرویس در Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is active!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

Thread(target=run).start()

# تنظیمات اصلی ربات
TELEGRAM_TOKEN = "8842950899:AAH9or8k99NqZDzf2G9b1yz5eOmMJ-Zj6q0"
GEMINI_API_KEY = "AQ.Ab8RN6KotS0e7bhL5Y0l8axNJ_cVio5VG8cu-zSzC1Qvsu1dQg"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! من دستیار هوش مصنوعی تو هستم. هر سوالی داری بپرس!")

@bot.message_handler(func=lambda message: True)
def handle_ai_response(message):
    try:
        response = ai_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=message.text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"خطایی رخ داد: {e}")

print("ربات روشن شد...")
bot.infinity_polling()
