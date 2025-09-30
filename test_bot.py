import pytest

# Приклад — замість цього імпорту треба підтягнути твою функцію з bot.py
# from bot import get_schedule

def get_schedule(day: str):
    """Тимчасова тестова функція (щоб перевірити тести)."""
    schedules = {
        "monday": "Понеділок: 2 пари",
        "tuesday": "Вівторок: 3 пари",
    }
    return schedules.get(day, "Немає розкладу")

# Тест 1. Чи повертає функція правильний розклад для понеділка
def test_schedule_monday():
    result = get_schedule("monday")
    assert "Понеділок" in result

# Тест 2. Чи є хоча б одна пара у вівторок
def test_schedule_not_empty():
    result = get_schedule("tuesday")
    assert len(result) > 0
        