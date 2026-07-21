from django.db import models

from accounts.models import Account
from products.models import Product


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

    rating = models.PositiveSmallIntegerField()

    review = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        unique_together = (
            "account",
            "product",
        )

    def __str__(self):
        return f"{self.account.username} - {self.product.name}"