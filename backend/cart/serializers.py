from rest_framework import serializers

from .models import (
    Cart,
    CartItem,
)

from products.serializers import (
    ProductVariantSerializer,
)


# ==========================================================
# Cart Item Serializer
# ==========================================================

class CartItemSerializer(serializers.ModelSerializer):

    variant = ProductVariantSerializer(
        read_only=True,
    )

    total_price = serializers.ReadOnlyField()

    class Meta:

        model = CartItem

        fields = (
            "id",
            "variant",
            "quantity",
            "total_price",
        )

        read_only_fields = (
            "id",
            "variant",
            "total_price",
        )


# ==========================================================
# Cart Serializer
# ==========================================================

class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:

        model = Cart

        fields = (
            "id",
            "account",
            "items",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "account",
            "created_at",
            "updated_at",
        )