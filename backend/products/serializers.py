from rest_framework import serializers

from .models import (
    Product,
    ProductImage,
    ProductAttribute,
    ProductVariant,
    ProductInventory,
)


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = (
            "id",
            "product",
            "image",
            "alt_text",
            "is_primary",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
        )


class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = (
            "id",
            "product",
            "attribute_name",
            "attribute_value",
        )
        read_only_fields = (
            "id",
        )


class ProductVariantSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    class Meta:

        model = ProductVariant

        fields = (
            "id",
            "product",
            "product_name",
            "variant_name",
            "sku",
            "price",
            "discount_price",
            "is_active",
        )

        read_only_fields = (
            "id",
        )


class ProductInventorySerializer(serializers.ModelSerializer):

    available_stock = serializers.ReadOnlyField()

    class Meta:
        model = ProductInventory
        fields = (
            "id",
            "variant",
            "stock_quantity",
            "reserved_quantity",
            "low_stock_threshold",
            "available_stock",
        )
        read_only_fields = (
            "id",
            "available_stock",
        )


class ProductSerializer(serializers.ModelSerializer):

    average_rating = serializers.FloatField(read_only=True)
    total_reviews = serializers.IntegerField(read_only=True)

    images = ProductImageSerializer(
        many=True,
        read_only=True,
    )

    attributes = ProductAttributeSerializer(
        many=True,
        read_only=True,
    )

    variants = ProductVariantSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product

        fields = (
            "id",
            "seller",
            "category",
            "brand",
            "name",
            "slug",
            "description",
            "price",
            "discount_price",
            "sku",
            "weight",
            "is_featured",
            "is_active",
            "average_rating",
            "total_reviews",
            "images",
            "attributes",
            "variants",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "seller",
            "slug",
            "created_at",
            "updated_at",
        )