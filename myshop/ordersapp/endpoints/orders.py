from django.urls import path

from ordersapp.api.orders import OrderCreateView

app_name = 'rest_ordersapp'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='rest_create_order'),
]
