from rest_framework import serializers


from .models import (
    Order,
    OrderItem,
    OrderStatusHistory,
    ReturnRequest,
    Refund,
)


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem

        fields = (
            "id",
            "variant",
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