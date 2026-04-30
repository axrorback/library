from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from accounts.models import CustomUser


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def mail_task(self, user_id, otp_code):
    try:
        user = CustomUser.objects.get(id=user_id)

        if not user.email:
            return "User email topilmadi"

        subject = "Tasdiqlash kodi"

        context = {
            'username': user.username,
            'otp_code': otp_code
        }

        html_content = render_to_string('emails/otp_email.html', context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        return f"Email {user.email} ga yuborildi"

    except CustomUser.DoesNotExist:
        return "Xato: Foydalanuvchi topilmadi"