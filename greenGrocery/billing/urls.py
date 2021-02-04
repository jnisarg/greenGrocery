from django.urls import path

from .views import payment_method_view

app_name = 'billing'

urlpatterns = [
    path('payment-method', payment_method_view, name='payment-method')
]
