import uuid
from django.conf import settings
from django.db import models
from django.db.models import JSONField

class BookPurchase(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        CANCELED = "canceled", "Canceled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="book_purchases")
    book = models.ForeignKey("library.Book", on_delete=models.CASCADE, related_name="purchases")

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    raw_status = models.JSONField(default=dict, blank=True)
    cheque_id = models.CharField(max_length=128, unique=True)   # TsPay transaction id
    payment_url = models.URLField(blank=True)

    status = models.CharField(max_length=20, choices=Status, default=Status.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "book"], condition=models.Q(status="paid"), name="uniq_paid_purchase")
        ]

    def __str__(self):
        return f"{self.user} -> {self.book} ({self.status})"