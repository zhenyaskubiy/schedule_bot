# -*- coding: utf-8 -*-
# Centralized schedule and bells data

schedule = {
    "monday": [
        {
            "pair": 5,
            "title": "Автоматизація ІТ-інф.",
            "teacher": "Марченко Станіслав Віталійович",
            "groups": "2П-22",
            "room": "212",
            "elective_key": "elective_a",
            "option_idx": 0,
        },
        {
            "pair": 6,
            "title": "Автоматизація ІТ-інф.",
            "teacher": "Марченко Станіслав Віталійович",
            "groups": "2П-22",
            "room": "212",
            "elective_key": "elective_a",
            "option_idx": 0,
        },
        {
            "pair": 6,
            "title": "ВД Front-end-прогр.",
            "teacher": "Дмитрюк Валентин Віталійович",
            "groups": "2П-22",
            "room": "Everlabs",
            "elective_key": "elective_a",
            "option_idx": 1,
        },
        {       
            "pair": 7,
            "title": "ВД Front-end-прогр.",
            "teacher": "Дмитрюк Валентин Віталійович",
            "groups": "2П-22",
            "room": "Everlabs",
            "elective_key": "elective_a",
            "option_idx": 1,
        },
    ],
    "tuesday": [
        {
            "pair": 5,
            "title": "Основи поб. роботехніки",
            "teacher": "Орел Андрій Сергійович",
            "groups": "2П-22",
            "room": "105",
            "elective_key": "elective_b",
            "option_idx": 0,
        },
        {
            "pair": 7,
            "title": "ФОП",
            "teacher": "Шільвінська Ольга Леонардівна",
            "groups": "2П-22",
            "room": "201",
            "elective_key": "elective_b",
            "option_idx": 1,
        },
    ],
    "wednesday": [
        {
            "pair": 2,
            "title": "Теорія ймовірності",
            "teacher": "Ходаковська Олена Олександрівна",
            "groups": "2П-22",
            "room": "116",
        },
        {
            "pair": 3,
            "title": "Операційні системи",
            "teacher": "Медолиз Маргарита Миколаївна",
            "groups": "2П-22",
            "room": "116",
        },
        {
            "pair": 4,
            "title": "Командна розробка програмних проєктів",
            "teacher": "Захарова Марія В'ячеславівна",
            "groups": "2П-22",
            "room": "105",
        },
        {
            "pair": 5,
            "title": "Командна розробка програмних проєктів",
            "teacher": "Захарова Марія В'ячеславівна",
            "groups": "2П-22",
            "room": "210",
        },
    ],
    "thursday": [
        {
            "pair": 7,
            "title": "Алгоритми, методи обчислень та структури даних",
            "teacher": "Марченко Станіслав Віталійович",
            "groups": "2П-22",
            "room": "212",
        },
    ],
    "friday": [
        {
            "pair": 6,
            "title": "Комп'ютерні мережі",
            "teacher": "Медолиз Маргарита Миколаївна",
            "groups": "2П-22",
            "room": "210",
        },
        {
            "pair": 7,
            "title": "Операційні системи",
            "teacher": "Медолиз Маргарита Миколаївна",
            "groups": "2П-22",
            "room": "210",
        },
    ],
    "saturday": ["Вихідний 🙂"],
    "sunday": ["Вихідний 🙂"],
}

schedule_upper = {
    "monday": [],
    "tuesday": [
        {
            "pair": 6,
            "title": "Основи поб. роботехніки",
            "teacher": "Орел Андрій Сергійович",
            "groups": "2П-22",
            "room": "210",
            "elective_key": "elective_b",
            "option_idx": 0,
        },
    ],
    "wednesday": [],
    "thursday": [
        {
            "pair": 5,
            "title": "Алгоритми, методи обчислень та структури даних",
            "teacher": "Марченко Станіслав Віталійович",
            "groups": "2П-22",
            "room": "302",
        },
        {
            "pair": 6,
            "title": "Комп'ютерні мережі",
            "teacher": "Медолиз Маргарита Миколаївна",
            "groups": "2П-22",
            "room": "200",
        },
    ],
    "friday": [],
    "saturday": ["Вихідний 🙂"],
    "sunday": ["Вихідний 🙂"],
}

schedule_lower = {
    "monday": [],
    "tuesday": [
        {
            "pair": 6,
            "title": "ФОП",
            "teacher": "Шільвінська Ольга Леонардівна",
            "groups": "2П-22",
            "room": "201",
            "elective_key": "elective_b",
            "option_idx": 1,
        },
    ],
    "wednesday": [],
    "thursday": [
        {
            "pair": 4,
            "title": "Алгоритми, методи обчислень та структури даних",
            "teacher": "Марченко Станіслав Віталійович",
            "groups": "2П-22",
            "room": "302",
        },
        {
            "pair": 5,
            "title": "Теорія ймовірностей",
            "teacher": "Ходаковська Олена Олександрівна",
            "groups": "2П-22",
            "room": "308",
        },
        {
            "pair": 6,
            "title": "Комп'ютерні мережі",
            "teacher": "Медолиз Маргарита Миколаївна",
            "groups": "2П-22",
            "room": "308",
        },
    ],
    "friday": [],
    "saturday": ["Вихідний 🙂"],
    "sunday": ["Вихідний 🙂"],
}

bells = [
    "0 пара: 08:00 – 08:50",
    "1 пара: 09:00 – 10:20",
    "2 пара: 10:30 – 11:50",
    "3 пара: 12:00 – 13:20",
    "4 пара: 13:40 – 15:00",
    "5 пара: 15:10 – 16:30",
    "6 пара: 16:40 – 18:00",
    "7 пара: 18:10 – 19:00",
]
