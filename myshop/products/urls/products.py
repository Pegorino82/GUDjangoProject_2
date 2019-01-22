from django.urls import path
from django.views.decorators.cache import cache_page

from products.views import (
    # catalog,
    # product,
    Catalog,
    ProductCreateView,
    ProductListView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,
)

app_name = 'productsapp'

urlpatterns = [
    # path('catalog/', catalog, name='catalog'),
    # path('product/<str:category>/<int:pk>/', product, name='product'), # старая реализвция, тут не используется
    path('catalog/', cache_page(3600)(Catalog.as_view()), name='catalog'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('list/', ProductListView.as_view(), name='list'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
]
