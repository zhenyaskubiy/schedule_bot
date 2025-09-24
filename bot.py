import os
import json
from dotenv import load_dotenv
import telebot
from telebot import types
from datetime import datetime

from schedules import schedule, schedule_upper, schedule_lower, bells

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)


def get_time_by_pair(pair: int) -> str:
    try:
        rec = bells[int(pair)]
        return rec.split(": ", 1)[1]
    except Exception:
        return ""

def format_lessons_with_pairs(lessons: list) -> str:
    if not any(isinstance(x, dict) and 'pair' in x for x in lessons):
        return "\n".join(map(str, lessons)) if lessons else "Пар немає 🙂"

    blocks = []
    for it in lessons:
        if not isinstance(it, dict):
            blocks.append(str(it))
            continue
        pair_num = it.get('pair', None)
        time_range = get_time_by_pair(pair_num if pair_num is not None else -1)
        title = it.get('title', '')
        teacher = it.get('teacher', '')
        groups = it.get('groups', '')
        room = it.get('room', '')

        lines = []
        if pair_num is not None and time_range:
            lines.append(f"🔢 Пара {pair_num} — 🕰️ {time_range}")
        elif pair_num is not None:
            lines.append(f"🔢 Пара {pair_num}")
        elif time_range:
            lines.append(f"🕰️ {time_range}")
        if title:
            lines.append(f"🖊️ {title}")
        if teacher:
            lines.append(f"👨‍🏫Викладач: {teacher}")
        if groups:
            lines.append(f"👥Група: {groups}")
        if room:
            lines.append(f"🏫Аудиторія: {room}")

        blocks.append("\n".join(lines))

    return "\n\n".join(blocks) if blocks else "Пар немає 🙂"

# Filter lessons according to user's elective preferences
def filter_lessons_for_user(chat_id: int, lessons: list) -> list:
    if not lessons:
        return lessons
    chosen_a = get_pref(chat_id, QUESTION_A_KEY)
    chosen_b = get_pref(chat_id, QUESTION_B_KEY)
    filtered = []
    for it in lessons:
        if not isinstance(it, dict):
            filtered.append(it)
            continue
        ekey = it.get("elective_key")
        if not ekey:
            filtered.append(it)
            continue
        # If user hasn't answered yet, show all options so they can see both
        if ekey == QUESTION_A_KEY:
            if chosen_a is None or it.get("option_idx") == chosen_a:
                filtered.append(it)
        elif ekey == QUESTION_B_KEY:
            if chosen_b is None or it.get("option_idx") == chosen_b:
                filtered.append(it)
        else:
            # Unknown elective key — include by default
            filtered.append(it)
    return filtered

# Sort lessons by pair number (dict items first, ascending by 'pair'), others after
def sort_lessons_by_pair(lessons: list) -> list:
    dicts = [x for x in lessons if isinstance(x, dict)]
    others = [x for x in lessons if not isinstance(x, dict)]
    dicts.sort(key=lambda d: d.get('pair', 999))
    return dicts + others

# ===== Week helpers =====
WEEK_LABELS = {
    "upper": "Верхній тиждень",
    "lower": "Нижній тиждень",
}

def get_week_type(date_obj: datetime) -> str:
    iso_week = date_obj.isocalendar().week
    return "upper" if iso_week % 2 == 0 else "lower"

def build_week_header(date_obj: datetime) -> str:
    wt = get_week_type(date_obj)
    label = WEEK_LABELS[wt]
    icon = "🔼" if wt == "upper" else "🔽"
    return f"{icon} {label}"

# ===== Simple per-user preferences for two fixed elective questions =====
PREFS_FILE = "user_prefs.json"

