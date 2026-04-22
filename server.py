import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import time

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

USERS_FILE = 'users.txt'

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        with open(USERS_FILE, 'a') as f:
            f.write(f"{user_id}\n")
        print(f"✅ Новый пользователь добавлен: {user_id}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    save_user(user_id)
    
    first_name = message.from_user.first_name or "Guest"
    text = (f"Welcome, {first_name}! This is the place where you'll find all the trending games — and more🔥\n\n"
            "✅Subscribe to the channel and unlock full access to games👇")
    
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="SUBSCRIBE", url="https://lkbb.cc/7425b0cb", style="success")
    keyboard.add(button)
    
    bot.send_message(user_id, text, reply_markup=keyboard)

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    ADMIN_ID = 1472818360
    
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ У тебя нет доступа к этой команде.")
        return
    
    broadcast_text = message.text.replace('/broadcast', '', 1).strip()
    
    if not broadcast_text:
        bot.reply_to(message, "❌ Напиши текст рассылки после команды.")
        return
    
    users = load_users()
    
    if not users:
        bot.reply_to(message, "📭 Нет подписанных пользователей.")
        return
    
    bot.reply_to(message, f"🚀 Начинаю рассылку для {len(users)} пользователей...")
    
    success = 0
    fail = 0
    
    for user_id in users:
        try:
            bot.send_message(user_id, broadcast_text)
            success += 1
            time.sleep(0.1)
        except Exception as e:
            fail += 1
            print(f"❌ Не отправлено {user_id}: {e}")
    
    bot.reply_to(message, f"✅ Рассылка завершена!\nОтправлено: {success}\nОшибок: {fail}")

@bot.message_handler(commands=['stats'])
def stats(message):
    ADMIN_ID = 1472818360
    
    if message.from_user.id != ADMIN_ID:
        return
    
    users = load_users()
    bot.reply_to(message, f"📊 В базе {len(users)} пользователей.")

print("✅ Бот Victoria Club Bot запущен!")
bot.infinity_polling()
