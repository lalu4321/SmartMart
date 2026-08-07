from django.core.exceptions import ValidationError


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

    if value > 100:

        raise ValidationError(
            "Maximum quantity allowed is 100."
        )