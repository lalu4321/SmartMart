from decimal import Decimal
import re

from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import (
    Account,
    Address,
)

from products.models import (
    ProductVariant,
)

from .validators import (
    validate_order_number,
    validate_amount,
    validate_quantity,
    validate_remarks,
    validate_return_reason,
)

# ==========================================================
# Order Number
# ==========================================================

def validate_order_number(value):

    if value is None:
        return

    value = value.strip().upper()

    if not value:
        raise ValidationError(
            "Order number is required."
        )

    if len(value) > 30:
        raise ValidationError(
            "Order number cannot exceed 30 characters."
        )

    if not re.fullmatch(
        r"[A-Z0-9_-]+",
        value,
    ):
        raise ValidationError(
            "Order number contains invalid characters."
        )


# ==========================================================
# Amount
# ==========================================================

def validate_amount(value):

    if value is None:
        raise ValidationError(
            "Amount is required."
        )

    if value <= Decimal("0"):
        raise ValidationError(
            "Amount must be greater than zero."
        )

    if value > Decimal("99999999.99"):
        raise ValidationError(
            "Amount is too large."
        )


# ==========================================================
# Quantity
# ==========================================================

def validate_quantity(value):

    if value is None:
        raise ValidationError(
            "Quantity is required."
        )

    if value <= 0:
        raise ValidationError(
            "Quantity must be greater than zero."
        )

    if value > 1000:
        raise ValidationError(
            "Quantity is too large."
        )


# ==========================================================
# Remarks
# ==========================================================

def validate_remarks(value):

    if value in (None, ""):
        return

    value = value.strip()

    if len(value) > 255:
        raise ValidationError(
            "Remarks cannot exceed 255 characters."
        )


# ==========================================================
# Return Reason
# ==========================================================

def validate_return_reason(value):

    if value is None:
        return

    value = value.strip()

    if len(value) < 10:
        raise ValidationError(
            "Return reason must contain at least 10 characters."
        )

    if len(value) > 1000:
        raise ValidationError(
            "Return reason cannot exceed 1000 characters."
        )


# ==========================================================
# Order
# ==========================================================

class Order(models.Model):

    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        SHIPPED = "SHIPPED", "Shipped"
        OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for Delivery"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    order_number = models.CharField(
        max_length=30,
        unique=True,
        validators=[validate_order_number],
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_amount],
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Order"

        verbose_name_plural = "Orders"

    def clean(self):

        super().clean()

        if self.order_number:
            self.order_number = (
                self.order_number
                .strip()
                .upper()
            )

        if (
            self.shipping_address
            and self.shipping_address.account
            != self.account
        ):
            raise ValidationError(
                {
                    "shipping_address":
                    (
                        "Shipping address must "
                        "belong to the customer."
                    )
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return self.order_number


# ==========================================================
# Order Item
# ==========================================================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name="order_items"
    )

    quantity = models.PositiveIntegerField(
        validators=[validate_quantity],
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_amount],
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_amount],
    )

    class Meta:

        ordering = ["id"]

        verbose_name = "Order Item"

        verbose_name_plural = "Order Items"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "order",
                    "variant",
                ],
                name="unique_order_variant",
            ),
        ]

    def clean(self):

        super().clean()

        if (
            self.quantity
            and self.unit_price
        ):

            expected_total = (
                self.quantity
                * self.unit_price
            )

            if self.total_price != expected_total:

                raise ValidationError(
                    {
                        "total_price":
                        (
                            "Total price must equal "
                            "quantity × unit price."
                        )
                    }
                )

        if (
            self.variant
            and not self.variant.is_active
        ):

            raise ValidationError(
                {
                    "variant":
                    "Selected variant is inactive."
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.variant.variant_name} "
            f"x {self.quantity}"
        )



# ==========================================================
# Order Status History
# ==========================================================

class OrderStatusHistory(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="status_history"
    )

    status = models.CharField(
        max_length=20,
        choices=Order.OrderStatus.choices
    )

    remarks = models.CharField(
        max_length=255,
        blank=True,
        validators=[validate_remarks],
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Order Status History"

        verbose_name_plural = "Order Status Histories"

    def clean(self):

        super().clean()

        if self.remarks:
            self.remarks = self.remarks.strip()

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.order.order_number}"
            f" - "
            f"{self.status}"
        )

from .validators import (
    validate_return_reason,
)

# ==========================================================
# Return Request
# ==========================================================

class ReturnRequest(models.Model):

    class ReturnStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        COMPLETED = "COMPLETED", "Completed"

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="returns"
    )

    reason = models.TextField(
        validators=[validate_return_reason],
    )

    status = models.CharField(
        max_length=20,
        choices=ReturnStatus.choices,
        default=ReturnStatus.PENDING
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-requested_at"]

        verbose_name = "Return Request"

        verbose_name_plural = "Return Requests"

        constraints = [
            models.UniqueConstraint(
                fields=["order"],
                name="unique_return_request_per_order",
            ),
        ]

    def clean(self):

        super().clean()

        if self.reason:
            self.reason = self.reason.strip()

        if self.order:

            if self.order.status != Order.OrderStatus.DELIVERED:

                raise ValidationError(
                    {
                        "order":
                        (
                            "Return request can only be "
                            "created for delivered orders."
                        )
                    }
                )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.order.order_number}"
            f" - "
            f"{self.status}"
        )



# ==========================================================
# Refund
# ==========================================================

class Refund(models.Model):

    class RefundStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSED = "PROCESSED", "Processed"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    return_request = models.OneToOneField(
        ReturnRequest,
        on_delete=models.CASCADE,
        related_name="refund"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_amount],
    )

    status = models.CharField(
        max_length=20,
        choices=RefundStatus.choices,
        default=RefundStatus.PENDING
    )

    refunded_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Refund"

        verbose_name_plural = "Refunds"

    def clean(self):

        super().clean()

        if (
            self.return_request
            and self.amount
            > self.return_request.order.total_amount
        ):

            raise ValidationError(
                {
                    "amount":
                    (
                        "Refund amount cannot exceed "
                        "the order total amount."
                    )
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.return_request.order.order_number}"
            f" - "
            f"{self.status}"
        )