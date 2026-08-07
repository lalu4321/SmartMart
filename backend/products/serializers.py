from django.db import transaction

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

    # ==========================================
    # Image Validation
    # ==========================================

    def validate_image(self, value):

        if not value:
            raise serializers.ValidationError(
                "Product image is required."
            )

        return value

    # ==========================================
    # Alt Text Validation
    # ==========================================

    def validate_alt_text(self, value):

        if value:
            value = value.strip()

        return value

    # ==========================================
    # Object Validation
    # ==========================================

    def validate(self, attrs):

        product = attrs.get(
            "product",
            getattr(self.instance, "product", None),
        )

        is_primary = attrs.get(
            "is_primary",
            False,
        )

        if (
            product
            and is_primary
        ):

            queryset = ProductImage.objects.filter(
                product=product,
                is_primary=True,
            )

            if self.instance:
                queryset = queryset.exclude(
                    pk=self.instance.pk
                )

            if queryset.exists():

                queryset.update(
                    is_primary=False
                )

        return attrs

    # ==========================================
    # Create
    # ==========================================

    @transaction.atomic
    def create(self, validated_data):

        return ProductImage.objects.create(
            **validated_data
        )

    # ==========================================
    # Update
    # ==========================================

    @transaction.atomic
    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

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

    # ==========================================
    # Attribute Name Validation
    # ==========================================

    def validate_attribute_name(self, value):

        return value.strip().title()

    # ==========================================
    # Attribute Value Validation
    # ==========================================

    def validate_attribute_value(self, value):

        return value.strip()

    # ==========================================
    # Object Validation
    # ==========================================

    def validate(self, attrs):

        product = attrs.get(
            "product",
            getattr(self.instance, "product", None),
        )

        attribute_name = attrs.get(
            "attribute_name",
            getattr(self.instance, "attribute_name", None),
        )

        attribute_value = attrs.get(
            "attribute_value",
            getattr(self.instance, "attribute_value", None),
        )

        queryset = ProductAttribute.objects.filter(
            product=product,
            attribute_name__iexact=attribute_name,
            attribute_value__iexact=attribute_value,
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                {
                    "attribute_name":
                    "This attribute already exists for this product."
                }
            )

        return attrs

    # ==========================================
    # Create
    # ==========================================

    @transaction.atomic
    def create(self, validated_data):

        return ProductAttribute.objects.create(
            **validated_data
        )

    # ==========================================
    # Update
    # ==========================================

    @transaction.atomic
    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

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

    # ==========================================
    # Variant Name Validation
    # ==========================================

    def validate_variant_name(self, value):

        return value.strip().title()

    # ==========================================
    # SKU Validation
    # ==========================================

    def validate_sku(self, value):

        value = value.strip().upper()

        queryset = ProductVariant.objects.filter(
            sku__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "SKU already exists."
            )

        return value

    # ==========================================
    # Object Validation
    # ==========================================

    def validate(self, attrs):

        product = attrs.get(
            "product",
            getattr(self.instance, "product", None),
        )

        variant_name = attrs.get(
            "variant_name",
            getattr(self.instance, "variant_name", None),
        )

        queryset = ProductVariant.objects.filter(
            product=product,
            variant_name__iexact=variant_name,
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                {
                    "variant_name":
                    "This variant already exists for this product."
                }
            )

        price = attrs.get(
            "price",
            getattr(self.instance, "price", None),
        )

        discount_price = attrs.get(
            "discount_price",
            getattr(self.instance, "discount_price", None),
        )

        if (
            discount_price is not None
            and price is not None
            and discount_price >= price
        ):
            raise serializers.ValidationError(
                {
                    "discount_price":
                    "Discount price must be less than price."
                }
            )

        return attrs

    # ==========================================
    # Create
    # ==========================================

    @transaction.atomic
    def create(self, validated_data):

        return ProductVariant.objects.create(
            **validated_data
        )

    # ==========================================
    # Update
    # ==========================================

    @transaction.atomic
    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

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

    # ==========================================
    # Stock Quantity Validation
    # ==========================================

    def validate_stock_quantity(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Stock quantity cannot be negative."
            )

        return value

    # ==========================================
    # Reserved Quantity Validation
    # ==========================================

    def validate_reserved_quantity(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Reserved quantity cannot be negative."
            )

        return value

    # ==========================================
    # Low Stock Threshold Validation
    # ==========================================

    def validate_low_stock_threshold(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Low stock threshold cannot be negative."
            )

        return value

    # ==========================================
    # Object Validation
    # ==========================================

    def validate(self, attrs):

        stock_quantity = attrs.get(
            "stock_quantity",
            getattr(
                self.instance,
                "stock_quantity",
                0,
            ),
        )

        reserved_quantity = attrs.get(
            "reserved_quantity",
            getattr(
                self.instance,
                "reserved_quantity",
                0,
            ),
        )

        if reserved_quantity > stock_quantity:
            raise serializers.ValidationError(
                {
                    "reserved_quantity":
                    (
                        "Reserved quantity cannot exceed "
                        "stock quantity."
                    )
                }
            )

        return attrs

    # ==========================================
    # Create
    # ==========================================

    @transaction.atomic
    def create(self, validated_data):

        return ProductInventory.objects.create(
            **validated_data
        )

    # ==========================================
    # Update
    # ==========================================

    @transaction.atomic
    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

