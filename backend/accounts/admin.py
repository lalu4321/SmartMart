from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account


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
    )

    list_filter = (
        "role",
        "is_verified",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "phone",
    )

    ordering = ("id",)