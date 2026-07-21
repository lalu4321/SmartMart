from django.db import models

from accounts.models import Account
from products.models import ProductVariant


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

    def __str__(self):
        return f"{self.account.username}'s Cart"


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
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = (
            "cart",
            "variant",
        )

    @property
    def total_price(self):
        return self.variant.price * self.quantity

    def __str__(self):
        return f"{self.variant.variant_name} ({self.quantity})"