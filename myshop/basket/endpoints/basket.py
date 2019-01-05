from django.urls import path

from basket.api import rest_basket_detail, rest_basket_list, rest_basket_update, rest_basket_delete

app_name = 'rest_basket'

urlpatterns = [
    path('detail/', rest_basket_detail, name='rest_detail'),
    path('list/', rest_basket_list, name='rest_list'),
    path('update/', rest_basket_update, name='rest_update'),
    path('delete/', rest_basket_delete, name='rest_delete'),
    ]