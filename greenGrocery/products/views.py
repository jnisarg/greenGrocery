from django.shortcuts import render
from django.http import Http404

from carts.models import Cart
from .models import Product

from analytics.signals import object_viewed_signal

lst = ['Dragon Fruit', 'Papaya', 'Pineapple', 'Sugarcane']


def all_products(request, slug=None):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    query = request.GET.get('q')
    if query:
        qs = Product.objects.all().search(query)
    else:
        qs = Product.objects.all().order_by('?')
    dict = {
        'qs': qs,
        'btn': 'all_products',
        'lst': lst,
        'query': query,
        'cart': cart_obj
    }
    context = slug_fun(slug)
    if context:
        context.update(dict)
        return render(request, 'products/product_detail.html', context)
    return render(request, "products/index.html", dict)


def vegetables(request, slug=None):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    query = request.GET.get('q')
    if query:
        # Product.objects.vegetables().filter(title__icontains=query)
        qs = Product.objects.vegetables().search(query)
    else:
        qs = Product.objects.vegetables()
    dict = {
        'qs': qs,
        'btn': 'vegetables',
        'lst': lst,
        'query': query,
        'cart': cart_obj
    }
    context = slug_fun(slug)
    if context:
        context.update(dict)
        return render(request, 'products/product_detail.html', context)
    return render(request, "products/index.html", dict)


def fruits(request, slug=None):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    query = request.GET.get('q')
    if query:
        qs = Product.objects.fruits().search(query)
    else:
        qs = Product.objects.fruits()
    dict = {
        'qs': qs,
        'btn': 'fruits',
        'lst': lst,
        'query': query,
        'cart': cart_obj
    }
    context = slug_fun(slug)
    if context:
        context.update(dict)
        return render(request, 'products/product_detail.html', context)
    return render(request, "products/index.html", dict)


def featured(request, slug=None):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    query = request.GET.get('q')
    if query:
        qs = Product.objects.featured().search(query)
    else:
        qs = Product.objects.featured()
    dict = {
        'qs': qs,
        'btn': 'featured',
        'lst': lst,
        'query': query,
        'cart': cart_obj
    }
    context = slug_fun(slug)
    if context:
        context.update(dict)
        return render(request, 'products/product_detail.html', context)
    return render(request, "products/index.html", dict)


def sale(request, slug=None):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    query = request.GET.get('q')
    if query:
        qs = Product.objects.sale().search(query)
    else:
        qs = Product.objects.sale().order_by('-discount')
    dict = {
        'qs': qs,
        'btn': 'sale',
        'lst': lst,
        'query': query,
        'cart': cart_obj
    }
    context = slug_fun(slug)
    if context:
        context.update(dict)
        return render(request, 'products/product_detail.html', context)
    return render(request, "products/index.html", dict)


def slug_fun(slug):
    context = {}
    if slug != None:
        q = Product.objects.slug(slug)
        if q.exists():
            q = q.first()
        else:
            raise Http404('Not Found...')
        context = {
            'q': q
        }
    return context
