from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="account.username",
        read_only=True
    )

    is_owner = serializers.SerializerMethodField()

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
            "is_owner",
        )

        read_only_fields = (
            "id",
            "account",
            "username",
            "created_at",
            "updated_at",
            "is_owner",
        )

    def get_is_owner(self, obj):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            return obj.account == request.user

        return False

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value