from django.urls import path

from main.views import (
    list_author,
    create_author_model_form,
    update_author_model_form,
    detail_author,
    delete_author
)

app_name = 'authorsapp'

urlpatterns = [
    path('list/', list_author, name='list'),
    path('create/', create_author_model_form, name='create'),
    path('detail/<int:pk>/', detail_author, name='detail'),
    path('update/<int:pk>/', update_author_model_form, name='update'),
    path('delete/<int:pk>/', delete_author, name='delete'),
]
