import os
import re
from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


# ============================================================
# Common Constants
# ============================================================

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB

PHONE_PATTERN = re.compile(r"^[6-9]\d{9}$")

PINCODE_PATTERN = re.compile(r"^[1-9]\d{5}$")

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")

IFSC_PATTERN = re.compile(r"^[A-Z]{4}0[A-Z0-9]{6}$")

GST_PATTERN = re.compile(
    r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$"
)

BANK_ACCOUNT_PATTERN = re.compile(r"^[0-9]{9,18}$")

NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z .'-]*$")


# ============================================================
# Name Validation
# ============================================================

def validate_name(value):
    if value is None:
        return

    value = value.strip()

    if not value:
        raise ValidationError("Name cannot be empty.")

    if len(value) < 2:
        raise ValidationError(
            "Name must contain at least 2 characters."
        )

    if len(value) > 100:
        raise ValidationError(
            "Name cannot exceed 100 characters."
        )

    if not NAME_PATTERN.fullmatch(value):
        raise ValidationError(
            "Name can contain only letters, spaces, periods, "
            "apostrophes and hyphens."
        )


# ============================================================
# Username Validation
# ============================================================

def validate_username(value):
    if value is None:
        return

    value = value.strip()

    if not value:
        raise ValidationError("Username cannot be empty.")

    if len(value) < 4:
        raise ValidationError(
            "Username must contain at least 4 characters."
        )

    if len(value) > 30:
        raise ValidationError(
            "Username cannot exceed 30 characters."
        )

    if not USERNAME_PATTERN.fullmatch(value):
        raise ValidationError(
            "Username can contain only letters, numbers and underscores."
        )

    if value.startswith("_") or value.endswith("_"):
        raise ValidationError(
            "Username cannot start or end with an underscore."
        )

    if "__" in value:
        raise ValidationError(
            "Username cannot contain consecutive underscores."
        )


# ============================================================
# Email Validation
# ============================================================

def validate_account_email(value):
    if value is None:
        return

    value = value.strip()

    if not value:
        raise ValidationError("Email address is required.")

    if len(value) > 254:
        raise ValidationError(
            "Email address cannot exceed 254 characters."
        )

    try:
        validate_email(value)
    except ValidationError:
        raise ValidationError(
            "Enter a valid email address."
        )


# ============================================================
# Phone Validation
# ============================================================

def validate_phone(value):
    if value is None:
        return

    value = str(value).strip()

    if not value:
        raise ValidationError("Phone number is required.")

    if not value.isdigit():
        raise ValidationError(
            "Phone number must contain only digits."
        )

    if len(value) != 10:
        raise ValidationError(
            "Phone number must contain exactly 10 digits."
        )

    if not PHONE_PATTERN.fullmatch(value):
        raise ValidationError(
            "Phone number must start with 6, 7, 8 or 9."
        )


# ============================================================
# Date Of Birth Validation
# ============================================================

def validate_date_of_birth(value):
    if value is None:
        return

    if not isinstance(value, date):
        raise ValidationError(
            "Enter a valid date of birth."
        )

    today = date.today()

    if value > today:
        raise ValidationError(
            "Date of birth cannot be in the future."
        )

    age = (
        today.year
        - value.year
        - (
            (today.month, today.day)
            < (value.month, value.day)
        )
    )

    if age < 18:
        raise ValidationError(
            "You must be at least 18 years old."
        )

    if age > 110:
        raise ValidationError(
            "Age cannot exceed 110 years."
        )


# ============================================================
# Profile / Shop Image Validation
# ============================================================

def validate_image(value):
    if not value:
        return

    filename = getattr(value, "name", "")

    if not filename:
        raise ValidationError(
            "Invalid image file."
        )

    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            "Only JPG, JPEG, PNG and WEBP images are allowed."
        )

    size = getattr(value, "size", None)

    if size is not None and size > MAX_IMAGE_SIZE:
        raise ValidationError(
            "Image size cannot exceed 2 MB."
        )

    content_type = getattr(value, "content_type", None)

    allowed_content_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if (
        content_type
        and content_type.lower() not in allowed_content_types
    ):
        raise ValidationError(
            "Invalid image format."
        )


# ============================================================
# Pincode Validation
# ============================================================

