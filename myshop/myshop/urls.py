"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

router = [
    path('categories/', include('products.endpoints.categories')),
    path('products/', include('products.endpoints.products')),
    path('basket/', include('basket.endpoints.basket')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myshopadmin/', include('myshopadmin.urls')),
    path('authors/', include('main.urls.authors')),
    path('articles/', include('main.urls.articles')),
    path('contacts/', include('contacts.urls')),
    path('products/', include('products.urls.products')),
    path('categories/', include('products.urls.categories')),
    path('customer/', include('customers.urls')),
    path('images/', include('images.urls')),
    path('basket/', include('basket.urls')),
    path('auth/', include('authapp.urls')),
    path('auth/oauth2/', include('social_django.urls')),
    path('api/', include(router)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
