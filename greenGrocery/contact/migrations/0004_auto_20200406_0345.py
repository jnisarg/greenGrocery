# Generated by Django 3.0.4 on 2020-04-05 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_auto_20200406_0342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]
