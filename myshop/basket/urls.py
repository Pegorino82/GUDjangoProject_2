from django.urls import path

from basket import views

app_name = 'basketapp'

urlpatterns = [
    path('list/', views.ModelBasketList.as_view(), name='list'),

    path('basket/', views.basket, name='basket'),
    path('add_product/<int:pk>/', views.add_product, name='add_product'),
    path('add_product_ajax/<int:pk>/', views.add_product_ajax, name='add_product_ajax'),
    path('remove_product/<int:pk>/', views.remove_product, name='remove_product'),
    path('remove_product_ajax/<int:pk>/', views.remove_product_ajax, name='remove_product_ajax'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('delete_product_ajax/<int:pk>/', views.delete_product_ajax, name='delete_product_ajax'),
    path('edit/<int:pk>/<int:quantity>/', views.edit_basket, name='edit_basket'),
]
