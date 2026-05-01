from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from tspay.exceptions import TsPayError
from django.contrib.auth.decorators import login_required
from library.models import Book, BookPurchase
import requests


@login_required
def create_book_payment(request, id):
    book = get_object_or_404(Book, id=id, is_active=True)

    if book.is_free:
        return redirect("book_detail", category_slug=book.categories.first().slug, book_slug=book.slug)

    if BookPurchase.objects.filter(user=request.user, book=book, status=BookPurchase.Status.PAID).exists():
        return redirect("book_detail", category_slug=book.categories.first().slug, book_slug=book.slug)

    if not book.price:
        return redirect("book_detail", category_slug=book.categories.first().slug, book_slug=book.slug)


    callback_path = reverse("payment_callback_book")
    callback_url = request.build_absolute_uri(callback_path)
    payload = {
        "amount": book.price,
        "purpose": "book_purchase",
        "reference_id": f"book_purchase_{book.id}",
        "user_id": str(request.user.id),
        "callback_url": callback_url,
    }
    try:
        res = requests.post(
            "https://pay.axror.tech/payment/create/",
            json=payload,
            timeout=15
        )
        data = res.json()

        BookPurchase.objects.create(
            user=request.user,
            book=book,
            amount=book.price,
            cheque_id=str(data.get("order_id")),
            payment_url=data.get("payment_url", ""),
            status=BookPurchase.Status.PENDING,
        )

        return redirect(data["payment_url"])

    except TsPayError as e:
        return redirect("book_detail", category_slug=book.categories.first().slug, book_slug=book.slug)
