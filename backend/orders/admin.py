from django.contrib import admin

from .models import (
    Order,
    OrderItem,
    OrderStatusHistory,
    ReturnRequest,
    Refund,
)


# ==========================================================
# Order
# ==========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order_number",
        "account",
        "status",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "account__username",
        "account__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25


# ==========================================================
# Order Item
# ==========================================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "variant",
        "quantity",
        "unit_price",
        "total_price",
    )

    search_fields = (
        "order__order_number",
        "variant__variant_name",
        "variant__product__name",
    )

    ordering = (
        "order",
    )

    list_per_page = 25


# ==========================================================
# Order Status History
# ==========================================================

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order__order_number",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25


# ==========================================================
# Return Request
# ==========================================================

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "status",
        "requested_at",
    )

    list_filter = (
        "status",
        "requested_at",
    )

    search_fields = (
        "order__order_number",
    )

    readonly_fields = (
        "requested_at",
        "updated_at",
    )

    ordering = (
        "-requested_at",
    )

    list_per_page = 25


# ==========================================================
# Refund
# ==========================================================

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "return_request",
        "amount",
        "status",
        "refunded_at",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "return_request__order__order_number",
    )

    readonly_fields = (
        "created_at",
        "refunded_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25