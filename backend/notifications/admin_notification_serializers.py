from rest_framework import serializers

from .models import Notification


class AdminNotificationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="account.username",
        read_only=True
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