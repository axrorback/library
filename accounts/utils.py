from random import randint
from secrets import token_urlsafe
import requests
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send_message(message,chat_id):
    requests.post(URL,data={'chat_id':chat_id,'text':message})

def generate_otp():
    return randint(111111,999999)

def generate_token():
    return token_urlsafe(16)