from rest_framework import serializers

from .models import Review


# ==========================================
# Admin Review Serializer
# ==========================================

class AdminReviewSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="account.username",
        read_only=True
    )

    customer_email = serializers.CharField(
        source="account.email",
        read_only=True
    )

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:

        model = Review

        fields = (
            "id",
            "product",
            "product_name",
            "account",
            "customer_name",
            "customer_email",
            "rating",
            "review",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )