# Generated by Django 3.0.4 on 2020-03-27 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_delete_userprofileinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=10, verbose_name='Mobile Number')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'verbose_name': 'User Profile Info',
                'verbose_name_plural': 'Profile Info for Users',
            },
        ),
    ]
