# Generated by Django 3.0.4 on 2020-03-23 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0005_auto_20200318_1639'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_Name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_Name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('address_line_1', models.CharField(max_length=50, verbose_name='Street Address')),
                ('address_line_2', models.CharField(max_length=50, verbose_name='')),
                ('city', models.CharField(default='Ahmedabad', max_length=50, verbose_name='City / Town')),
                ('zip_code', models.CharField(max_length=6, verbose_name='PostCode / Zip')),
                ('state', models.CharField(default='Gujarat', max_length=50, verbose_name='State')),
                ('mobile', models.CharField(max_length=10, verbose_name='Mobile Number')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.BillingProfile')),
            ],
        ),
    ]
