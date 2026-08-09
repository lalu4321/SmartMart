from django.db import models

from accounts.models import Account
from products.models import Product, ProductVariant

from .validators import validate_product


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


    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        related_name="wishlist_variants",
        null=True,
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        ordering = ["-created_at"]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "account",
                    "product",
                    "variant",
                ],
                name="unique_account_product_variant_wishlist",
            ),

        ]


    def clean(self):

        super().clean()

        validate_product(
            self.product
        )


    def save(self,*args,**kwargs):

        self.full_clean()

        super().save(*args,**kwargs)


    def __str__(self):

        return (
            f"{self.account.username}"
            f" - "
            f"{self.product.name}"
        )