class ProductSerializer(serializers.ModelSerializer):

    seller_name = serializers.CharField(
        source="seller.shop_name",
        read_only=True,
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    brand_name = serializers.CharField(
        source="brand.name",
        read_only=True,
    )

    average_rating = serializers.FloatField(
        read_only=True,
    )

    total_reviews = serializers.IntegerField(
        read_only=True,
    )

    discount_percentage = serializers.SerializerMethodField()

    product_image = serializers.SerializerMethodField()

    stock = serializers.SerializerMethodField()

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

    # ==========================================
    # Name Validation
    # ==========================================

    def validate_name(self, value):

        return value.strip()

    # ==========================================
    # SKU Validation
    # ==========================================

    def validate_sku(self, value):

        value = value.strip().upper()

        queryset = Product.objects.filter(
            sku__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "SKU already exists."
            )

        return value

    # ==========================================
    # Object Validation
    # ==========================================

    def validate(self, attrs):

        price = attrs.get(
            "price",
            getattr(self.instance, "price", None),
        )

        discount_price = attrs.get(
            "discount_price",
            getattr(
                self.instance,
                "discount_price",
                None,
            ),
        )

        if (
            discount_price is not None
            and price is not None
            and discount_price >= price
        ):
            raise serializers.ValidationError(
                {
                    "discount_price":
                    "Discount price must be less than price."
                }
            )

        return attrs

    # ==========================================
    # Create
    # ==========================================

    @transaction.atomic
    def create(self, validated_data):

        return Product.objects.create(
            **validated_data
        )

    # ==========================================
    # Update
    # ==========================================

    @transaction.atomic
    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    # ==========================================
    # Discount Percentage
    # ==========================================

    def get_discount_percentage(self, obj):

        if (
            obj.discount_price
            and obj.price > 0
        ):
            return round(
                (
                    (
                        obj.price
                        - obj.discount_price
                    )
                    / obj.price
                )
                * 100,
                2,
            )

        return 0

    # ==========================================
    # Product Image
    # ==========================================

    def get_product_image(self, obj):

        primary_image = obj.images.filter(
            is_primary=True
        ).first()

        if primary_image is None:
            primary_image = obj.images.first()

        if (
            primary_image
            and primary_image.image
        ):

            request = self.context.get(
                "request"
            )

            if request:
                return request.build_absolute_uri(
                    primary_image.image.url
                )

            return primary_image.image.url

        return None

    # ==========================================
    # Stock
    # ==========================================

    def get_stock(self, obj):

        inventories = ProductInventory.objects.filter(
            variant__product=obj
        )

        return sum(
            inventory.available_stock
            for inventory in inventories
        )