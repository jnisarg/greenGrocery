from django import forms
from django.core import validators

from .models import Address


class AddressForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        validators=[
            validators.RegexValidator(
                regex='^[A-Za-z]{3,50}$', message="Must be valid...")
        ]
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        validators=[
            validators.RegexValidator(
                regex='^[A-Za-z]{3,50}$', message="Must be valid...")
        ]
    )
    address_line_1 = forms.CharField(
        label="Delivery Address",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'House number and street name',
            }
        ),
    )
    address_line_2 = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Appartment, suite, unit etc:',
            }
        ),
    )
    city = forms.CharField(
        label="City / Town",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'value': 'Ahmedabad'
            }
        ),
        validators=[
            validators.RegexValidator(
                regex='^[A-Za-z]{3,50}$', message="Must be valid...")
        ]
    )
    zip_code = forms.CharField(
        label="Postcode / ZIP",
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'onkeypress': 'return onlyNumberKey(event)'
        }),
        validators=[
            validators.RegexValidator(
                regex='^[3]\d{5}$', message="Must be valid...")
        ]
    )
    state = forms.CharField(
        label="State",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'value': 'Gujarat',
                # 'disabled': 'True'
            }
        ),
    )
    mobile = forms.CharField(
        label="Mobile",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'onkeypress': 'return onlyNumberKey(event)'
        }),
        validators=[
            validators.RegexValidator(
                regex='^[6-9]\d{9}$', message="Must be valid...")
        ]
    )

    class Meta():
        model = Address
        fields = [
            'first_name',
            'last_name',
            'address_line_1',
            'address_line_2',
            'city',
            'zip_code',
            'state',
            'mobile',
        ]
