from django.shortcuts import render
from django.core.paginator import Paginator

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from customers.mixins import AdminGroupRequired
from products.models import Category, Product
from products.forms import CategoryModelForm


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


class ModelCreateCategory(AdminGroupRequired, CreateView):
    model = Category
    redirect_url = reverse_lazy('categoriesapp:list')
    template_name = 'products/create.html'
    form_class = CategoryModelForm
    success_url = reverse_lazy('categoriesapp:list')


class ModelListCategoriy(ListView):
    model = Category
    template_name = 'products/categories_list.html'
    context_object_name = 'results'
    # paginate_by = 3 # в этом случае в шаблоне обращаемся к контекстной переменной page_object

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ModelListCategoriy, self).get_context_data(**kwargs)
        context['results'] = self.items
        return context

    def get(self, request, *args, **kwargs):
        query = self.model.objects.all()
        paginator = Paginator(query, 3)
        page = request.GET.get('page')
        self.items = paginator.get_page(page)
        return super(ModelListCategoriy, self).get(request, *args, **kwargs)


class ModelDetailCategory(DetailView):
    model = Category
    template_name = 'products/detail.html'
    context_object_name = 'results'


class ModelUpdateCategory(AdminGroupRequired, UpdateView):
    model = Category
    redirect_url = reverse_lazy('categoriesapp:list')
    template_name = 'products/update.html'
    form_class = CategoryModelForm
    success_url = reverse_lazy('categoriesapp:list')


# not used
class ModelDeleteCategory(AdminGroupRequired, DeleteView):
    model = Category
    redirect_url = reverse_lazy('categoriesapp:list')
    template_name = 'products/delete.html'
    success_url = reverse_lazy('categoriesapp:list')
