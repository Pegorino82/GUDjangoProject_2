from django.urls import path

from main.views import (
    list_article,
    create_article,
    update_article,
    detail_article,
    delete_article,

    # generic views:
    CreateArticleView,
    ListArticleView,
    DetailArticleView,
    UpdateArticleView,
    DeleteArticleView,
)

app_name = 'articlesapp'

urlpatterns = [
    # path('list/', list_article, name='list'),
    # path('create/', create_article, name='create'),
    # path('update/<int:pk>/', update_article, name='update'),
    # path('detail/<int:pk>/', detail_article, name='detail'),
    # path('delete/<int:pk>/', delete_article, name='delete'),

    # generic views:
    path('create/', CreateArticleView.as_view(), name='create'),
    path('list/', ListArticleView.as_view(), name='list'),
    path('detail/<int:pk>/', DetailArticleView.as_view(), name='detail'),
    path('update/<int:pk>/', UpdateArticleView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteArticleView.as_view(), name='delete'),
]
