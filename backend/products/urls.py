from django.urls import path

from .views import (
    ProductCreateAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    ProductUpdateAPIView,
    ProductDeleteAPIView,
    ProductImageCreateAPIView,
    ProductImageListAPIView,
    ProductImageDetailAPIView,
    ProductImageUpdateAPIView,
    ProductImageDeleteAPIView,
    ProductAttributeCreateAPIView,
    ProductAttributeListAPIView,
    ProductAttributeDetailAPIView,
    ProductAttributeUpdateAPIView,
    ProductAttributeDeleteAPIView,
    ProductVariantCreateAPIView,
    ProductVariantListAPIView,
    ProductVariantDetailAPIView,
    ProductVariantUpdateAPIView,
    ProductVariantDeleteAPIView,
    ProductInventoryCreateAPIView,
    ProductInventoryListAPIView,
    ProductInventoryDetailAPIView,
    ProductInventoryUpdateAPIView,
    ProductInventoryDeleteAPIView,
)

urlpatterns = [

    # Product APIs
    path("create/", ProductCreateAPIView.as_view(), name="product-create"),

    path("", ProductListAPIView.as_view(), name="product-list"),

    path("<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),

    path("<int:pk>/update/", ProductUpdateAPIView.as_view(), name="product-update"),

    path("<int:pk>/delete/", ProductDeleteAPIView.as_view(), name="product-delete"),

    # Product Image APIs
    path("image/create/", ProductImageCreateAPIView.as_view(), name="product-image-create"),

    path("image/list/", ProductImageListAPIView.as_view(), name="product-image-list"),

    path("image/<int:pk>/", ProductImageDetailAPIView.as_view(), name="product-image-detail"),

    path("image/<int:pk>/update/", ProductImageUpdateAPIView.as_view(), name="product-image-update"),

    path("image/<int:pk>/delete/", ProductImageDeleteAPIView.as_view(), name="product-image-delete"),

    # Product Attribute APIs
    path("attribute/create/", ProductAttributeCreateAPIView.as_view(), name="product-attribute-create"),

    path("attribute/list/", ProductAttributeListAPIView.as_view(), name="product-attribute-list"),

    path("attribute/<int:pk>/", ProductAttributeDetailAPIView.as_view(), name="product-attribute-detail"),

    path("attribute/<int:pk>/update/", ProductAttributeUpdateAPIView.as_view(), name="product-attribute-update"),

    path("attribute/<int:pk>/delete/", ProductAttributeDeleteAPIView.as_view(), name="product-attribute-delete"),

    # Product Variant APIs
    path("variant/create/", ProductVariantCreateAPIView.as_view(), name="product-variant-create"),

    path("variant/list/", ProductVariantListAPIView.as_view(), name="product-variant-list"),

    path("variant/<int:pk>/", ProductVariantDetailAPIView.as_view(), name="product-variant-detail"),

    path("variant/<int:pk>/update/", ProductVariantUpdateAPIView.as_view(), name="product-variant-update"),

    path("variant/<int:pk>/delete/", ProductVariantDeleteAPIView.as_view(), name="product-variant-delete"),

    # Product Inventory APIs
    path("inventory/create/", ProductInventoryCreateAPIView.as_view(), name="product-inventory-create"),

    path("inventory/list/", ProductInventoryListAPIView.as_view(), name="product-inventory-list"),

    path("inventory/<int:pk>/", ProductInventoryDetailAPIView.as_view(), name="product-inventory-detail"),

    path("inventory/<int:pk>/update/", ProductInventoryUpdateAPIView.as_view(), name="product-inventory-update"),

    path("inventory/<int:pk>/delete/", ProductInventoryDeleteAPIView.as_view(), name="product-inventory-delete"),

]