from django.db import transaction
from rest_framework import serializers

from .models import Account, Address, SellerProfile


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account

        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "gender",
            "profile_image",
            "date_of_birth",
            "is_active",
            "is_verified",
            "created_at",
        )

        read_only_fields = (
            "id",
            "is_verified",
            "created_at",
        )

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    # =====================================================
    # Username
    # =====================================================

    def validate_username(self, value):
        value = value.strip()

        queryset = Account.objects.filter(
            username__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    # =====================================================
    # Email
    # =====================================================

    def validate_email(self, value):
        value = value.strip().lower()

        if not value.endswith("@gmail.com"):
            raise serializers.ValidationError(
                "Only Gmail addresses are allowed."
            )

        queryset = Account.objects.filter(
            email__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    # =====================================================
    # Phone
    # =====================================================

    def validate_phone(self, value):
        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must be exactly 10 digits."
            )

        queryset = Account.objects.filter(
            phone=value
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Phone number already exists."
            )

        return value

    # =====================================================
    # Password
    # =====================================================

    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must contain at least 8 characters."
            )

        if len(value) > 20:
            raise serializers.ValidationError(
                "Password cannot exceed 20 characters."
            )

        if " " in value:
            raise serializers.ValidationError(
                "Password cannot contain spaces."
            )

        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not any(char.islower() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )

        special_characters = "@$#*_-/\\"

        if not any(char in special_characters for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )

        return value

    # =====================================================
    # Profile Image
    # =====================================================

    def validate_profile_image(self, value):

        if not value:
            return value

        allowed_extensions = (
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        )

        file_name = value.name.lower()

        if not file_name.endswith(allowed_extensions):
            raise serializers.ValidationError(
                "Only JPG, JPEG, PNG and WEBP images are allowed."
            )

        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError(
                "Image size cannot exceed 2 MB."
            )

        return value

    # =====================================================
    # Object Validation
    # =====================================================

    def validate(self, attrs):

        role = attrs.get(
            "role",
            getattr(self.instance, "role", None)
        )

        phone = attrs.get(
            "phone",
            getattr(self.instance, "phone", None)
        )

        if (
            role == Account.Role.SELLER
            and not phone
        ):
            raise serializers.ValidationError(
                {
                    "phone":
                    "Seller must provide a phone number."
                }
            )

        return attrs

    # =====================================================
    # Create
    # =====================================================

    @transaction.atomic
    def create(self, validated_data):

        password = validated_data.pop("password")

        account = Account(**validated_data)

        account.set_password(password)

        account.save()

        return account

    # =====================================================
    # Update
    # =====================================================

    @transaction.atomic
    def update(self, instance, validated_data):

        password = validated_data.pop(
            "password",
            None,
        )

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address

        fields = (
            "id",
            "full_name",
            "phone",
            "address_line1",
            "address_line2",
            "landmark",
            "city",
            "district",
            "state",
            "country",
            "pincode",
            "address_type",
            "is_default",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    # =====================================================
    # Validation
    # =====================================================

    def validate_full_name(self, value):
        return value.strip()

    def validate_city(self, value):
        return value.strip().title()

    def validate_district(self, value):
        return value.strip().title()

    def validate_state(self, value):
        return value.strip().title()

    def validate_country(self, value):
        return value.strip().title()

    def validate(self, attrs):

        account = self.context["request"].user

        if (
            attrs.get("is_default", False)
            and Address.objects.filter(
                account=account,
                is_default=True,
            ).exclude(
                pk=getattr(self.instance, "pk", None)
            ).exists()
        ):
            Address.objects.filter(
                account=account,
                is_default=True,
            ).exclude(
                pk=getattr(self.instance, "pk", None)
            ).update(
                is_default=False
            )

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        validated_data["account"] = self.context["request"].user

        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class SellerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerProfile

        fields = (
            "id",
            "shop_name",
            "shop_logo",
            "shop_description",
            "gst_number",
            "bank_account_name",
            "bank_account_number",
            "ifsc_code",
            "is_verified",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "is_verified",
            "created_at",
            "updated_at",
        )

    # =====================================================
    # Validation
    # =====================================================

    def validate_shop_name(self, value):
        return value.strip()

    def validate_gst_number(self, value):
        return value.strip().upper()

    def validate_ifsc_code(self, value):
        return value.strip().upper()

    def validate(self, attrs):

        request = self.context["request"]

        if request.user.role != Account.Role.SELLER:
            raise serializers.ValidationError(
                {
                    "detail":
                    "Only sellers can create a seller profile."
                }
            )

        queryset = SellerProfile.objects.filter(
            account=request.user
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                {
                    "detail":
                    "Seller profile already exists."
                }
            )

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        validated_data["account"] = self.context["request"].user

        return SellerProfile.objects.create(
            **validated_data
        )

    @transaction.atomic
    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

