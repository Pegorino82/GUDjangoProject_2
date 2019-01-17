from django.urls import path

from main.views import (
    list_author,
    create_author_model_form,
    update_author_model_form,
    detail_author,
    delete_author,

    # generic views:
    CreateAuthorView,
    ListAuthorView,
    DetailAuthorView,
    UpdateAuthorView,
    DeleteAuthorView,
)

app_name = 'authorsapp'

urlpatterns = [
    # path('list/', list_author, name='list'),
    # path('create/', create_author_model_form, name='create'),
    # path('detail/<int:pk>/', detail_author, name='detail'),
    # path('update/<int:pk>/', update_author_model_form, name='update'),
    # path('delete/<int:pk>/', delete_author, name='delete'),

    # generic views:
    path('list/', ListAuthorView.as_view(), name='list'),
    path('create/', CreateAuthorView.as_view(), name='create'),
    path('detail/<int:pk>/', DetailAuthorView.as_view(), name='detail'),
    path('update/<int:pk>/', UpdateAuthorView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteAuthorView.as_view(), name='delete'),
]
