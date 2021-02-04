from django.db import models
from greenGrocery.utils import unique_slug_generator
from products.models import Product
from django.db.models.signals import pre_save, post_save

# Create your models here.


class Tag(models.Model):
    title = models.CharField(
        "Title",
        max_length=50
    )
    slug = models.SlugField(
        "Slug",
        blank=True
    )
    timestamp = models.DateTimeField(
        "Time Stamp",
        auto_now_add=True
    )
    products = models.ManyToManyField(
        Product,
        blank=True
    )

    def __str__(self):
        return self.title


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_receiver, sender=Tag)
