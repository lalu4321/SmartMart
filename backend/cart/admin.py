from django.contrib import admin

from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "account",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "account__username",
        "account__email",
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cart",
        "variant",
        "quantity",
        "total_price",
        "created_at",
    )

    search_fields = (
        "variant__variant_name",
        "cart__account__username",
    )