from django.urls import path

from products.api import (
    rest_product_list,
    rest_product_detail,
    rest_product_create,
    rest_product_update,
    rest_product_delete,
    rest_basket_json,
)

app_name = 'rest_products'

urlpatterns = [
    path('list/', rest_product_list, name='rest_list'),
    path('detail/<int:pk>/', rest_product_detail, name='rest_detail'),
    path('create/', rest_product_create, name='rest_create'),
    path('update/<int:pk>/', rest_product_update, name='rest_update'),
    path('delete/<int:pk>/', rest_product_delete, name='rest_delete'),

    path('basket/', rest_basket_json, name='rest_basket'),
]
