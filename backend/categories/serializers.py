from django.db import transaction

from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category

        fields = (
            "id",
            "name",
            "slug",
            "parent",
            "description",
            "image",
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

        queryset = Category.objects.filter(
            name__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Category with this name already exists."
            )

        return value

    # ==========================================
    # Parent Validation
    # ==========================================

    def validate_parent(self, value):

        if (
            self.instance
            and value
            and value == self.instance
        ):
            raise serializers.ValidationError(
                "A category cannot be its own parent."
            )

        return value

    # ==========================================
    # Object Validation
    # ==========================================

    def validate(self, attrs):

        parent = attrs.get(
            "parent",
            getattr(self.instance, "parent", None),
        )

        if (
            self.instance
            and parent
            and parent == self.instance
        ):
            raise serializers.ValidationError(
                {
                    "parent":
                    "A category cannot be its own parent."
                }
            )

        return attrs

    # ==========================================
    # Create
    # ==========================================

    @transaction.atomic
    def create(self, validated_data):

        category = Category.objects.create(
            **validated_data
        )

        return category

    # ==========================================
    # Update
    # ==========================================

    @transaction.atomic
    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance