from django.contrib import admin

from .models import (
    Payment,
)


# ==========================================================
# Payment Admin
# ==========================================================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "account",
        "payment_method",
        "payment_status",
        "amount",
        "transaction_id",
        "created_at",
    )

    list_filter = (
        "payment_method",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "order__order_number",
        "account__username",
        "account__email",
        "transaction_id",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25