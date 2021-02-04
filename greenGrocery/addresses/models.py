from django.db import models

from billing.models import BillingProfile

# Create your models here.


class Address(models.Model):
    billing_profile = models.ForeignKey(
        to=BillingProfile,
        on_delete=models.CASCADE
    )
    first_name = models.CharField(
        'First Name',
        max_length=50
    )
    last_name = models.CharField(
        'Last Name',
        max_length=50
    )
    address_line_1 = models.CharField(
        'Delivery Address',
        max_length=50
    )
    address_line_2 = models.CharField(
        '',
        max_length=50
    )
    city = models.CharField(
        'City / Town',
        max_length=50,
        default='Ahmedabad'
    )
    zip_code = models.CharField(
        'PostCode / Zip',
        max_length=6
    )
    state = models.CharField(
        'State',
        max_length=50,
        default='Gujarat'
    )
    mobile = models.CharField(
        'Mobile Number',
        max_length=10,
    )

    def __str__(self):
        return str(self.billing_profile)
