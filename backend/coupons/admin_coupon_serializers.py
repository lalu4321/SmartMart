from rest_framework import serializers

from .models import (
    Coupon,
)


# ==========================================================
# Admin Coupon Serializer
# ==========================================================

class AdminCouponSerializer(serializers.ModelSerializer):

    class Meta:

        model = Coupon

        fields = (
            "id",
            "code",
            "description",
            "discount_type",
            "discount_value",
            "minimum_order_amount",
            "maximum_discount",
            "usage_limit",
            "used_count",
            "valid_from",
            "valid_until",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "used_count",
            "created_at",
            "updated_at",
        )


# ==========================================================
# Admin Coupon Status Serializer
# ==========================================================

class AdminCouponStatusSerializer(serializers.Serializer):

    is_active = serializers.BooleanField()