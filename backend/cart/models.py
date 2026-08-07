from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import Account
from products.models import ProductVariant

from .validators import (
    validate_quantity,
)

# ==========================================================
# Cart
# ==========================================================

class Cart(models.Model):

    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Cart"

        verbose_name_plural = "Carts"

    def clean(self):

        super().clean()

        if (
            self.account
            and not self.account.is_active
        ):

            raise ValidationError(
                {
                    "account":
                    "Inactive account cannot have a cart."
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.account.username}'s Cart"

# ==========================================================
# Cart Item
# ==========================================================

class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[
            validate_quantity,
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Cart Item"

        verbose_name_plural = "Cart Items"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "cart",
                    "variant",
                ],
                name="unique_cart_variant",
            ),
        ]

    @property
    def total_price(self):

        return (
            self.variant.price
            * self.quantity
        )

    def clean(self):

        super().clean()

        if (
            self.variant
            and not self.variant.is_active
        ):

            raise ValidationError(
                {
                    "variant":
                    "Selected product variant is inactive."
                }
            )

        if (
            self.variant
            and hasattr(
                self.variant,
                "inventory",
            )
            and self.quantity
            > self.variant.inventory.available_stock
        ):

            raise ValidationError(
                {
                    "quantity":
                    "Requested quantity exceeds available stock."
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.variant.variant_name} "
            f"({self.quantity})"
        )