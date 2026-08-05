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
        read_only=True
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

    seller_name = serializers.CharField(
        source="seller.shop_name",
        read_only=True
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    brand_name = serializers.CharField(
        source="brand.name",
        read_only=True
    )

    average_rating = serializers.FloatField(
        read_only=True
    )

    total_reviews = serializers.IntegerField(
        read_only=True
    )

    discount_percentage = serializers.SerializerMethodField()

    product_image = serializers.SerializerMethodField()

    stock = serializers.SerializerMethodField()

    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    attributes = ProductAttributeSerializer(
        many=True,
        read_only=True
    )

    variants = ProductVariantSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Product

        fields = (

            "id",

            "seller",
            "seller_name",

            "category",
            "category_name",

            "brand",
            "brand_name",

            "name",
            "slug",
            "description",

            "price",
            "discount_price",
            "discount_percentage",

            "sku",
            "weight",

            "is_featured",
            "is_active",

            "average_rating",
            "total_reviews",

            "stock",
            "product_image",

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

    def get_discount_percentage(self, obj):

        if obj.discount_price:

            return round(

                (
                    (obj.price - obj.discount_price)
                    / obj.price
                ) * 100,

                2

            )

        return 0

    def get_product_image(self, obj):

        primary_image = obj.images.filter(
            is_primary=True
        ).first()

        if not primary_image:

            primary_image = obj.images.first()

        if primary_image and primary_image.image:

            request = self.context.get("request")

            if request:

                return request.build_absolute_uri(
                    primary_image.image.url
                )

            return primary_image.image.url

        return None

    def get_stock(self, obj):

        inventories = ProductInventory.objects.filter(
            variant__product=obj
        )

        total_stock = sum(

            inventory.available_stock

            for inventory in inventories

        )

        return total_stock