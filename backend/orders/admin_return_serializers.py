from rest_framework import serializers

from .models import (
    ReturnRequest,
    Refund,
)


# ==========================================================
# Admin Return Serializer
# ==========================================================

class AdminReturnSerializer(serializers.ModelSerializer):

    order_number = serializers.CharField(
        source="order.order_number",
        read_only=True,
    )

    customer_name = serializers.CharField(
        source="order.account.username",
        read_only=True,
    )

    class Meta:

        model = ReturnRequest

        fields = (
            "id",
            "order",
            "order_number",
            "customer_name",
            "reason",
            "status",
            "requested_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "order_number",
            "customer_name",
            "requested_at",
            "updated_at",
        )


# ==========================================================
# Admin Refund Serializer
# ==========================================================

class AdminRefundSerializer(serializers.ModelSerializer):

    order_number = serializers.CharField(
        source="return_request.order.order_number",
        read_only=True,
    )

    customer_name = serializers.CharField(
        source="return_request.order.account.username",
        read_only=True,
    )

    class Meta:

        model = Refund

        fields = (
            "id",
            "return_request",
            "order_number",
            "customer_name",
            "amount",
            "status",
            "refunded_at",
            "created_at",
        )

        read_only_fields = (
            "id",
            "order_number",
            "customer_name",
            "amount",
            "status",
            "refunded_at",
            "created_at",
        )