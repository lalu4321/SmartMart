from django.contrib import admin

from .models import (
    Product,
    ProductImage,
    ProductAttribute,
    ProductVariant,
    ProductInventory,
)


# ==========================================================
# Product
# ==========================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "seller",
        "category",
        "brand",
        "price",
        "discount_price",
        "sku",
        "is_featured",
        "is_active",
        "created_at",
    )

    list_filter = (
        "category",
        "brand",
        "is_featured",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "sku",
        "seller__shop_name",
        "category__name",
        "brand__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    ordering = (
        "-created_at",
    )

    list_per_page = 25


# ==========================================================
# Product Image
# ==========================================================

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "is_primary",
        "created_at",
    )

    list_filter = (
        "is_primary",
        "created_at",
    )

    search_fields = (
        "product__name",
        "alt_text",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25


# ==========================================================
# Product Attribute
# ==========================================================

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "attribute_name",
        "attribute_value",
    )

    list_filter = (
        "attribute_name",
    )

    search_fields = (
        "product__name",
        "attribute_name",
        "attribute_value",
    )

    ordering = (
        "product",
        "attribute_name",
    )

    list_per_page = 25


# ==========================================================
# Product Variant
# ==========================================================

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "variant_name",
        "sku",
        "price",
        "discount_price",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "product__name",
        "variant_name",
        "sku",
    )

    ordering = (
        "product",
        "variant_name",
    )

    list_per_page = 25


# ==========================================================
# Product Inventory
# ==========================================================

@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "variant",
        "stock_quantity",
        "reserved_quantity",
        "available_stock",
        "low_stock_threshold",
    )

    search_fields = (
        "variant__variant_name",
        "variant__sku",
        "variant__product__name",
    )

    readonly_fields = (
        "available_stock",
    )

    ordering = (
        "variant",
    )

    list_per_page = 25