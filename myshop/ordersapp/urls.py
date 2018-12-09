from django.urls import path

from ordersapp import views

app_name = 'ordersapp'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('', views.OrderListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.OrderDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', views.OrderUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.OrderDeleteView.as_view(), name='delete'),
]
