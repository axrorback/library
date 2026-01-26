# donations/models.py
from django.conf import settings
from django.db import models

class Donation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="donations")
    amount = models.PositiveIntegerField()
    cheque_id = models.CharField(max_length=128, unique=True, null=True, blank=True)
    payment_url = models.URLField(blank=True)
    status = models.CharField(max_length=16, choices=Status, default=Status.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    raw_status = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