def validate_pincode(value):
    if value is None:
        return

    value = str(value).strip()

    if not value:
        raise ValidationError(
            "Pincode is required."
        )

    if not value.isdigit():
        raise ValidationError(
            "Pincode must contain only digits."
        )

    if not PINCODE_PATTERN.fullmatch(value):
        raise ValidationError(
            "Enter a valid 6-digit Indian pincode."
        )


# ============================================================
# Address Text Validation
# ============================================================

def validate_address_text(value):
    if value is None:
        return

    value = value.strip()

    if not value:
        raise ValidationError(
            "Address cannot be empty."
        )

    if len(value) < 3:
        raise ValidationError(
            "Address must contain at least 3 characters."
        )

    if len(value) > 255:
        raise ValidationError(
            "Address cannot exceed 255 characters."
        )

    # Reject control characters.
    if any(ord(character) < 32 for character in value):
        raise ValidationError(
            "Address contains invalid characters."
        )


# ============================================================
# City / District / State / Country Validation
# ============================================================

def validate_location_name(value):
    if value is None:
        return

    value = value.strip()

    if not value:
        raise ValidationError(
            "This field cannot be empty."
        )

    if len(value) < 2:
        raise ValidationError(
            "This field must contain at least 2 characters."
        )

    if len(value) > 100:
        raise ValidationError(
            "This field cannot exceed 100 characters."
        )

    if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", value):
        raise ValidationError(
            "Only letters, spaces, periods, apostrophes and hyphens "
            "are allowed."
        )


# ============================================================
# GST Number Validation
# ============================================================

def validate_gst_number(value):
    if value is None:
        return

    value = value.strip().upper()

    if not value:
        raise ValidationError(
            "GST number is required."
        )

    if len(value) != 15:
        raise ValidationError(
            "GST number must contain exactly 15 characters."
        )

    if not GST_PATTERN.fullmatch(value):
        raise ValidationError(
            "Enter a valid GST number."
        )


# ============================================================
# IFSC Code Validation
# ============================================================

def validate_ifsc_code(value):
    if value is None:
        return

    value = value.strip().upper()

    if not value:
        raise ValidationError(
            "IFSC code is required."
        )

    if len(value) != 11:
        raise ValidationError(
            "IFSC code must contain exactly 11 characters."
        )

    if not IFSC_PATTERN.fullmatch(value):
        raise ValidationError(
            "Enter a valid IFSC code."
        )


# ============================================================
# Bank Account Number Validation
# ============================================================

def validate_bank_account_number(value):
    if value is None:
        return

    value = str(value).strip()

    if not value:
        raise ValidationError(
            "Bank account number is required."
        )

    if not value.isdigit():
        raise ValidationError(
            "Bank account number must contain only digits."
        )

    if not BANK_ACCOUNT_PATTERN.fullmatch(value):
        raise ValidationError(
            "Bank account number must contain between "
            "9 and 18 digits."
        )

    if len(set(value)) == 1:
        raise ValidationError(
            "Enter a valid bank account number."
        )


# ============================================================
# Shop Name Validation
# ============================================================

def validate_shop_name(value):
    if value is None:
        return

    value = value.strip()

    if not value:
        raise ValidationError(
            "Shop name is required."
        )

    if len(value) < 2:
        raise ValidationError(
            "Shop name must contain at least 2 characters."
        )

    if len(value) > 150:
        raise ValidationError(
            "Shop name cannot exceed 150 characters."
        )

    if any(ord(character) < 32 for character in value):
        raise ValidationError(
            "Shop name contains invalid characters."
        )


# ============================================================
# Shop Description Validation
# ============================================================

def validate_shop_description(value):
    if value is None or value == "":
        return

    value = value.strip()

    if len(value) > 2000:
        raise ValidationError(
            "Shop description cannot exceed 2000 characters."
        )

    if any(ord(character) < 32 and character not in "\n\r\t"
           for character in value):
        raise ValidationError(
            "Shop description contains invalid characters."
        )


# ============================================================
# Bank Account Holder Name Validation
# ============================================================

def validate_bank_account_name(value):
    if value is None:
        return

    value = value.strip()

    if not value:
        raise ValidationError(
            "Bank account holder name is required."
        )

    if len(value) < 2:
        raise ValidationError(
            "Bank account holder name must contain at least 2 characters."
        )

    if len(value) > 100:
        raise ValidationError(
            "Bank account holder name cannot exceed 100 characters."
        )

    if not NAME_PATTERN.fullmatch(value):
        raise ValidationError(
            "Bank account holder name contains invalid characters."
        )