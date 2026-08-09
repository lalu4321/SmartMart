from django.core.exceptions import ValidationError


# ==========================================================
# Contact Name Validator
# ==========================================================

def validate_name(value):

    if not value:

        raise ValidationError(
            "Name is required."
        )

    value = value.strip()

    if len(value) < 3:

        raise ValidationError(
            "Name must contain at least 3 characters."
        )

    if len(value) > 100:

        raise ValidationError(
            "Name cannot exceed 100 characters."
        )


# ==========================================================
# Subject Validator
# ==========================================================

def validate_subject(value):

    if not value:

        raise ValidationError(
            "Subject is required."
        )

    value = value.strip()

    if len(value) < 3:

        raise ValidationError(
            "Subject must contain at least 3 characters."
        )

    if len(value) > 255:

        raise ValidationError(
            "Subject cannot exceed 255 characters."
        )


# ==========================================================
# Message Validator
# ==========================================================

def validate_message(value):

    if not value:

        raise ValidationError(
            "Message is required."
        )

    value = value.strip()

    if len(value) < 10:

        raise ValidationError(
            "Message must contain at least 10 characters."
        )

    if len(value) > 5000:

        raise ValidationError(
            "Message cannot exceed 5000 characters."
        )