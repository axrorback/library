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

    order_id = data.get("order_id")
    status = data.get("status")

    try:
        purchase = BookPurchase.objects.get(id=order_id)
    except BookPurchase.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)

    purchase.raw_status = data

    if status == "success":
        purchase.status = "paid"
        purchase.paid_at = now()
    elif status == "failed":
        purchase.status = "failed"

    purchase.save()

    return JsonResponse({"ok": True})