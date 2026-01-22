from django.urls import path
from accounts.views import register

urlpatterns = [
    path('register/', register , name='register'),
]