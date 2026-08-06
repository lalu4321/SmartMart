from rest_framework import serializers

from .models import ContactMessage


class AdminContactSerializer(serializers.ModelSerializer):

    class Meta:

        model = ContactMessage

        fields = (
            "id",
            "name",
            "email",
            "subject",
            "message",
            "is_read",
            "created_at",
        )