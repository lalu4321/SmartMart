from django.utils.text import slugify
from .models import Product


def generate_unique_slug(name, instance=None):

    slug = slugify(name)

    unique_slug = slug

    counter = 1

    while Product.objects.filter(
        slug=unique_slug
    ).exclude(
        pk=instance.pk if instance else None
    ).exists():

        unique_slug = f"{slug}-{counter}"

        counter += 1

    return unique_slug