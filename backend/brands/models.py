from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from .validators import (
    validate_brand_description,
    validate_brand_logo,
    validate_brand_name,
    validate_brand_website,
)


class Brand(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[validate_brand_name],
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        db_index=True,
    )

    logo = models.ImageField(
        upload_to="brand_logos/",
        blank=True,
        null=True,
        validators=[validate_brand_logo],
    )

    description = models.TextField(
        blank=True,
        null=True,
        validators=[validate_brand_description],
    )

    website = models.URLField(
        blank=True,
        null=True,
        validators=[validate_brand_website],
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
        ]

    def clean(self):
        super().clean()

        if self.name:
            self.name = self.name.strip()

        if self.description:
            self.description = self.description.strip()

        if self.website:
            self.website = self.website.strip()

    def save(self, *args, **kwargs):

        self.full_clean()

        if not self.slug:

            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Brand.objects.filter(
                slug=slug
            ).exclude(
                pk=self.pk
            ).exists():

                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name