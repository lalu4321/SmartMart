from django.db import models
from django.core.exceptions import ValidationError

from .validators import (
    validate_coupon_code,
    validate_discount_value,
    validate_usage_limit,
)


# ==========================================================
# Coupon
# ==========================================================

class Coupon(models.Model):

    class DiscountType(models.TextChoices):

        PERCENTAGE = (
            "PERCENTAGE",
            "Percentage",
        )

        FIXED = (
            "FIXED",
            "Fixed",
        )


    code = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            validate_coupon_code,
        ],
    )

    description = models.TextField(
        blank=True,
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            validate_discount_value,
        ],
    )

    minimum_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    maximum_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    usage_limit = models.PositiveIntegerField(
        default=1,
        validators=[
            validate_usage_limit,
        ],
    )

    used_count = models.PositiveIntegerField(
        default=0,
    )

    valid_from = models.DateTimeField()

    valid_until = models.DateTimeField()

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

        ordering = (
            "-created_at",
        )

        verbose_name = "Coupon"

        verbose_name_plural = "Coupons"


    def clean(self):

        if self.valid_until <= self.valid_from:

            raise ValidationError(
                "Valid until date must be after valid from date."
            )


        if (
            self.discount_type == self.DiscountType.PERCENTAGE
            and self.discount_value > 100
        ):

            raise ValidationError(
                "Percentage discount cannot exceed 100."
            )


        if self.used_count > self.usage_limit:

            raise ValidationError(
                "Used count cannot exceed usage limit."
            )


    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(
            *args,
            **kwargs,
        )


    def __str__(self):

        return self.code