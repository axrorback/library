import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import now
from library.models import BookPurchase


@csrf_exempt
def payment_callback(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "invalid json"}, status=400)

    order_id = str(data.get("order_id"))
    status = data.get("status")

    purchase = BookPurchase.objects.filter(cheque_id=order_id).first()

    if not purchase:
        return JsonResponse({"error": "not found"}, status=404)

    purchase.raw_status = data

    if status == "success":
        purchase.status = "paid"
        purchase.paid_at = now()
    else:
        purchase.status = "failed"

    purchase.save()

    return JsonResponse({"ok": True})