from django.db import models

from .validators import (
    validate_name,
    validate_subject,
    validate_message,
)


# ==========================================================
# Contact Message
# ==========================================================

class ContactMessage(models.Model):

    name = models.CharField(
        max_length=100,
        validators=[
            validate_name,
        ],
    )

    email = models.EmailField()

    subject = models.CharField(
        max_length=255,
        validators=[
            validate_subject,
        ],
    )

    message = models.TextField(
        validators=[
            validate_message,
        ],
    )

    is_read = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    class Meta:

        ordering = (
            "-created_at",
        )

        verbose_name = "Contact Message"

        verbose_name_plural = "Contact Messages"


    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(
            *args,
            **kwargs,
        )


    def __str__(self):

        return self.subject