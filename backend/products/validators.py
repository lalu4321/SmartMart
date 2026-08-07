import os
import re
from decimal import Decimal

from django.core.exceptions import ValidationError


# ==========================================================
# Constants
# ==========================================================

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


# ==========================================================
# Product Name
# ==========================================================

def validate_product_name(value):

    if value is None:
        return

    value = value.strip()

    if not value:
        raise ValidationError(
            "Product name is required."
        )

    if len(value) < 3:
        raise ValidationError(
            "Product name must contain at least 3 characters."
        )

    if len(value) > 200:
        raise ValidationError(
            "Product name cannot exceed 200 characters."
        )

    if value.isdigit():
        raise ValidationError(
            "Product name cannot contain only numbers."
        )

    if not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9 &'().,_/+:-]*",
        value,
    ):
        raise ValidationError(
            "Product name contains invalid characters."
        )


# ==========================================================
# Product Description
# ==========================================================

def validate_product_description(value):

    if value is None:
        return

    value = value.strip()

    if len(value) < 10:
        raise ValidationError(
            "Description must contain at least 10 characters."
        )

    if len(value) > 5000:
        raise ValidationError(
            "Description cannot exceed 5000 characters."
        )


# ==========================================================
# Price
# ==========================================================

def validate_price(value):

    if value is None:
        raise ValidationError(
            "Price is required."
        )

    if value <= Decimal("0"):
        raise ValidationError(
            "Price must be greater than zero."
        )

    if value > Decimal("99999999.99"):
        raise ValidationError(
            "Price is too large."
        )


# ==========================================================
# Discount Price
# ==========================================================

def validate_discount_price(value):

    if value is None:
        return

    if value <= Decimal("0"):
        raise ValidationError(
            "Discount price must be greater than zero."
        )


# ==========================================================
# Weight
# ==========================================================

def validate_product_weight(value):

    if value is None:
        return

    if value <= Decimal("0"):
        raise ValidationError(
            "Weight must be greater than zero."
        )

    if value > Decimal("99999.99"):
        raise ValidationError(
            "Weight is too large."
        )


# ==========================================================
# SKU
# ==========================================================

def validate_sku(value):

    if value is None:
        return

    value = value.strip().upper()

    if len(value) < 3:
        raise ValidationError(
            "SKU must contain at least 3 characters."
        )

    if len(value) > 50:
        raise ValidationError(
            "SKU cannot exceed 50 characters."
        )

    if not re.fullmatch(
        r"[A-Z0-9_-]+",
        value,
    ):
        raise ValidationError(
            "SKU can contain only uppercase letters, numbers, hyphen and underscore."
        )

# ==========================================================
# Product Image
# ==========================================================

def validate_product_image(value):

    if not value:
        return

    filename = getattr(value, "name", "")

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            "Only JPG, JPEG, PNG and WEBP images are allowed."
        )

    size = getattr(value, "size", None)

    if size and size > MAX_IMAGE_SIZE:
        raise ValidationError(
            "Image size cannot exceed 5 MB."
        )

    content_type = getattr(
        value,
        "content_type",
        None,
    )

    if (
        content_type
        and content_type.lower()
        not in ALLOWED_IMAGE_CONTENT_TYPES
    ):
        raise ValidationError(
            "Invalid image format."
        )


# ==========================================================
# Alt Text
# ==========================================================

def validate_alt_text(value):

    if value in (None, ""):
        return

    value = value.strip()

    if len(value) > 255:
        raise ValidationError(
            "Alt text cannot exceed 255 characters."
        )


# ==========================================================
# Attribute Name
# ==========================================================

def validate_attribute_name(value):

    if value is None:
        return

    value = value.strip()

    if len(value) < 2:
        raise ValidationError(
            "Attribute name must contain at least 2 characters."
        )

    if len(value) > 100:
        raise ValidationError(
            "Attribute name cannot exceed 100 characters."
        )

    if not re.fullmatch(
        r"[A-Za-z0-9 ]+",
        value,
    ):
        raise ValidationError(
            "Attribute name contains invalid characters."
        )


# ==========================================================
# Attribute Value
# ==========================================================

def validate_attribute_value(value):

    if value is None:
        return

    value = value.strip()

    if len(value) < 1:
        raise ValidationError(
            "Attribute value is required."
        )

    if len(value) > 255:
        raise ValidationError(
            "Attribute value cannot exceed 255 characters."
        )

# ==========================================================
# Variant Name
# ==========================================================

def validate_variant_name(value):

    if value is None:
        return

    value = value.strip()

    if len(value) < 2:
        raise ValidationError(
            "Variant name must contain at least 2 characters."
        )

    if len(value) > 100:
        raise ValidationError(
            "Variant name cannot exceed 100 characters."
        )

    if not re.fullmatch(
        r"[A-Za-z0-9 &'().,_/+:-]+",
        value,
    ):
        raise ValidationError(
            "Variant name contains invalid characters."
        )


# ==========================================================
# Stock Quantity
# ==========================================================

def validate_stock_quantity(value):

    if value is None:
        return

    if value < 0:
        raise ValidationError(
            "Stock quantity cannot be negative."
        )

    if value > 1000000:
        raise ValidationError(
            "Stock quantity is too large."
        )


# ==========================================================
# Reserved Quantity
# ==========================================================

def validate_reserved_quantity(value):

    if value is None:
        return

    if value < 0:
        raise ValidationError(
            "Reserved quantity cannot be negative."
        )

    if value > 1000000:
        raise ValidationError(
            "Reserved quantity is too large."
        )


# ==========================================================
# Low Stock Threshold
# ==========================================================

def validate_low_stock_threshold(value):

    if value is None:
        return

    if value < 0:
        raise ValidationError(
            "Low stock threshold cannot be negative."
        )

    if value > 1000000:
        raise ValidationError(
            "Low stock threshold is too large."
        )