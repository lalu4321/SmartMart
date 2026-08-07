from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import Account
from products.models import Product

from .validators import (
    validate_rating,
    validate_review,
)


# ==========================================================
# Review
# ==========================================================

class Review(models.Model):

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            validate_rating,
        ],
    )

    review = models.TextField(
        validators=[
            validate_review,
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

        verbose_name = "Review"

        verbose_name_plural = "Reviews"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "account",
                    "product",
                ],
                name="unique_account_product_review",
            ),
        ]

    def clean(self):

        super().clean()

        if (
            self.product
            and not self.product.is_active
        ):

            raise ValidationError(
                {
                    "product":
                    "Inactive product cannot be reviewed."
                }
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