
import json
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect , reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Donation

@login_required
def donate_view(request):
    if request.method == "POST":
        try:
            amount = int(request.POST.get("amount"))
        except (TypeError, ValueError):
            messages.error(request, "Noto‘g‘ri summa")
            return redirect("donate")

        if amount < 1000:
            messages.error(request, "Minimal summa 1000 so‘m")
            return redirect("donate")
        callback_url = request.build_absolute_uri(reverse("payment_callback"))
        payload = {
            "amount": amount,
            "purpose": "donate",
            "reference_id": f"donate-{request.user.id}-{amount}",
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
        except Exception:
            messages.error(request, "Payment service bilan bog‘lanib bo‘lmadi")
            return redirect("donate")

        donation = Donation.objects.create(
            user=request.user,
            amount=amount,
            cheque_id=str(data["order_id"]),
            payment_url=data["payment_url"],
        )

        return redirect(donation.payment_url)

    total_amount = (
        Donation.objects.filter(status="paid")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    top_donators = (
        Donation.objects.filter(status="paid")
        .values("user__username")
        .annotate(total=Sum("amount"))
        .order_by("-total")[:10]
    )

    return render(request, "billing/donations/donate.html", {
        "total_amount": total_amount,
        "top_donators": top_donators,
    })



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

    donation = Donation.objects.filter(order_id=order_id).first()

    if not donation:
        return JsonResponse({"error": "not found"}, status=404)

    donation.raw_status = data

    if status == "success":
        donation.status = "paid"
        donation.paid_at = timezone.now()
    else:
        donation.status = "failed"

    donation.save()

    return JsonResponse({"ok": True})
