from django.urls import path

from customers import views

app_name = 'customersapp'

urlpatterns = [
    # path('', views.login_view, name='customer'),
    # path('create/', views.create_customer, name='create_customer'),  # надо переделать адрес и шаблон на login
    # path('update/<int:pk>/', views.update_customer, name='update_customer'),
    # path('detail/<int:pk>/', views.detail_customer, name='detail_customer'),
    # path('delete/<int:pk>/', views.delete_customer, name='delete_customer'),
    # path('list/', views.list_customer, name='list_customer'),

    path('create/', views.CustomerCreateView.as_view(), name='create'),
    path('list/', views.CustomerListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.CustomerDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', views.CustomerUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.CustomerDeleteView.as_view(), name='delete'),
    path('edit_profile/<int:pk>/', views.edit_profile, name='edit_profile'),
]
