from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()



@shared_task(name="accounts.tasks.send_reset_password_mail")
def send_reset(user_id, token, domain):
    try:
        user = User.objects.get(id=user_id)
        protocol = "https" if settings.DEBUG else "http"
        reset_link = f"{protocol}://{domain}/accounts/reset-password-confirm/{token}/"

        context = {
            'username': user.username,
            'reset_link': reset_link,
            'expiration_time': 10
        }

        html_message = render_to_string('emails/password_reset_email.html', context)
        plain_message = strip_tags(html_message)

        subject = "Parolni qayta tiklash"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [user.email]

        email = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
        email.attach_alternative(html_message, "text/html")
        email.send()

        return f"Reset link sent to {user.email}"
    except User.DoesNotExist:
        return "User not found"