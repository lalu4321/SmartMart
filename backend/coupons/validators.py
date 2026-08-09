from django.core.exceptions import ValidationError


# ==========================================================
# Coupon Code Validator
# ==========================================================

def validate_coupon_code(value):

    if not value:

        raise ValidationError(
            "Coupon code is required."
        )

    value = value.strip().upper()

    if len(value) < 3:

        raise ValidationError(
            "Coupon code must contain at least 3 characters."
        )

    if len(value) > 50:

        raise ValidationError(
            "Coupon code cannot exceed 50 characters."
        )


# ==========================================================
# Discount Value Validator
# ==========================================================

def validate_discount_value(value):

    if value <= 0:

        raise ValidationError(
            "Discount value must be greater than zero."
        )


# ==========================================================
# Usage Limit Validator
# ==========================================================

def validate_usage_limit(value):

    if value < 1:

        raise ValidationError(
            "Usage limit must be at least 1."
        )