from django.db import transaction

from rest_framework import serializers

from .models import Brand


class BrandSerializer(serializers.ModelSerializer):

    class Meta:

        model = Brand

        fields = (
            "id",
            "name",
            "slug",
            "logo",
            "description",
            "website",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "slug",
            "created_at",
            "updated_at",
        )

    # ==========================================
    # Name Validation
    # ==========================================

    def validate_name(self, value):

        value = value.strip()

        queryset = Brand.objects.filter(
            name__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Brand with this name already exists."
            )

        return value

    # ==========================================
    # Website Validation
    # ==========================================

    def validate_website(self, value):

        if value:
            value = value.strip().lower()

        return value

    # ==========================================
    # Object Validation
    # ==========================================

    def validate(self, attrs):

        return attrs

    # ==========================================
    # Create
    # ==========================================

    @transaction.atomic
    def create(self, validated_data):

        brand = Brand.objects.create(
            **validated_data
        )

        return brand

    # ==========================================
    # Update
    # ==========================================

    @transaction.atomic
    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance