from django.core.exceptions import ValidationError


# ==========================================================
# Notification Title Validator
# ==========================================================

def validate_title(value):

    if not value:

        raise ValidationError(
            "Title is required."
        )

    value = value.strip()

    if len(value) < 3:

        raise ValidationError(
            "Title must contain at least 3 characters."
        )

    if len(value) > 255:

        raise ValidationError(
            "Title cannot exceed 255 characters."
        )


# ==========================================================
# Notification Message Validator
# ==========================================================

def validate_message(value):

    if not value:

        raise ValidationError(
            "Message is required."
        )

    value = value.strip()

    if len(value) < 5:

        raise ValidationError(
            "Message must contain at least 5 characters."
        )

    if len(value) > 5000:

        raise ValidationError(
            "Message cannot exceed 5000 characters."
        )