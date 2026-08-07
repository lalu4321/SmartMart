from django.contrib import admin

from .models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "slug",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "slug",
        "description",
        "website",
    )

    ordering = (
        "name",
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    fieldsets = (
        (
            "Brand Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "logo",
                    "description",
                    "website",
                    "is_active",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    actions = (
        "activate_brands",
        "deactivate_brands",
    )

    @admin.action(description="Activate selected brands")
    def activate_brands(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected brands")
    def deactivate_brands(self, request, queryset):
        queryset.update(is_active=False)