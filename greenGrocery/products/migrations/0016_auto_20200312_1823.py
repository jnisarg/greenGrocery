# Generated by Django 3.0.4 on 2020-03-12 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20200308_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=50, null=True, verbose_name='Title'),
        ),
    ]