from django.shortcuts import render, redirect
from django.http import JsonResponse
from decimal import Decimal

from .models import Cart, CartItem
from orders.models import Order
from products.models import Product
from billing.models import BillingProfile
from user.forms import GuestForm
from user.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address

from django.contrib import messages

# Create your views here.


def cart_api(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{"image": x.image.url, "title": x.title, "price": x.price}
                for x in cart_obj.products.all()]
    return JsonResponse({
        "products": products,
        "subtotal": cart_obj.subtotal,
        "discount_amount": cart_obj.discount_amount,
        "total": cart_obj.total
    })


def cart(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    discount = f'{0:.2f}'
    cart_obj.discount_amount = discount
    cart_obj.save()
    quantity_dict = {}
    for product in cart_obj.products.all():
        quantity = CartItem.objects.get(
            item=product, item_cart=cart_obj).quantity
        quantity_dict[product] = quantity
    if request.POST:
        coupon = request.POST.get('coupon').lower()
        discount_response = cart_obj.update_discount_total(coupon)
        if discount_response == 'success':
            messages.success(
                request, f'Coupon applied successfully. You have saved ₹{cart_obj.discount_amount} on your cart.')
        else:
            messages.error(request, 'Invalid coupon or cart value')
    my_dict = {
        'cart': cart_obj,
        'quantity': quantity_dict
    }
    return render(request, 'carts/cart.html', my_dict)


def cart_update(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))
    product_obj = Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    item, created = CartItem.objects.get_or_create(
        item=product_obj, item_cart=cart_obj)
    if quantity not in range(1, 11):
        pass
    if product_obj in cart_obj.products.all():
        qs = CartItem.objects.get(
            item=product_obj, item_cart=cart_obj)
        actual_quantity = qs.quantity
        if quantity < actual_quantity and quantity != 0:
            request.session['quantity'] = quantity
            CartItem.objects.filter(item=product_obj, item_cart=cart_obj).update(
                quantity=quantity)
        else:
            item.delete()
            request.session['quantity'] = 1
            cart_obj.products.remove(product_obj)
            product_added = False
    else:
        if quantity > 0:
            CartItem.objects.filter(item=product_obj, item_cart=cart_obj).update(
                quantity=quantity)
            request.session['quantity'] = quantity
            cart_obj.products.add(product_obj)
            product_added = True
    request.session['cart_items_total'] = cart_obj.products.count()
    if request.is_ajax():
        # print("Ajax Request")
        json_data = {
            "added": product_added,
            "removed": not product_added,
            "cartItemCount": cart_obj.products.count()
        }
        return JsonResponse(json_data)
    return redirect(product_obj.get_absolute_url())


def in_cart_remove(request):
    product_id = request.POST.get('product_id')
    product_obj = Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    item, created = CartItem.objects.get_or_create(
        item=product_obj, item_cart=cart_obj)
    if product_obj in cart_obj.products.all():
        item.delete()
        request.session['quantity'] = 1
        cart_obj.products.remove(product_obj)
    request.session['cart_items_total'] = cart_obj.products.count()
    return redirect('carts:cart')


def success(request):
    return render(request, "carts/success.html")


def checkout(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('carts:cart')
    guest_form = GuestForm()
    address_form = AddressForm(request.POST or None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request)
    if address_form.is_valid():
        instance = address_form.save(commit=False)
        instance.billing_profile = billing_profile
        instance.save()
        request.session['delivery_address_id'] = instance.id
    delivery_address_id = request.session.get('delivery_address_id', None)
    address_qs = None
    if billing_profile is not None:
        address_qs = Address.objects.filter(billing_profile=billing_profile)
        if address_qs.count() >= 1:
            address_qs = address_qs.first()
        order_obj, order_obj_created = Order.objects.new_or_get(
            billing_profile, cart_obj)
        if delivery_address_id:
            order_obj.delivery_address = Address.objects.get(
                id=delivery_address_id)
            del request.session['delivery_address_id']
            order_obj.save()
    if request.method == 'POST':
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items_total'] = 0
            del request.session['cart_id']
            return redirect('carts:success')
    my_dict = {
        'order': order_obj,
        'cart': cart_obj,
        'billing_profile': billing_profile,
        'address_form': address_form,
        'address_qs': address_qs,
    }
    return render(request, 'carts/checkout.html', my_dict)
