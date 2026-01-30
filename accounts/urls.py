from django.urls import path
from accounts.views import *
from django.contrib.auth.views import LoginView , LogoutView
urlpatterns = [
    path('register/', register , name='register'),
    path('login/',LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('verify-otp/', verify_otp , name='verify_otp'),
    path('resend-otp/', resend_otp , name='resend_otp'),
    path('change-email-register/', change_email_and_resend , name='change_email'),
    path('forgot-password/', forgot_password , name='forgot_password'),
    path('reset-password-confirm/<str:token>/', reset_password_confirm, name='reset_password_confirm'),
    path('profile/', profile_view, name='profile_view'),
    path('profile-edit/', profile_edit, name='profile_edit'),
    path('change-password/', change_password, name='change_password'),
    path('telegram-code/', enter_telegram_id, name='telegram_code'),
    path('telegram-send/', send_telegram_code, name='send_telegram_code'), # bu formda kera bolgan manga tegilmasin umuman @axrorback
    path('verify-telegram/', verify_telegram, name='verify_telegram'),
    path('disconnect-telegram/', disconnect_telegram, name='disconnect_telegram'), #telegramni uzishga kerak bu (Night actions bu AI emas!)


]