from rest_framework import serializers

from .models import Cart, CartItem
from products.serializers import ProductVariantSerializer


class CartItemSerializer(serializers.ModelSerializer):

    variant = ProductVariantSerializer(read_only=True)

    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem

        fields = (
            "id",
            "variant",
            "quantity",
            "total_price",
        )


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