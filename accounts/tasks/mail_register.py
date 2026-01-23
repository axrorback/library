from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def mail_task(user_id, otp_code):
    try:
        user = User.objects.get(id=user_id)
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
    except User.DoesNotExist:
        return "Xato: Foydalanuvchi topilmadi"