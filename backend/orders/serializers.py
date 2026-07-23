from rest_framework import serializers

from .models import (
    Order,
    OrderItem,
    OrderStatusHistory,
    ReturnRequest,
    Refund,
)


class OrderItemSerializer(serializers.ModelSerializer):

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
            "variant",
            "product_name",
            "variant_name",
            "quantity",
            "unit_price",
            "total_price",
        )


class OrderStatusHistorySerializer(serializers.ModelSerializer):

    class Meta:

        model = OrderStatusHistory

        fields = (
            "id",
            "status",
            "remarks",
            "created_at",
        )


class OrderSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="account.username",
        read_only=True
    )

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    status_history = OrderStatusHistorySerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Order

        fields = (
            "id",
            "order_number",
            "account",
            "customer_name",
            "shipping_address",
            "status",
            "total_amount",
            "items",
            "status_history",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "order_number",
            "account",
            "customer_name",
            "status",
            "total_amount",
            "created_at",
            "updated_at",
        )


class ReturnRequestSerializer(serializers.ModelSerializer):

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

        read_only_fields = (
            "id",
            "status",
            "requested_at",
            "updated_at",
        )


class RefundSerializer(serializers.ModelSerializer):

    class Meta:

        model = Refund

        fields = (
            "id",
            "return_request",
            "amount",
            "status",
            "refunded_at",
            "created_at",
        )

        read_only_fields = (
            "id",
            "amount",
            "status",
            "refunded_at",
            "created_at",
        )