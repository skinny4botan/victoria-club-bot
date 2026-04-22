import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import time

TOKEN = '8652117442:AAFzs-v3rx9rX_EQMWsgmQWFm0XBvMA9Y8Q'
bot = telebot.TeleBot(TOKEN)

# Файл для хранения ID пользователей
USERS_FILE = 'users.txt'

# ---------- ФУНКЦИИ ДЛЯ РАБОТЫ С БАЗОЙ ПОЛЬЗОВАТЕЛЕЙ ----------
def load_users():
    """Загружает список пользователей из файла"""
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]

def save_user(user_id):
    """Сохраняет нового пользователя, если его еще нет"""
    users = load_users()
    if user_id not in users:
        with open(USERS_FILE, 'a') as f:
            f.write(f"{user_id}\n")
        print(f"✅ Новый пользователь добавлен: {user_id}")

# ---------- КОМАНДА /start ----------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    save_user(user_id)  # Сохраняем пользователя
    
    first_name = message.from_user.first_name or "Guest"
    text = (f"Welcome, {first_name}! This is the place where you'll find all the trending games — and more🔥\n\n"
            "✅Subscribe to the channel and unlock full access to games👇")
    
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="SUBSCRIBE", url="https://lkbb.cc/7425b0cb", style="success")
    keyboard.add(button)
    
    bot.send_message(user_id, text, reply_markup=keyboard)

# ---------- КОМАНДА ДЛЯ РАССЫЛКИ (ТОЛЬКО ДЛЯ ТЕБЯ) ----------
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    # ТВОЙ TELEGRAM ID — ЗАМЕНИ НА СВОЙ!
    ADMIN_ID = 123456789  # 👈 ВСТАВЬ СВОЙ ID (узнай у @userinfobot)
    
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ У тебя нет доступа к этой команде.")
        return
    
    # Получаем текст рассылки (всё, что после /broadcast)
    broadcast_text = message.text.replace('/broadcast', '', 1).strip()
    
    if not broadcast_text:
        bot.reply_to(message, "❌ Напиши текст рассылки после команды.\nПример: /broadcast Привет всем!")
        return
    
    # Загружаем всех пользователей
    users = load_users()
    
    if not users:
        bot.reply_to(message, "📭 Нет подписанных пользователей.")
        return
    
    bot.reply_to(message, f"🚀 Начинаю рассылку для {len(users)} пользователей...")
    
    # Отправляем рассылку
    success = 0
    fail = 0
    
    for user_id in users:
        try:
            bot.send_message(user_id, broadcast_text)
            success += 1
            time.sleep(0.1)  # пауза, чтобы Telegram не забанил
        except Exception as e:
            fail += 1
            print(f"❌ Не отправлено {user_id}: {e}")
    
    bot.reply_to(message, f"✅ Рассылка завершена!\nОтправлено: {success}\nОшибок: {fail}")

# ---------- КОМАНДА ДЛЯ ПРОСМОТРА КОЛИЧЕСТВА ПОЛЬЗОВАТЕЛЕЙ ----------
@bot.message_handler(commands=['stats'])
def stats(message):
    ADMIN_ID = 123456789  # 👈 ТВОЙ ID
    
    if message.from_user.id != ADMIN_ID:
        return
    
    users = load_users()
    bot.reply_to(message, f"📊 В базе {len(users)} пользователей.")

# ---------- ЗАПУСК БОТА ----------
print("✅ Бот Victoria Club Bot запущен!")
bot.infinity_polling()
