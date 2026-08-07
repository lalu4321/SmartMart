from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Account,
    Address,
    SellerProfile,
)


@admin.register(Account)
class AccountAdmin(UserAdmin):

    list_display = (
        "id",
        "username",
        "email",
        "phone",
        "role",
        "is_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    list_filter = (
        "role",
        "gender",
        "is_verified",
        "is_staff",
        "is_superuser",
        "is_active",
        "created_at",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_login",
        "date_joined",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "phone",
                    "role",
                    "gender",
                    "date_of_birth",
                    "profile_image",
                    "is_verified",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "email",
                    "phone",
                    "role",
                    "gender",
                    "date_of_birth",
                    "profile_image",
                )
            },
        ),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "account",
        "phone",
        "city",
        "state",
        "country",
        "pincode",
        "address_type",
        "is_default",
        "created_at",
    )

    list_filter = (
        "address_type",
        "is_default",
        "state",
        "country",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "city",
        "district",
        "state",
        "country",
        "pincode",
        "account__username",
        "account__email",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "shop_name",
        "account",
        "gst_number",
        "ifsc_code",
        "is_verified",
        "created_at",
    )

    list_filter = (
        "is_verified",
        "created_at",
    )

    search_fields = (
        "shop_name",
        "gst_number",
        "ifsc_code",
        "account__username",
        "account__email",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )