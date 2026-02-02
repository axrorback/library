# library/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from library.models import Book, Category, BookPurchase


@login_required
def book_detail(request, category_slug, book_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    book = get_object_or_404(Book, slug=book_slug, is_active=True, categories=category)

    has_access = book.is_free
    if request.user.is_authenticated and not has_access:
        has_access = BookPurchase.objects.filter(
            user=request.user, book=book, status=BookPurchase.Status.PAID
        ).exists()

    return render(request, "library/book_detail.html", {
        "category": category,
        "book": book,
        "has_access": has_access,
    })
