from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    subject = models.CharField(max_length=70, default="")
    message = models.CharField(
        max_length=500, default="", null=True, blank=True)
    timestamp = models.DateTimeField(
        auto_now_add=True,
        # null=True
    )

    def __str__(self):
        return self.name
