from django.db.models import Count
from rest_framework import serializers

from orders.models import Order
from products.models import Product

from .models import SellerProfile


class AdminSellerSerializer(serializers.ModelSerializer):

    seller_name = serializers.CharField(
        source="shop_name",
        read_only=True,
    )

    owner_name = serializers.SerializerMethodField()

    email = serializers.CharField(
        source="account.email",
        read_only=True,
    )

    phone = serializers.CharField(
        source="account.phone",
        read_only=True,
    )

    is_active = serializers.BooleanField(
        source="account.is_active",
        read_only=True,
    )

    is_verified = serializers.BooleanField(
        source="is_verified",
        read_only=True,
    )

    total_products = serializers.SerializerMethodField()

    total_orders = serializers.SerializerMethodField()

    class Meta:

        model = SellerProfile

        fields = (
            "id",
            "seller_name",
            "owner_name",
            "email",
            "phone",
            "is_active",
            "is_verified",
            "total_products",
            "total_orders",
        )

        read_only_fields = fields

    def get_owner_name(self, obj):

        full_name = (
            f"{obj.account.first_name} "
            f"{obj.account.last_name}"
        ).strip()

        return full_name if full_name else obj.account.username

    def get_total_products(self, obj):

        return (
            Product.objects.filter(
                seller=obj,
            )
            .count()
        )

    def get_total_orders(self, obj):

        return (
            Order.objects.filter(
                items__variant__product__seller=obj
            )
            .distinct()
            .count()
        )