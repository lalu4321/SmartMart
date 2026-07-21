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

    def validate_email(self, value):
        if not value.endswith("@gmail.com"):
            raise serializers.ValidationError(
                "Only Gmail addresses are allowed."
            )
        return value

    def validate_phone(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        if value and len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must be exactly 10 digits."
            )

        return value

    def validate(self, attrs):
        role = attrs.get("role")
        phone = attrs.get("phone")

        if role == Account.Role.SELLER and not phone:
            raise serializers.ValidationError(
                {
                    "phone": "Seller must provide a phone number."
                }
            )

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")

        account = Account(**validated_data)
        account.set_password(password)
        account.save()

        return account
    

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