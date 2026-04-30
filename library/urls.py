from django.urls import path
from library.views import *

urlpatterns = [
    path("", CategoryListView.as_view(), name="category_list"),
    path("categories/<slug:category_slug>/", BookByCategoryListView.as_view(), name="book_list_by_category"),
    path("categories/<slug:category_slug>/<slug:book_slug>/", BookDetailView.as_view(), name="book_detail"),

]