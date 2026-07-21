from django.db import models

from accounts.models import Account, Address
from products.models import ProductVariant


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
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.order_number


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

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.variant.variant_name} x {self.quantity}"
    
    
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
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.order.order_number} - {self.status}"
    
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

    reason = models.TextField()

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

    def __str__(self):
        return f"{self.order.order_number} - {self.status}"
    
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
        decimal_places=2
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

    def __str__(self):
        return f"{self.return_request.order.order_number} - {self.status}"