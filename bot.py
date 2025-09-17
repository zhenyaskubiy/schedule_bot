import os
from dotenv import load_dotenv
import telebot
from telebot import types
from datetime import datetime

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

schedule = {
    "monday": [],
    "tuesday": [],
    "wednesday": [],
    "thursday": [],
    "friday": [],
    "saturday": ["Вихідний 🙂"],
    "sunday": ["Вихідний 🙂"],
}

bells = [
    
]

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [
        "Сьогодні", "Понеділок", "Вівторок", "Середа",
        "Четвер", "П’ятниця", "Субота", "Неділя", "Дзвінки"
    ]
    markup.add(*[types.KeyboardButton(b) for b in buttons])
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привіт 👋 Обери день або розклад дзвінків 👇",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text.lower()
    chat_id = message.chat.id

    if text == "сьогодні":
        day = datetime.today().strftime("%A").lower()
        lessons = schedule.get(day, ["Пар немає 🙂"])
        bot.send_message(chat_id, "📅 Сьогодні:\n" + "\n".join(lessons))

    elif text == "дзвінки":
        bot.send_message(chat_id, "⏰ Розклад дзвінків:\n" + "\n".join(bells))

    else:
        uk_to_en = {
            "понеділок": "monday",
            "вівторок": "tuesday",
            "середа": "wednesday",
            "четвер": "thursday",
            "п’ятниця": "friday",
            "субота": "saturday",
            "неділя": "sunday"
        }
        if text in uk_to_en:
            lessons = schedule.get(uk_to_en[text], ["Пар немає 🙂"])
            bot.send_message(chat_id, f"📅 {text.title()}:\n" + "\n".join(lessons))
        else:
            bot.send_message(chat_id, "Не розумію 🤔 Обери кнопку з меню.")

# 🔄 запуск
bot.polling(none_stop=True)