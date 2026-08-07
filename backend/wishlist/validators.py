from django.core.exceptions import ValidationError


# ==========================================================
# Wishlist Product
# ==========================================================

def validate_product(product):

    if product is None:

        raise ValidationError(
            "Product is required."
        )

    if not product.is_active:

        raise ValidationError(
            "Inactive product cannot be added to wishlist."
        )