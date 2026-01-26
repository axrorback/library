from django.urls import path
from billing.views import *

urlpatterns = [
    path('donate/',donate_page,name='donate'),
    path('callback/',tspay_callback,name='tspay_callback'),
    path('callback',tspay_callback,name='tspay_callback'),
    path('donate/thank-you/<str:username>/',thank_you_page,name='donate-thanks')

]