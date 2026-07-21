from django.contrib import admin
from .models import( Product, ProductImage, ProductAttribute,ProductVariant,ProductInventory,)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "seller",
        "category",
        "brand",
        "price",
        "is_active",
    )

    list_filter = (
        "category",
        "brand",
        "is_active",
    )

    search_fields = (
        "name",
        "sku",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    ordering = (
        "name",
    )


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
    )

    search_fields = (
        "product__name",
    )


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
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "variant_name",
        "price",
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
        "variant__product__name",
    )