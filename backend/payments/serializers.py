from rest_framework import serializers

from .models import (
    Payment,
)


# ==========================================================
# Payment Serializer
# ==========================================================

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Payment

        fields = (
            "id",
            "order",
            "account",
            "payment_method",
            "payment_status",
            "amount",
            "transaction_id",
            "created_at",
        )

        read_only_fields = (
            "id",
            "order",
            "account",
            "amount",
            "payment_status",
            "transaction_id",
            "created_at",
        )