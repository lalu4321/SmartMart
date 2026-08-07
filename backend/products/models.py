from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from accounts.models import SellerProfile
from brands.models import Brand
from categories.models import Category

from .validators import (
    validate_product_name,
    validate_product_description,
    validate_price,
    validate_discount_price,
    validate_product_weight,
    validate_sku,
    validate_product_image,
    validate_alt_text,
    validate_attribute_name,
    validate_attribute_value,
    validate_variant_name,
    validate_stock_quantity,
    validate_reserved_quantity,
    validate_low_stock_threshold,
)


class Product(models.Model):

    seller = models.ForeignKey(
        SellerProfile,
        on_delete=models.CASCADE,
        related_name="products",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="products",
    )

    name = models.CharField(
        max_length=200,
        validators=[validate_product_name],
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField(
        validators=[validate_product_description],
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_price],
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[validate_discount_price],
    )

    sku = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_sku],
    )

    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[validate_product_weight],
    )

    is_featured = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def clean(self):
        super().clean()

        if self.name:
            self.name = self.name.strip()

        if self.description:
            self.description = self.description.strip()

        if self.sku:
            self.sku = self.sku.strip().upper()

        if (
            self.discount_price is not None
            and self.discount_price >= self.price
        ):
            raise ValidationError(
                {
                    "discount_price":
                    "Discount price must be less than product price."
                }
            )

        if self.category and not self.category.is_active:
            raise ValidationError(
                {
                    "category":
                    "Selected category is inactive."
                }
            )

        if self.brand and not self.brand.is_active:
            raise ValidationError(
                {
                    "brand":
                    "Selected brand is inactive."
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(
                slug=slug
            ).exclude(
                pk=self.pk
            ).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="products/",
        validators=[validate_product_image],
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
        validators=[validate_alt_text],
    )

    is_primary = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def clean(self):
        super().clean()

        if self.alt_text:
            self.alt_text = self.alt_text.strip()

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product,
                is_primary=True,
            ).exclude(
                pk=self.pk,
            ).update(
                is_primary=False,
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} Image"

class ProductAttribute(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="attributes",
    )

    attribute_name = models.CharField(
        max_length=100,
        validators=[validate_attribute_name],
    )

    attribute_value = models.CharField(
        max_length=255,
        validators=[validate_attribute_value],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["attribute_name"]
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "product",
                    "attribute_name",
                    "attribute_value",
                ],
                name="unique_product_attribute",
            ),
        ]

    def clean(self):
        super().clean()

        if self.attribute_name:
            self.attribute_name = (
                self.attribute_name.strip().title()
            )

        if self.attribute_value:
            self.attribute_value = (
                self.attribute_value.strip()
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.attribute_name}: "
            f"{self.attribute_value}"
        )

class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    variant_name = models.CharField(
        max_length=100,
        validators=[validate_variant_name],
    )

    sku = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_sku],
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_price],
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[validate_discount_price],
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["variant_name"]
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "product",
                    "variant_name",
                ],
                name="unique_product_variant_name",
            ),
        ]

    def clean(self):
        super().clean()

        if self.variant_name:
            self.variant_name = (
                self.variant_name.strip().title()
            )

        if self.sku:
            self.sku = self.sku.strip().upper()

        if (
            self.discount_price is not None
            and self.discount_price >= self.price
        ):
            raise ValidationError(
                {
                    "discount_price":
                    "Discount price must be less than variant price."
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.product.name} - "
            f"{self.variant_name}"
        )

class ProductInventory(models.Model):

    variant = models.OneToOneField(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="inventory",
    )

    stock_quantity = models.PositiveIntegerField(
        default=0,
        validators=[validate_stock_quantity],
    )

    reserved_quantity = models.PositiveIntegerField(
        default=0,
        validators=[validate_reserved_quantity],
    )

    low_stock_threshold = models.PositiveIntegerField(
        default=5,
        validators=[validate_low_stock_threshold],
    )

    class Meta:
        ordering = ["variant"]
        verbose_name = "Product Inventory"
        verbose_name_plural = "Product Inventories"

    @property
    def available_stock(self):
        return (
            self.stock_quantity
            - self.reserved_quantity
        )

    def clean(self):
        super().clean()

        if self.reserved_quantity > self.stock_quantity:
            raise ValidationError(
                {
                    "reserved_quantity":
                    "Reserved quantity cannot exceed stock quantity."
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.variant.sku} Inventory"