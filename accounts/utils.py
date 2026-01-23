from random import randint
from secrets import token_urlsafe

def generate_otp():
    return randint(111111,999999)

def generate_token():
    return token_urlsafe(16)