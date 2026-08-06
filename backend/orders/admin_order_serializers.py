from rest_framework import serializers

from .models import (
    Order,
    OrderItem,
    OrderStatusHistory,
)


# ==========================================
# Order Item Serializer
# ==========================================

class AdminOrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="variant.product.name",
        read_only=True
    )

    variant_name = serializers.CharField(
        source="variant.variant_name",
        read_only=True
    )

    class Meta:

        model = OrderItem

        fields = (
            "id",
            "product_name",
            "variant_name",
            "quantity",
            "unit_price",
            "total_price",
        )


# ==========================================
# Status History Serializer
# ==========================================

class AdminOrderStatusHistorySerializer(serializers.ModelSerializer):

    class Meta:

        model = OrderStatusHistory

        fields = (
            "id",
            "status",
            "remarks",
            "created_at",
        )


# ==========================================
# Order Serializer
# ==========================================

class AdminOrderSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="account.username",
        read_only=True
    )

    customer_email = serializers.CharField(
        source="account.email",
        read_only=True
    )

    customer_phone = serializers.CharField(
        source="account.phone",
        read_only=True
    )

    shipping_name = serializers.CharField(
        source="shipping_address.full_name",
        read_only=True
    )

    shipping_phone = serializers.CharField(
        source="shipping_address.phone",
        read_only=True
    )

    shipping_city = serializers.CharField(
        source="shipping_address.city",
        read_only=True
    )

    shipping_state = serializers.CharField(
        source="shipping_address.state",
        read_only=True
    )

    shipping_pincode = serializers.CharField(
        source="shipping_address.pincode",
        read_only=True
    )

    items = AdminOrderItemSerializer(
        many=True,
        read_only=True
    )

    status_history = AdminOrderStatusHistorySerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Order

        fields = (
            "id",
            "order_number",
            "customer_name",
            "customer_email",
            "customer_phone",
            "shipping_name",
            "shipping_phone",
            "shipping_city",
            "shipping_state",
            "shipping_pincode",
            "status",
            "total_amount",
            "items",
            "status_history",
            "created_at",
            "updated_at",
        )


# ==========================================
# Update Status Serializer
# ==========================================

class AdminOrderStatusSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=Order.OrderStatus.choices
    )