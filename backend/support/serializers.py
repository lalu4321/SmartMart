from rest_framework import serializers

from .models import (
    SupportTicket,
    TicketReply,
)


class SupportTicketSerializer(serializers.ModelSerializer):

    class Meta:

        model = SupportTicket

        fields = (
            "id",
            "account",
            "subject",
            "message",
            "status",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "account",
            "status",
            "created_at",
            "updated_at",
        )


class TicketReplySerializer(serializers.ModelSerializer):

    class Meta:

        model = TicketReply

        fields = (
            "id",
            "ticket",
            "account",
            "message",
            "created_at",
        )

        read_only_fields = (
            "id",
            "account",
            "created_at",
        )