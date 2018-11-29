from django.urls import path

from customers import views

app_name = 'customersapp'

urlpatterns = [
    path('', views.login_view, name='customer'),
    path('create/', views.create_customer, name='create_customer'),
    path('update/<int:pk>/', views.update_customer, name='update_customer'),
    path('edit_profile/<int:pk>/', views.edit_profile, name='edit_profile'),
    path('detail/<int:pk>/', views.detail_customer, name='detail_customer'),
    path('delete/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('list/', views.list_customer, name='list_customer'),
]
