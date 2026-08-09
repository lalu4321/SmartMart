from rest_framework import serializers

from orders.models import (
    Order,
    OrderItem,
    ReturnRequest,
)


# ==========================================================
# Seller Order Item Serializer
# ==========================================================

class SellerOrderItemSerializer(serializers.ModelSerializer):

    class Meta:

        model = OrderItem

        fields = (
            "id",
            "variant",
            "quantity",
            "unit_price",
            "total_price",
        )


# ==========================================================
# Seller Order Serializer
# ==========================================================

class SellerOrderSerializer(serializers.ModelSerializer):

    items = SellerOrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:

        model = Order

        fields = (
            "id",
            "order_number",
            "account",
            "shipping_address",
            "status",
            "total_amount",
            "items",
            "created_at",
        )


# ==========================================================
# Update Order Status Serializer
# ==========================================================

class UpdateOrderStatusSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=Order.OrderStatus.choices,
    )


# ==========================================================
# Seller Return Request Serializer
# ==========================================================

class SellerReturnRequestSerializer(serializers.ModelSerializer):

    class Meta:

        model = ReturnRequest

        fields = (
            "id",
            "order",
            "reason",
            "status",
            "requested_at",
            "updated_at",
        )