from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from .validators import (
    validate_category_description,
    validate_category_image,
    validate_category_name,
)


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[validate_category_name],
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        db_index=True,
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
        validators=[validate_category_description],
    )

    image = models.ImageField(
        upload_to="category_images/",
        blank=True,
        null=True,
        validators=[validate_category_image],
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
        verbose_name = "Category"
        verbose_name_plural = "Categories"
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

        if self.parent and self.parent == self:
            raise ValidationError(
                {
                    "parent": "A category cannot be its own parent."
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1

            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name