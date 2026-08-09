from django.db import models

from .validators import (
    validate_question,
    validate_answer,
)


# ==========================================================
# FAQ
# ==========================================================

class FAQ(models.Model):

    question = models.CharField(
        max_length=255,
        validators=[
            validate_question,
        ],
    )

    answer = models.TextField(
        validators=[
            validate_answer,
        ],
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


    class Meta:

        ordering = [
            "-created_at",
        ]

        verbose_name = "FAQ"

        verbose_name_plural = "FAQs"


    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(
            *args,
            **kwargs,
        )


    def __str__(self):

        return self.question