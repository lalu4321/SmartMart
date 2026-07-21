from django.db import models

from accounts.models import Account


class Notification(models.Model):

    class NotificationType(models.TextChoices):

        ORDER = "ORDER", "Order"

        PAYMENT = "PAYMENT", "Payment"

        RETURN = "RETURN", "Return"

        REFUND = "REFUND", "Refund"

        GENERAL = "GENERAL", "General"

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.GENERAL
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = (
            "-created_at",
        )

    def __str__(self):

        return f"{self.account.username} - {self.title}"