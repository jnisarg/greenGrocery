from django.urls import path
from .import views

app_name = 'products'

urlpatterns = [
    path('', views.all_products, name='products'),
    path('vegetables/', views.vegetables, name='vegetables'),
    path('fruits/', views.fruits, name='fruits'),
    path('featured/', views.featured, name='featured'),
    path('sale/', views.sale, name='sale'),

    path('<slug:slug>/', views.all_products, name='products'),
    path('vegetables/<slug:slug>/', views.vegetables, name='vegetables'),
    path('fruits/<slug:slug>/', views.fruits, name='fruits'),
    path('featured/<slug:slug>/', views.featured, name='featured'),
    path('sale/<slug:slug>/', views.sale, name='sale'),
]
