from random import randint
from secrets import token_urlsafe
import requests
import os
from dotenv import load_dotenv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send_message(message,chat_id):
    requests.post(URL,data={'chat_id':chat_id,'text':message})

def generate_otp():
    return randint(111111,999999)

def generate_token():
    return token_urlsafe(16)



class EmailService:
    def __init__(self):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY

        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

    def send_email(self, to_email, subject, html_content, to_name=None):
        try:
            email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{
                    "email": to_email,
                    "name": to_name or ""
                }],
                sender={
                    "email": settings.DEFAULT_FROM_EMAIL,
                    "name": "Library"
                },
                subject=subject,
                html_content=html_content
            )

            response = self.api_instance.send_transac_email(email)
            return response

        except ApiException as e:
            print("Brevo error:", e)
            raise