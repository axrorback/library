import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# donations/views.py
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from tspay import TsPayClient
from tspay.exceptions import TsPayError
from billing.forms import DonateForm
from .models import Donation
from django.db import transaction as db_transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def donate_page(request):
    form = DonateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        amount = form.cleaned_data["amount"]

        client = TsPayClient()
        try:
            tx = client.create_transaction(
                amount=amount,
                redirect_url='https://43048a2c02b2.ngrok-free.app/payment/callback/',
                comment=f"Donation user={request.user.username}",
                access_token=settings.TSPAY_SHOP_ACCESS_TOKEN,
            )

            Donation.objects.create(
                user=request.user,
                amount=amount,
                cheque_id=tx.get("cheque_id"),
                payment_url=tx.get("payment_url", ""),
                status=Donation.Status.PENDING,
            )
            return redirect(tx["payment_url"])

        except TsPayError as e:
            form.add_error(None, f"To'lov yaratishda xatolik: {str(e)}")

    top_donators = (
        Donation.objects.filter(status=Donation.Status.PAID)
        .select_related("user")
        .values("user__id", "user__username")
        .annotate(total=models.Sum("amount"))
        .order_by("-total")[:10]
    )

    return render(request, "billing/donations/donate.html", {"form": form, "top_donators": top_donators})



def _get_json_payload(request) -> dict:
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except Exception:
        return {}


def _get_cheque_id(request) -> str | None:
    payload = _get_json_payload(request)
    return (
        request.GET.get("cheque_id")
        or request.GET.get("chequeId")
        or request.GET.get("ChequeID")
        or request.GET.get("transaction_id")
        or request.GET.get("id")
        or request.POST.get("cheque_id")
        or request.POST.get("chequeId")
        or request.POST.get("ChequeID")
        or request.POST.get("transaction_id")
        or request.POST.get("id")
        or payload.get("cheque_id")
        or payload.get("chequeId")
        or payload.get("ChequeID")
        or payload.get("transaction_id")
        or payload.get("id")
        or (payload.get("transaction") or {}).get("id")
        or (payload.get("data") or {}).get("cheque_id")
    )


def _is_browser_request(request) -> bool:
    accept = (request.headers.get("Accept") or "").lower()
    user_agent = (request.headers.get("User-Agent") or "").lower()
    return ("text/html" in accept) or ("mozilla" in user_agent)


@csrf_exempt
def tspay_callback(request):
    payload = _get_json_payload(request)
    cheque_id = _get_cheque_id(request)
    if not cheque_id:
        return JsonResponse(
            {"ok": False, "error": "cheque_id missing", "get": dict(request.GET), "post": dict(request.POST), "json": payload},
            status=400
        )

    donation = get_object_or_404(Donation, cheque_id=cheque_id)

    if donation.status == Donation.Status.PAID:
        if _is_browser_request(request):
            return redirect("donate-thank-you", username=donation.user.username)
        return JsonResponse({"ok": True, "status": "already_paid"})

    client = TsPayClient()
    try:
        status_payload = client.check_transaction(
            access_token=settings.TSPAY_SHOP_ACCESS_TOKEN,
            cheque_id=cheque_id,
        )
    except TsPayError as e:
        donation.raw_status = {"error": str(e)}
        donation.save(update_fields=["raw_status"])
        if _is_browser_request(request):
            return redirect("donate")
        return JsonResponse({"ok": False, "error": str(e)}, status=502)

    gateway_status = (status_payload.get("status") or "").lower()

    donation.raw_status = status_payload

    with db_transaction.atomic():
        donation = Donation.objects.select_for_update().get(pk=donation.pk)

        if donation.status == Donation.Status.PAID:
            if _is_browser_request(request):
                return redirect("donate-thank-you", username=donation.user.username)
            return JsonResponse({"ok": True, "status": "already_paid"})

        if gateway_status in ("paid", "success", "succeeded", "completed"):
            donation.status = Donation.Status.PAID
            donation.paid_at = timezone.now()
            donation.save(update_fields=["status", "paid_at", "raw_status"])

            if _is_browser_request(request):
                return redirect("donate-thank-you", username=donation.user.username)
            return JsonResponse({"ok": True, "status": "paid"})

        if gateway_status in ("failed", "canceled", "cancelled", "error"):
            donation.status = Donation.Status.FAILED
            donation.save(update_fields=["status", "raw_status"])

            if _is_browser_request(request):
                return redirect("donate")
            return JsonResponse({"ok": True, "status": "failed"})

        donation.status = Donation.Status.PENDING
        donation.save(update_fields=["status", "raw_status"])

    if _is_browser_request(request):
        return redirect("donate")
    return JsonResponse({"ok": True, "status": "pending"})

def thank_you_page(request, username):

    user = get_object_or_404(User, username=username)

    last_donation = (
        Donation.objects
        .filter(user=user, status=Donation.Status.PAID)
        .order_by("-paid_at")
        .first()
    )

    return render(
        request,
        "billing/donations/thank_you.html",
        {"donator": user, "donation": last_donation},)