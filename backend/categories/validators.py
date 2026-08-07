import os
import re

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

MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB


# ==========================================================
# Category Name Validation
# ==========================================================

def validate_category_name(value):

    if value is None:
        return

    value = value.strip()

    if not value:
        raise ValidationError(
            "Category name is required."
        )

    if len(value) < 2:
        raise ValidationError(
            "Category name must contain at least 2 characters."
        )

    if len(value) > 100:
        raise ValidationError(
            "Category name cannot exceed 100 characters."
        )

    if value.isdigit():
        raise ValidationError(
            "Category name cannot contain only numbers."
        )

    if not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9 &'().,_/-]*",
        value,
    ):
        raise ValidationError(
            "Category name contains invalid characters."
        )


# ==========================================================
# Category Description Validation
# ==========================================================

def validate_category_description(value):

    if value in (None, ""):
        return

    value = value.strip()

    if len(value) > 1000:
        raise ValidationError(
            "Description cannot exceed 1000 characters."
        )

    if any(
        ord(char) < 32 and char not in "\n\r\t"
        for char in value
    ):
        raise ValidationError(
            "Description contains invalid characters."
        )


# ==========================================================
# Category Image Validation
# ==========================================================

def validate_category_image(value):

    if not value:
        return

    filename = getattr(value, "name", "")

    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            "Only JPG, JPEG, PNG and WEBP images are allowed."
        )

    size = getattr(value, "size", None)

    if size and size > MAX_IMAGE_SIZE:
        raise ValidationError(
            "Image size cannot exceed 2 MB."
        )

    content_type = getattr(value, "content_type", None)

    if (
        content_type
        and content_type.lower()
        not in ALLOWED_IMAGE_CONTENT_TYPES
    ):
        raise ValidationError(
            "Invalid image format."
        )