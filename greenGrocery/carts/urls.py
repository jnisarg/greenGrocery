from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('update/', views.cart_update, name='update'),
    path('remove_in_cart/', views.in_cart_remove, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('api/', views.cart_api, name='api')
]
