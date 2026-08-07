from decimal import Decimal
import re

from django.core.exceptions import ValidationError


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


# ==========================================================
# Transaction ID
# ==========================================================

def validate_transaction_id(value):

    if not value:
        return

    value = value.strip()

    if len(value) > 255:

        raise ValidationError(
            "Transaction ID cannot exceed 255 characters."
        )

    if not re.fullmatch(
        r"[A-Za-z0-9_-]+",
        value,
    ):

        raise ValidationError(
            "Transaction ID contains invalid characters."
        )