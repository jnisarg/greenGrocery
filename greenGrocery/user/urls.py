from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('register/guest', views.guest_register_view, name='guest_register'),
    path('logout/', views.logoutView, name='logout')
]
