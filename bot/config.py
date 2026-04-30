import os
import telebot
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)