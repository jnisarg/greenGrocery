# Generated by Django 3.0.4 on 2020-04-06 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0020_auto_20200406_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]