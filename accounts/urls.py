from django.urls import path
from accounts.views import register

urlpatterns = [
    path('register/', register , name='register'),
    path('change-email-register/', change_email_and_resend , name='change_email'),
    path('forgot-password/', forgot_password , name='forgot_password'),
    path('reset-password-confirm/<str:token>/', reset_password_confirm, name='reset_password_confirm'),
    path('profile/', profile_view, name='profile_view'),
    path('profile-edit/', profile_edit, name='profile_edit'),
    path('change-password/', change_password, name='change_password'),
]