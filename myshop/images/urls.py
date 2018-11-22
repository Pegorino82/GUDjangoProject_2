from django.urls import path

from images import views

app_name = 'imagesapp'

urlpatterns = [
    path('list_image/', views.list_image, name='list_image'),
    path('create_image/', views.create_image, name='create_image'),
    path('update_image/<int:pk>/', views.update_image, name='update_image'),
    path('detail_image/<int:pk>/', views.detail_image, name='detail_image'),
    path('delete_image/<int:pk>/', views.delete_image, name='delete_image'),
]