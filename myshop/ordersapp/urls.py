from django.urls import path

from ordersapp import views

app_name = 'ordersapp'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('create/', views.OrderCreateView.as_view(), name='create'),
]
