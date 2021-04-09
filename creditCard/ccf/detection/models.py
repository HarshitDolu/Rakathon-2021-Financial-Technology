from django.db import models
from django.utils.translation import gettext as _
# Create your models here.
from django.contrib.auth.models import  User
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)

from django.urls import reverse

# Account details
class AccountDetails(models.Model):
    GENDER_CHOICE = (
        ("M", "Male"),
        ("F", "Female"),
    )
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    account_no = models.PositiveIntegerField(
        unique=True,
        validators=[
            MinValueValidator(10000000),
            MaxValueValidator(99999999)
        ]
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    picture = models.ImageField(
        null=True,
        blank=True,
        upload_to='account_pictures/',
    )

    def __str__(self):
        return str(self.account_no)

# user address

class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address',
        on_delete=models.CASCADE,
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.user.email


from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

class Payment(models.Model):
    acc=models.OneToOneField(AccountDetails,
                        related_name='card',
        on_delete=models.CASCADE)

    cc_number = CardNumberField(_('card number'))
    cc_expiry = CardExpiryField(_('expiration date'))
    cc_code = SecurityCodeField(_('security code'))

    def __str__(self):
        return self.cc_number
