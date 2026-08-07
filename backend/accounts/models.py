from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from .validators import (
    validate_account_email,
    validate_address_text,
    validate_bank_account_name,
    validate_bank_account_number,
    validate_date_of_birth,
    validate_gst_number,
    validate_ifsc_code,
    validate_image,
    validate_location_name,
    validate_name,
    validate_phone,
    validate_pincode,
    validate_shop_description,
    validate_shop_name,
    validate_username,
)


class Account(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SELLER = "SELLER", "Seller"
        CUSTOMER = "CUSTOMER", "Customer"

    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    email = models.EmailField(
        unique=True,
        validators=[validate_account_email],
    )

    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_phone],
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CUSTOMER,
        db_index=True,
    )

    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
        validators=[validate_image],
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        validators=[validate_date_of_birth],
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        blank=True,
        null=True,
        db_index=True,
    )

    is_verified = models.BooleanField(
        default=False,
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
        ordering = ["-created_at"]
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["role"]),
            models.Index(fields=["is_verified"]),
        ]

    def clean(self):
        super().clean()

        if self.email:
            self.email = self.email.strip().lower()

        if self.username:
            self.username = self.username.strip()
            validate_username(self.username)

        if self.first_name:
            self.first_name = self.first_name.strip()
            validate_name(self.first_name)

        if self.last_name:
            self.last_name = self.last_name.strip()
            validate_name(self.last_name)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Address(models.Model):

    class AddressType(models.TextChoices):
        HOME = "HOME", "Home"
        OFFICE = "OFFICE", "Office"
        OTHER = "OTHER", "Other"

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    full_name = models.CharField(
        max_length=100,
        validators=[validate_name],
    )

    phone = models.CharField(
        max_length=15,
        validators=[validate_phone],
    )

    address_line1 = models.CharField(
        max_length=255,
        validators=[validate_address_text],
    )

    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_address_text],
    )

    landmark = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_address_text],
    )

    city = models.CharField(
        max_length=100,
        validators=[validate_location_name],
    )

    district = models.CharField(
        max_length=100,
        validators=[validate_location_name],
    )

    state = models.CharField(
        max_length=100,
        validators=[validate_location_name],
    )

    country = models.CharField(
        max_length=100,
        validators=[validate_location_name],
    )

    pincode = models.CharField(
        max_length=10,
        validators=[validate_pincode],
    )

    address_type = models.CharField(
        max_length=10,
        choices=AddressType.choices,
        default=AddressType.HOME,
    )

    is_default = models.BooleanField(
        default=False,
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
        ordering = ["-created_at"]
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        indexes = [
            models.Index(fields=["account"]),
            models.Index(fields=["city"]),
            models.Index(fields=["state"]),
            models.Index(fields=["pincode"]),
            models.Index(fields=["is_default"]),
        ]

    def clean(self):
        super().clean()

        if self.full_name:
            self.full_name = self.full_name.strip()

        if self.city:
            self.city = self.city.strip().title()

        if self.district:
            self.district = self.district.strip().title()

        if self.state:
            self.state = self.state.strip().title()

        if self.country:
            self.country = self.country.strip().title()

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.is_default:
            Address.objects.filter(
                account=self.account,
                is_default=True,
            ).exclude(
                pk=self.pk
            ).update(
                is_default=False
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.city}"

class SellerProfile(models.Model):

    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="seller_profile",
    )

    shop_name = models.CharField(
        max_length=150,
        validators=[validate_shop_name],
    )

    shop_logo = models.ImageField(
        upload_to="shop_logos/",
        blank=True,
        null=True,
        validators=[validate_image],
    )

    shop_description = models.TextField(
        blank=True,
        null=True,
        validators=[validate_shop_description],
    )

    gst_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_gst_number],
    )

    bank_account_name = models.CharField(
        max_length=100,
        validators=[validate_bank_account_name],
    )

    bank_account_number = models.CharField(
        max_length=30,
        validators=[validate_bank_account_number],
    )

    ifsc_code = models.CharField(
        max_length=20,
        validators=[validate_ifsc_code],
    )

    is_verified = models.BooleanField(
        default=False,
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
        ordering = ["-created_at"]
        verbose_name = "Seller Profile"
        verbose_name_plural = "Seller Profiles"
        indexes = [
            models.Index(fields=["account"]),
            models.Index(fields=["shop_name"]),
            models.Index(fields=["gst_number"]),
            models.Index(fields=["is_verified"]),
        ]

    def clean(self):
        super().clean()

        if self.shop_name:
            self.shop_name = self.shop_name.strip()

        if self.shop_description:
            self.shop_description = self.shop_description.strip()

        if self.gst_number:
            self.gst_number = self.gst_number.strip().upper()

        if self.ifsc_code:
            self.ifsc_code = self.ifsc_code.strip().upper()

        if self.bank_account_name:
            self.bank_account_name = self.bank_account_name.strip()

        if self.bank_account_number:
            self.bank_account_number = (
                self.bank_account_number.strip()
            )

        if (
            self.account
            and self.account.role != Account.Role.SELLER
        ):
            raise ValidationError(
                {
                    "account": (
                        "Only users with the SELLER role "
                        "can have a seller profile."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.shop_name  