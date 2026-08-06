from rest_framework import serializers

from .models import SellerProfile
from products.models import Product
from orders.models import Order


class AdminSellerSerializer(serializers.ModelSerializer):

    seller_name = serializers.CharField(
        source="shop_name",
        read_only=True
    )

    owner_name = serializers.SerializerMethodField()

    email = serializers.CharField(
        source="account.email",
        read_only=True
    )

    phone = serializers.CharField(
        source="account.phone",
        read_only=True
    )

    is_active = serializers.BooleanField(
        source="account.is_active",
        read_only=True
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
            "total_products",
            "total_orders",
            "is_active",
        )

    def get_owner_name(self, obj):

        return f"{obj.account.first_name} {obj.account.last_name}".strip()

    def get_total_products(self, obj):

        return Product.objects.filter(
            seller=obj
        ).count()

    def get_total_orders(self, obj):

        return (
            Order.objects.filter(
                items__variant__product__seller=obj
            )
            .distinct()
            .count()
        )