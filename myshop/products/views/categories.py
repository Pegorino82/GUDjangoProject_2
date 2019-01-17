from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from customers.mixins import AdminGroupRequired
from products.models import Category, Product
from products.forms import CategoryModelForm


class CategoryCreateView(LoginRequiredMixin, AdminGroupRequired, CreateView):
    model = Category
    template_name = 'products/create_category.html'
    form_class = CategoryModelForm
    success_url = reverse_lazy('categoriesapp:list')
    login_url = reverse_lazy('authapp:login_view')
    redirect_url = reverse_lazy('categoriesapp:list')
    extra_context = {'title': 'Category Create'}


# показывает товары конкретной категории
class CategoryListOfView(DetailView):
    model = Category
    template_name = 'products/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(category=self.object.pk, is_active=True).order_by('-pk').select_related(
            'image', 'product_marker')
        products_paginator = Paginator(products, 4)
        products_page = self.request.GET.get('page')
        products_items = products_paginator.get_page(products_page)
        context.update({'title': f'{self.object} products'})
        context.update({'products': products_items})
        context.update({'pagination_url': reverse_lazy('categoriesapp:category', kwargs={'pk': self.object.pk})})
        return context


# пагинация реализована на js
class CategoryListView(ListView):
    model = Category
    template_name = 'products/list_category.html'

    # paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Category List'
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'products/detail_category.html'
    extra_context = {'title': 'Category Detail'}


class CategoryUpdateView(AdminGroupRequired, UpdateView):
    model = Category
    redirect_url = reverse_lazy('categoriesapp:list')
    template_name = 'products/update_category.html'
    form_class = CategoryModelForm
    success_url = reverse_lazy('categoriesapp:list')
    extra_context = {'title': 'Category Detail'}


# not used
class CategoryDeleteView(AdminGroupRequired, DeleteView):
    model = Category
    redirect_url = reverse_lazy('categoriesapp:list')
    template_name = 'products/delete.html'
    success_url = reverse_lazy('categoriesapp:list')

    def test_func(self):
        # функция для UserPassesTestMixin
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            self.object = self.queryset.get(pk=pk)
            self.object.is_active = False
            self.object.save()
        except Exception as err:
            print('exception%' * 20)
            print(err)
            print('exception%' * 20)
            pass

        return redirect(self.success_url)


def category(request, category):
    category_id = Category.objects.get(name=category).id
    products = Product.objects.filter(category=category_id, is_active=True).order_by('-id')
    products_paginator = Paginator(products, 4)
    products_page = request.GET.get('page')
    products_items = products_paginator.get_page(products_page)

    result = {
        'category': category,
        'products': products_items,
        'categories': Category.objects.all()
    }

    return render(request,
                  'products/category.html',
                  result
                  )
