from django import forms
from django.core import validators

from .models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        label="Name",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }
        ),
        validators=[
            validators.RegexValidator(
                regex='^[A-Za-z ]{3,50}$', message="Must be valid...")
        ]
    )
    email = forms.CharField(
        label="Email",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }
        ),
        validators=[
            validators.RegexValidator(
                regex='^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', message="Must be valid...")
        ]
    )
    subject = forms.CharField(
        label="Subject",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Subject'
            }
        ),
        validators=[
            validators.RegexValidator(
                regex='^[A-Za-z]{3,30}$', message="Must be valid...")
        ]
    )
    message = forms.CharField(
        label='Message',
        max_length=500,
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Message',
                'cols': '30',
                'rows': '7',
            }
        )
    )

    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'subject',
            'message'
        ]
