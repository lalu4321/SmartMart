from decimal import Decimal
import re

from django.core.exceptions import ValidationError


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