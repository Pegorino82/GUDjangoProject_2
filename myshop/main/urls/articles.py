from django.urls import path

from main.views import (
list_article,
create_article,
update_article,
detail_article,
delete_article
)

app_name = 'articlesapp'

urlpatterns = [
    path('list/', list_article, name='list'),
    path('create/', create_article, name='create'),
    path('update/<int:pk>/', update_article, name='update'),
    path('detail/<int:pk>/', detail_article, name='detail'),
    path('delete/<int:pk>/', delete_article, name='delete'),

]
