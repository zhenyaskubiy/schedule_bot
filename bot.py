import os
from dotenv import load_dotenv
import telebot
from telebot import types
from datetime import datetime

load_dotenv()

TOKEN = os.getenv("TOKEN")
