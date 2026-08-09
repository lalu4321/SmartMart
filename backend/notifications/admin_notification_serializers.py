from rest_framework import serializers

from .models import (
    Notification,
)


# ==========================================================
# Admin Notification Serializer
# ==========================================================

class AdminNotificationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="account.username",
        read_only=True,
    )

    class Meta:

        model = Notification

        fields = (
            "id",
            "account",
            "username",
            "title",
            "message",
            "notification_type",
            "is_read",
            "created_at",
        )

        read_only_fields = (
            "id",
            "username",
            "created_at",
        )