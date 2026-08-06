from rest_framework import serializers

from .models import Payment


# ==========================================
# Admin Payment Serializer
# ==========================================

class AdminPaymentSerializer(serializers.ModelSerializer):

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

    order_number = serializers.CharField(
        source="order.order_number",
        read_only=True
    )

    order_status = serializers.CharField(
        source="order.status",
        read_only=True
    )

    class Meta:

        model = Payment

        fields = (
            "id",
            "order_number",
            "customer_name",
            "customer_email",
            "customer_phone",
            "payment_method",
            "payment_status",
            "amount",
            "transaction_id",
            "order_status",
            "created_at",
        )


# ==========================================
# Update Payment Status Serializer
# ==========================================

class AdminPaymentStatusSerializer(serializers.Serializer):

    payment_status = serializers.ChoiceField(
        choices=Payment.PaymentStatus.choices
    )