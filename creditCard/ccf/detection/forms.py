from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.models import User
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class AccountDetailsForm(forms.ModelForm):

    class Meta:
        model = AccountDetails
        fields = [
            'gender',
            'birth_date',
            'picture'
        ]


class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = [
            'street_address',
            'city',
            'postal_code',
            'country'
        ]
