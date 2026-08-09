from rest_framework import serializers

from .models import (
    FAQ,
)


# ==========================================================
# FAQ Serializer
# ==========================================================

class FAQSerializer(serializers.ModelSerializer):

    class Meta:

        model = FAQ

        fields = (
            "id",
            "question",
            "answer",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )