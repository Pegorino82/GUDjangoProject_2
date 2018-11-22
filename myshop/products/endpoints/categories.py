from django.urls import path

from products.api import rest_category_list, rest_category_detail

app_name = 'rest_categories'

urlpatterns = [
    path('list/', rest_category_list, name='rest_list'),
    path('detail/<int:pk>/', rest_category_detail, name='rest_detail'),
]