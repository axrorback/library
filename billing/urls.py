from django.urls import path
from billing.views import *

urlpatterns = [
    path('donate/',donate_view,name='donate'),
    path('callback/',payment_callback,name='payment_callback')

]