from django.shortcuts import render , get_object_or_404
from library.models import Book , Category


def book_list_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    books = category.books.all()  # related_name='books'
    return render(request, "library/book_list.html", {"category": category, "books": books})