def _load_prefs():
    if os.path.exists(PREFS_FILE):
        try:
            with open(PREFS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_prefs(prefs):
    try:
        with open(PREFS_FILE, "w", encoding="utf-8") as f:
            json.dump(prefs, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def get_pref(chat_id: int, key: str):
    prefs = _load_prefs()
    return prefs.get(str(chat_id), {}).get(key)

def set_pref(chat_id: int, key: str, val: int):
    prefs = _load_prefs()
    user = prefs.setdefault(str(chat_id), {})
    user[key] = val
    _save_prefs(prefs)

QUESTION_A_KEY = "elective_a"  # 0: Автоматизація ІТ-інф., 1: ВД Front-end-прогр.
QUESTION_B_KEY = "elective_b"  # 0: Основи поб. роботехніки, 1: ФОП

def both_answered(chat_id: int) -> bool:
    return get_pref(chat_id, QUESTION_A_KEY) is not None and get_pref(chat_id, QUESTION_B_KEY) is not None

def ask_next_question(chat_id: int):
    """Ask questions one-by-one. If all answered, send a final confirmation."""
    # Ask Q1 if missing
    if get_pref(chat_id, QUESTION_A_KEY) is None:
        kb1 = types.InlineKeyboardMarkup()
        kb1.add(
            types.InlineKeyboardButton("Автоматизація ІТ-інф.", callback_data=f"pref:{QUESTION_A_KEY}:0"),
            types.InlineKeyboardButton("ВД Front-end-прогр.", callback_data=f"pref:{QUESTION_A_KEY}:1"),
        )
        bot.send_message(chat_id, "Оберіть: Автоматизація ІТ-інф. або ВД Front-end-прогр.", reply_markup=kb1)
        return
    # Ask Q2 if missing
    if get_pref(chat_id, QUESTION_B_KEY) is None:
        kb2 = types.InlineKeyboardMarkup()
        kb2.add(
            types.InlineKeyboardButton("Основи поб. роботехніки", callback_data=f"pref:{QUESTION_B_KEY}:0"),
            types.InlineKeyboardButton("ФОП", callback_data=f"pref:{QUESTION_B_KEY}:1"),
        )
        bot.send_message(chat_id, "Оберіть: Основи поб. роботехніки або ФОП", reply_markup=kb2)
        return
    # Both answered: confirm and show main menu greeting
    bot.send_message(chat_id, "Ваші вибори збережено ✅")
    bot.send_message(
        chat_id,
        "Привіт 👋 Обери день або розклад дзвінків 👇",
        reply_markup=main_menu()
    )

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
    chat_id = message.chat.id
    # If both answers already exist, show greeting immediately; else run survey and greet after completion
    if both_answered(chat_id):
        bot.send_message(
            chat_id,
            "Привіт 👋 Обери день або розклад дзвінків 👇",
            reply_markup=main_menu()
        )
    else:
        # Ask questions sequentially; greeting will be sent after completion
        ask_next_question(chat_id)

# Handle answers to the two questions
@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("pref:"))
def handle_pref_callback(call):
    try:
        _, key, idx = call.data.split(":", 2)
        set_pref(call.message.chat.id, key, int(idx))
        bot.answer_callback_query(call.id, text="Збережено ✅")
        # Immediately ask the next pending question or finish with confirmation
        ask_next_question(call.message.chat.id)
    except Exception:
        bot.answer_callback_query(call.id, text="Помилка збереження")

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text.lower()
    chat_id = message.chat.id

    if text == "сьогодні":
        today = datetime.today()
        day = today.strftime("%A").lower()
        week_type = get_week_type(today)
        week_sched = schedule_upper if week_type == "upper" else schedule_lower
        base_lessons = schedule.get(day, [])
        week_lessons = week_sched.get(day, [])
        # If base is a single placeholder like "Вихідний 🙂" and week entries exist, drop the placeholder
        if isinstance(base_lessons, list) and len(base_lessons) == 1 and isinstance(base_lessons[0], str) and week_lessons:
            base_lessons = []
        combined = list(base_lessons) + list(week_lessons)
        lessons = filter_lessons_for_user(chat_id, combined)
        lessons = sort_lessons_by_pair(lessons)
        if not lessons:
            lessons = ["Пар немає 🙂"]
        header = build_week_header(today)
        en_to_uk = {
            "monday": "Понеділок",
            "tuesday": "Вівторок",
            "wednesday": "Середа",
            "thursday": "Четвер",
            "friday": "П’ятниця",
            "saturday": "Субота",
            "sunday": "Неділя",
        }
        day_uk = en_to_uk.get(day, day.title())
        bot.send_message(chat_id, f"{header}\n📅 {day_uk}:\n" + format_lessons_with_pairs(lessons))

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
            today = datetime.today()
            week_type = get_week_type(today)
            week_sched = schedule_upper if week_type == "upper" else schedule_lower
            key = uk_to_en[text]
            base_lessons = schedule.get(key, [])
            week_lessons = week_sched.get(key, [])
            if isinstance(base_lessons, list) and len(base_lessons) == 1 and isinstance(base_lessons[0], str) and week_lessons:
                base_lessons = []
            combined = list(base_lessons) + list(week_lessons)
            lessons = filter_lessons_for_user(chat_id, combined)
            lessons = sort_lessons_by_pair(lessons)
            if not lessons:
                lessons = ["Пар немає 🙂"]
            header = build_week_header(today)
            bot.send_message(chat_id, f"{header}\n📅 {text.title()}:\n" + format_lessons_with_pairs(lessons))
        else:
            bot.send_message(chat_id, "Не розумію 🤔 Обери кнопку з меню.")

bot.polling(none_stop=True)