from celery import shared_task
from django.template.loader import render_to_string
from accounts.models import CustomUser
from accounts.utils import EmailService


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def mail_task(self, user_id, otp_code):
    try:
        user = CustomUser.objects.get(id=user_id)

        if not user.email:
            return "User email topilmadi"

        context = {
            'username': user.username,
            'otp_code': otp_code
        }

        html_content = render_to_string('emails/otp_email.html', context)

        email_service = EmailService()
        email_service.send_email(
            to_email=user.email,
            subject="Tasdiqlash kodi",
            html_content=html_content,
            to_name=user.username
        )

        return f"Email {user.email} ga yuborildi"

    except CustomUser.DoesNotExist:
        return "Xato: Foydalanuvchi topilmadi"