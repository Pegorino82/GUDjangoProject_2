from django.urls import path

from products.views import (
    category,
    CategoryListOfView,
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    CategoryDetailView
)

app_name = 'categoriesapp'

urlpatterns = [
    # path('category/<str:category>/', category, name='category'),
    path('category/<int:pk>/', CategoryListOfView.as_view(), name='category'),  # все продукты категории
    path('create/', CategoryCreateView.as_view(), name='create'),
    path('list/', CategoryListView.as_view(), name='list'),
    path('update/<int:pk>/', CategoryUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/', CategoryDetailView.as_view(), name='detail'),  # детальное представление категории
]
