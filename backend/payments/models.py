from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import Account
from orders.models import Order

from .validators import (
    validate_amount,
    validate_transaction_id,
)


# ==========================================================
# Payment
# ==========================================================

class Payment(models.Model):

    class PaymentMethod(models.TextChoices):

        CASH_ON_DELIVERY = (
            "COD",
            "Cash On Delivery",
        )

        UPI = (
            "UPI",
            "UPI",
        )

        CARD = (
            "CARD",
            "Card",
        )

        NET_BANKING = (
            "NET_BANKING",
            "Net Banking",
        )

    class PaymentStatus(models.TextChoices):

        PENDING = (
            "PENDING",
            "Pending",
        )

        SUCCESS = (
            "SUCCESS",
            "Success",
        )

        FAILED = (
            "FAILED",
            "Failed",
        )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            validate_amount,
        ],
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        validators=[
            validate_transaction_id,
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

        verbose_name = "Payment"

        verbose_name_plural = "Payments"

    def clean(self):

        super().clean()

        if (
            self.payment_method
            == self.PaymentMethod.CASH_ON_DELIVERY
            and self.transaction_id
        ):

            raise ValidationError(
                {
                    "transaction_id":
                    (
                        "Cash On Delivery "
                        "does not require a "
                        "transaction ID."
                    )
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.order.id}"
            f" - "
            f"{self.payment_status}"
        )