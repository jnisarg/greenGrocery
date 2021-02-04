import os
import random
from django.db import models
from django.db.models import Q
from greenGrocery.utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

# Create your models here.


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(filepath)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 100000000)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f"products/{new_filename}/{final_filename}"


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class ProductQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query) | Q(
            price__iexact=query) | Q(tag__title__icontains=query)
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def slug(self, slug):
        return self.get_queryset().filter(slug=slug)

    def featured(self):
        return self.get_queryset().filter(is_featured=True)

    def sale(self):
        return self.get_queryset().filter(on_sale=True)

    def vegetables(self):
        return self.get_queryset().filter(product_type='V')

    def fruits(self):
        return self.get_queryset().filter(product_type='F')

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().search(query)


class Product(models.Model):
    PRODUCT_TYPES = [
        ('V', 'Vegetable'),
        ('F', 'Fruit')
    ]
    product_type = models.CharField(
        max_length=1,
        choices=PRODUCT_TYPES,
        default='V'
    )
    title = models.CharField(
        "Title",
        max_length=50,
        null=True
    )
    slug = models.SlugField(
        blank=True
    )
    description = models.TextField(
        "Description",
        max_length=500
    )
    price = models.DecimalField(
        "Price",
        decimal_places=2,
        max_digits=5
    )
    image = models.ImageField(
        "Image",
        upload_to=upload_image_path,
        null=True,
        blank=False
    )
    is_featured = models.BooleanField(
        "Featured",
        default=False
    )
    on_sale = models.BooleanField(
        "On Sale",
        default=False
    )
    discount = IntegerRangeField(
        "Discount for Sale",
        null=True,
        blank=True,
        min_value=10,
        max_value=60
    )
    discounted_price = models.DecimalField(
        "Price after discount",
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True
    )

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('products:products', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if instance.on_sale:
        instance.discounted_price = instance.price - \
            ((instance.price * instance.discount) / 100)


pre_save.connect(product_pre_save_receiver, sender=Product)
