from django.db import models

from accounts.models import Account
from products.models import Product


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

        unique_together = (
            "account",
            "product",
        )

    def __str__(self):

        return f"{self.account.username} - {self.product.name}"