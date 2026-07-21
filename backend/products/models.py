from django.db import models

from accounts.models import SellerProfile
from brands.models import Brand
from categories.models import Category


class Product(models.Model):

    seller = models.ForeignKey(
        SellerProfile,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    sku = models.CharField(
        max_length=50,
        unique=True
    )

    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="products/"
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True
    )

    is_primary = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} Image"

class ProductAttribute(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="attributes"
    )

    attribute_name = models.CharField(max_length=100)

    attribute_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.attribute_name}: {self.attribute_value}"

class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    variant_name = models.CharField(max_length=100)

    sku = models.CharField(
        max_length=50,
        unique=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.variant_name}"

class ProductInventory(models.Model):

    variant = models.OneToOneField(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="inventory"
    )

    stock_quantity = models.PositiveIntegerField(default=0)

    reserved_quantity = models.PositiveIntegerField(default=0)

    low_stock_threshold = models.PositiveIntegerField(default=5)

    @property
    def available_stock(self):
        return self.stock_quantity - self.reserved_quantity

    def __str__(self):
        return f"{self.variant.sku} Inventory"

