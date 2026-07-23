from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="account.username",
        read_only=True
    )

    class Meta:
        model = Review

        fields = (
            "id",
            "account",
            "username",
            "product",
            "rating",
            "review",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "account",
            "username",
            "created_at",
            "updated_at",
        )

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value