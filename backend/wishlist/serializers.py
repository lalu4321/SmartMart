from rest_framework import serializers

from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):

    class Meta:

        model = Wishlist

        fields = (
            "id",
            "account",
            "product",
            "created_at",
        )

        read_only_fields = (
            "id",
            "account",
            "created_at",
        )