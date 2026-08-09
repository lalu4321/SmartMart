from django.contrib import admin

from .models import (
    FAQ,
)


# ==========================================================
# FAQ Admin
# ==========================================================

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "question",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "question",
        "answer",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25