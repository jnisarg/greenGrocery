from django.db import models
from django.db.models.signals import pre_save, post_save

from greenGrocery.utils import unique_order_id_generator
from carts.models import Cart
from billing.models import BillingProfile
from addresses.models import Address

# Create your models here.

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('delivered', "Delivered")
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
            obj.update_total()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile, cart=cart_obj)
            obj.update_total()
            created = True
        return obj, created


class Order(models.Model):
    billing_profile = models.ForeignKey(
        to=BillingProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    order_id = models.CharField(
        max_length=120,
        blank=True
    )
    delivery_address = models.ForeignKey(
        to=Address,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    cart = models.ForeignKey(
        to=Cart,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=120,
        default='created',
        choices=ORDER_STATUS_CHOICES
    )
    # delivery_total = models.DecimalField(
    #     default=0,  # change in future if wanted, the default value given now is 0
    #     max_digits=100,
    #     decimal_places=2
    # )
    total = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=2
    )
    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        self.total = cart_total
        self.save()
        return cart_total

    def check_done(self):
        billing_profile = self.billing_profile
        delivery_address = self.delivery_address
        total = self.total
        if billing_profile and delivery_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status

    objects = OrderManager()


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(
        billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
