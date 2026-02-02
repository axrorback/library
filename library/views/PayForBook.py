from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from tspay import TsPayClient
from tspay.exceptions import TsPayError
from django.contrib.auth.decorators import login_required
from library.models import Book, BookPurchase

@login_required
def create_book_payment(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_active=True)

    if book.is_free:
        return redirect("book_detail", category_slug=book.categories.first().slug, book_slug=book.slug)

    if BookPurchase.objects.filter(user=request.user, book=book, status=BookPurchase.Status.PAID).exists():
        return redirect("book_detail", category_slug=book.categories.first().slug, book_slug=book.slug)

    if not book.price:
        return redirect("book_detail", category_slug=book.categories.first().slug, book_slug=book.slug)

    client = TsPayClient()

    callback_path = reverse("tspay_callback")
    callback_url = request.build_absolute_uri(callback_path)

    try:
        tx = client.create_transaction(
            amount=float(book.price),
            redirect_url=callback_url,
            comment=f"BookPurchase User {request.user.username} Book {book.title}",
            access_token=settings.TSPAY_SHOP_ACCESS_TOKEN,
        )

        BookPurchase.objects.create(
            user=request.user,
            book=book,
            amount=book.price,
            cheque_id=tx.get("cheque_id"),
            payment_url=tx.get("payment_url", ""),
            status=BookPurchase.Status.PENDING,
        )

        return redirect(tx["payment_url"])

    except TsPayError as e:
        return redirect("book_detail", category_slug=book.categories.first().slug, book_slug=book.slug)
