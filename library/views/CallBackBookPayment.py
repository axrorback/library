from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction as db_transaction
from django.conf import settings
from tspay import TsPayClient
from tspay.exceptions import TsPayError
from library.models import BookPurchase
from billing.models import Donation
from billing.views import _get_json_payload, _get_cheque_id, _is_browser_request





def _redirect_or_json(request, obj, status: str):

    if _is_browser_request(request):
        # Donation bo'lsa
        if obj.__class__.__name__ == "Donation":
            if status in ("paid", "already_paid"):
                return redirect("donate-thank-you", username=obj.user.username)
            return redirect("donate")

        if obj.__class__.__name__ == "BookPurchase":
            category = obj.book.categories.first()
            if category:
                return redirect("book_detail", category_slug=category.slug, book_slug=obj.book.slug)
            return redirect("category_list")

    return JsonResponse({"ok": True, "status": status})


@csrf_exempt
def tspay_callback(request):
    payload = _get_json_payload(request)
    cheque_id = _get_cheque_id(request)
    if not cheque_id:
        return JsonResponse({"ok": False, "error": "cheque_id missing"}, status=400)

    donation = Donation.objects.filter(cheque_id=cheque_id).first()
    purchase = None if donation else BookPurchase.objects.filter(cheque_id=cheque_id).first()

    if not donation and not purchase:
        return JsonResponse({"ok": False, "error": "transaction not found"}, status=404)

    obj = donation or purchase
    client = TsPayClient()
    try:
        status_payload = client.check_transaction(
            access_token=settings.TSPAY_SHOP_ACCESS_TOKEN,
            cheque_id=cheque_id,
        )
    except TsPayError as e:
        obj.raw_status = {"error": str(e)}
        obj.save(update_fields=["raw_status"])
        return JsonResponse({"ok": False, "error": str(e)}, status=502)

    gateway_status = (status_payload.get("status") or "").lower()
    obj.raw_status = status_payload

    with db_transaction.atomic():
        obj = obj.__class__.objects.select_for_update().get(pk=obj.pk)

        if obj.status == obj.Status.PAID:
            return _redirect_or_json(request, obj, "already_paid")

        if gateway_status in ("paid", "success", "succeeded", "completed"):
            obj.status = obj.Status.PAID
            obj.paid_at = timezone.now()
            obj.save(update_fields=["status", "paid_at", "raw_status"])
            return _redirect_or_json(request, obj, "paid")

        if gateway_status in ("failed", "canceled", "cancelled", "error"):
            obj.status = obj.Status.FAILED
            obj.save(update_fields=["status", "raw_status"])
            return _redirect_or_json(request, obj, "failed")

        obj.status = obj.Status.PENDING
        obj.save(update_fields=["status", "raw_status"])
        return _redirect_or_json(request, obj, "pending")
