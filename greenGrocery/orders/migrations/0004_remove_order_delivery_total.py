# Generated by Django 3.0.4 on 2020-03-13 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20200313_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_total',
        ),
    ]