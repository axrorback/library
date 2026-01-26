from django.contrib import admin
from django.utils.safestring import mark_safe

from billing.models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "status",          # list_editable uchun shart
        "status_badge",    # chiroyli ko‘rinish
        "created_at",
        "paid_at",
        "cheque_id_short",
    )
    list_editable = ("status",)

    list_filter = ("status", "created_at", "paid_at")
    search_fields = ("user__username", "user__email", "cheque_id")
    list_select_related = ("user",)
    ordering = ("-created_at",)

    readonly_fields = ("created_at", "paid_at", "raw_status")

    fieldsets = (
        ("User & Amount", {"fields": ("user", "amount")}),
        ("Payment", {"fields": ("status", "cheque_id", "payment_url")}),
        ("Timestamps", {"fields": ("created_at", "paid_at")}),
        ("Raw Payload", {"fields": ("raw_status",)}),
    )

    @admin.display(description="Cheque ID")
    def cheque_id_short(self, obj):
        if not obj.cheque_id:
            return "-"
        return f"{obj.cheque_id[:8]}…{obj.cheque_id[-6:]}"

    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj):
        s = (obj.status or "").lower()
        if s == "paid":
            return mark_safe('<b style="color:#16a34a;">PAID</b>')
        if s == "failed":
            return mark_safe('<b style="color:#dc2626;">FAILED</b>')
        return mark_safe('<b style="color:#f59e0b;">PENDING</b>')
