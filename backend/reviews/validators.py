from django.core.exceptions import ValidationError


# ==========================================================
# Rating
# ==========================================================

def validate_rating(value):

    if value is None:

        raise ValidationError(
            "Rating is required."
        )

    if value < 1 or value > 5:

        raise ValidationError(
            "Rating must be between 1 and 5."
        )


# ==========================================================
# Review
# ==========================================================

def validate_review(value):

    if value is None:

        raise ValidationError(
            "Review is required."
        )

    value = value.strip()

    if len(value) < 5:

        raise ValidationError(
            "Review must contain at least 5 characters."
        )

    if len(value) > 1000:

        raise ValidationError(
            "Review cannot exceed 1000 characters."
        )