# Generated by Django 3.0.4 on 2020-04-06 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0022_auto_20200406_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='item_cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.Cart'),
        ),
    ]