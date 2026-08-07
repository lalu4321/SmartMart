from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import Account
from products.models import Product

from .validators import (
    validate_product,
)


# ==========================================================
# Wishlist
# ==========================================================

class Wishlist(models.Model):

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Wishlist"

        verbose_name_plural = "Wishlist"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "account",
                    "product",
                ],
                name="unique_account_product_wishlist",
            ),
        ]

    def clean(self):

        super().clean()

        validate_product(
            self.product
        )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.account.username}"
            f" - "
            f"{self.product.name}"
        )