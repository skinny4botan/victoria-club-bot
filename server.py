import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    first_name = message.from_user.first_name or "Guest"
    text = f"Welcome, {first_name}! This is the place where you'll find all the trending games — and more🔥\n\n✅Subscribe to the channel and unlock full access to games👇"
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="SUBSCRIBE", url="https://t.me/+t0EkIlOuMnkwOGNi")
    keyboard.add(button)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

print("✅ Бот Victoria Club Bot запущен!")
bot.infinity_polling()
