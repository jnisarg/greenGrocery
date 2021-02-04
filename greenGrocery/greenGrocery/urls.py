"""greenGrocery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from . import views
from user import urls as user_urls
from products import urls as product_urls
from carts import urls as cart_urls
from billing import urls as billing_urls
from contact import urls as contact_urls

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('subscription', views.subscription, name='subscription'),
    path('admin/', admin.site.urls),
    path('', include(user_urls)),
    path('products/', include(product_urls)),
    path('cart/', include(cart_urls)),
    path('billing/', include(billing_urls)),
    path('contact/', include(contact_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
