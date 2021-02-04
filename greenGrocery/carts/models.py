from django.db import models

from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.contrib.auth.models import User

# Create your models here.

# User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            cart_obj = qs.first()
            new_obj = False
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    products = models.ManyToManyField(
        to=Product,
        blank=True
    )
    subtotal = models.DecimalField(
        default=0.00,
        max_digits=100,
        decimal_places=2
    )
    discount_amount = models.DecimalField(
        'Discount Amount',
        default=0.00,
        max_digits=100,
        decimal_places=2
    )
    total = models.DecimalField(
        default=0.00,
        max_digits=100,
        decimal_places=2
    )
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    def update_discount_total(self, coupon):
        if coupon == 'green' and self.subtotal >= 150:
            discount = float(self.subtotal) * 0.5
            if discount > 100:
                discount = 100
            self.discount_amount = discount
            self.save()
            return 'success'
        else:
            return 'error'


def cart_m2m_changed_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            if x.on_sale:
                x.price = x.discounted_price * CartItem.objects.get(
                    item=x, item_cart=instance.id).quantity
            total += x.price * CartItem.objects.get(
                item=x, item_cart=instance.id).quantity
        instance.subtotal = total
        instance.save()


m2m_changed.connect(cart_m2m_changed_receiver, sender=Cart.products.through)


def cart_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal < 100:
        instance.total = instance.subtotal + 20
    else:
        instance.total = instance.subtotal

    instance.total = float(instance.total) - float(instance.discount_amount)


pre_save.connect(cart_pre_save_receiver, sender=Cart)


class CartItem(models.Model):
    item = models.OneToOneField(
        to=Product,
        on_delete=models.CASCADE
    )
    item_cart = models.ForeignKey(
        to=Cart,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        default=1,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.item_cart)
