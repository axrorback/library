from django.urls import path
from accounts.views import register

urlpatterns = [
    path('register/', register , name='register'),
    path('change-email-register/', change_email_and_resend , name='change_email'),
    path('forgot-password/', forgot_password , name='forgot_password'),
    path('reset-password-confirm/<str:token>/', reset_password_confirm, name='reset_password_confirm'),
]