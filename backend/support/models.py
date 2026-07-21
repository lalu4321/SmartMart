from django.db import models

from accounts.models import Account


class SupportTicket(models.Model):

    class Status(models.TextChoices):

        OPEN = "OPEN", "Open"

        IN_PROGRESS = "IN_PROGRESS", "In Progress"

        CLOSED = "CLOSED", "Closed"

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="support_tickets"
    )

    subject = models.CharField(
        max_length=255
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.subject


class TicketReply(models.Model):

    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Reply {self.id}"