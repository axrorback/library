from django.urls import path
from library.views import *

urlpatterns = [
    path("categories/", category_list, name="category_list"),
    path("categories/<slug:category_slug>/", book_list_by_category, name="book_list_by_category"),
    path("categories/<slug:category_slug>/<slug:book_slug>/", book_detail, name="book_detail"),
    path("<uuid:book_id>/pay/", create_book_payment, name="create_book_payment"),
    path('callback/',tspay_callback,name='tspay_callback')

]