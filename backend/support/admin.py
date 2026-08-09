from django.contrib import admin

from .models import (
    SupportTicket,
    TicketReply,
)


# ==========================================================
# Support Ticket Admin
# ==========================================================

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "account",
        "subject",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "subject",
        "message",
        "account__username",
        "account__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )


# ==========================================================
# Ticket Reply Admin
# ==========================================================

@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "ticket",
        "account",
        "created_at",
    )

    search_fields = (
        "message",
        "account__username",
        "account__email",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )