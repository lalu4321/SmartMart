from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SELLER = "SELLER", "Seller"
        CUSTOMER = "CUSTOMER", "Customer"

    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=15,
        unique=True
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

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
        related_name="addresses"
    )

    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    address_line1 = models.CharField(max_length=255)

    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    landmark = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    city = models.CharField(max_length=100)

    district = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    country = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    address_type = models.CharField(
        max_length=10,
        choices=AddressType.choices,
        default=AddressType.HOME
    )

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.city}"
    
class SellerProfile(models.Model):

    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="seller_profile"
    )

    shop_name = models.CharField(max_length=150)

    shop_logo = models.ImageField(
        upload_to="shop_logos/",
        blank=True,
        null=True
    )

    shop_description = models.TextField(
        blank=True,
        null=True
    )

    gst_number = models.CharField(
        max_length=20,
        unique=True
    )

    bank_account_name = models.CharField(max_length=100)

    bank_account_number = models.CharField(max_length=30)

    ifsc_code = models.CharField(max_length=20)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop_name
    

    