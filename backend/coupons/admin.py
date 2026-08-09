from django.contrib import admin

from .models import (
    Coupon,
)


# ==========================================================
# Coupon Admin
# ==========================================================

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "code",
        "discount_type",
        "discount_value",
        "usage_limit",
        "used_count",
        "is_active",
        "valid_from",
        "valid_until",
    )

    list_filter = (
        "discount_type",
        "is_active",
        "valid_from",
        "valid_until",
    )

    search_fields = (
        "code",
        "description",
    )

    readonly_fields = (
        "used_count",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25