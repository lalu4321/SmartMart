from django.db import models

from accounts.models import Account
from orders.models import Order


class Payment(models.Model):

    class PaymentMethod(models.TextChoices):

        CASH_ON_DELIVERY = "COD", "Cash On Delivery"

        UPI = "UPI", "UPI"

        CARD = "CARD", "Card"

        NET_BANKING = "NET_BANKING", "Net Banking"

    class PaymentStatus(models.TextChoices):

        PENDING = "PENDING", "Pending"

        SUCCESS = "SUCCESS", "Success"

        FAILED = "FAILED", "Failed"

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.order.id} - {self.payment_status}"