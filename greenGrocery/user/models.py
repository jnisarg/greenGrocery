from django.db import models
from django.contrib.auth.models import User


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(
        default=True
    )
    update = models.DateTimeField(
        auto_now=True
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.email


class UserProfileInfo(models.Model):

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    mobile = models.CharField(
        "Mobile Number",
        max_length=10,
    )

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta():
        verbose_name = "User Profile Info"
        verbose_name_plural = "Profile Info for Users"
