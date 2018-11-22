from django.urls import path

from basket import views

app_name = 'basketapp'

urlpatterns = [
    path('basket/', views.basket, name='basket'),
    path('add_product/<int:pk>/', views.add_product, name='add_product'),
    path('remove_product/<int:pk>/', views.remove_product, name='remove_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('edit/<int:pk>/<int:quantity>/', views.edit_basket, name='edit_basket'),
]
