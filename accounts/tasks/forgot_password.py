from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from accounts.models import CustomUser
from accounts.utils import EmailService

@shared_task(name="accounts.tasks.send_reset_password_mail")
def send_reset(user_id, token, domain):
    try:
        user = CustomUser.objects.get(id=user_id)

        protocol = "https" if not settings.DEBUG else "http"
        reset_link = f"{protocol}://{domain}/accounts/reset-password-confirm/{token}/"

        context = {
            'username': user.username,
            'reset_link': reset_link,
            'expiration_time': 10
        }

        html_message = render_to_string('emails/password_reset_email.html', context)

        email_service = EmailService()
        email_service.send_email(
            to_email=user.email,
            subject="Parolni qayta tiklash",
            html_content=html_message,
            to_name=user.username
        )

        return f"Reset link sent to {user.email}"

    except CustomUser.DoesNotExist:
        return "User not found"