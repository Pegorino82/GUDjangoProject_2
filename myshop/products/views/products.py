from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from customers.mixins import AdminGroupRequired
from products.models import Product, Category
from products.forms import ProductModelForm

from django.core.exceptions import ObjectDoesNotExist


class Catalog(ListView):
    model = Category
    template_name = 'products/catalog.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Catalog'})
        context.update({'limit_products': Product.get_limit(3)})  # TODO надо оптимизировать!
        context.update({'pagination_url': reverse_lazy('productsapp:catalog')})
        return context


class ProductCreateView(LoginRequiredMixin, AdminGroupRequired, CreateView):
    model = Product
    template_name = 'products/create_product.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('productsapp:list')
    login_url = reverse_lazy('authapp:login_view')
    redirect_url = reverse_lazy('productsapp:list')  # AdminGroupRequired
    extra_context = {'title': 'Product Create'}


# В настоящий момент отображение товаров и пагинация
# осуществляется js (products/api/products/rest_product_list/)
class ProductListView(ListView):
    # model = Product
    queryset = Product.objects.filter(is_active=True)
    template_name = 'products/list_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = self.items
        context['title'] = 'Product List'
        return context

    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.queryset, 3)
        page = request.GET.get('page')
        self.items = paginator.get_page(page)
        return super().get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    # model = Product
    queryset = Product.objects.filter(is_active=True)
    template_name = 'products/detail_product.html'
    extra_context = {'title': 'Product Detail '}


class ProductUpdateView(LoginRequiredMixin, AdminGroupRequired, UpdateView):
    # model = Product
    queryset = Product.objects.filter(is_active=True)
    template_name = 'products/update_product.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('productsapp:catalog')
    login_url = reverse_lazy('authapp:login_view')
    redirect_url = reverse_lazy('productsapp:list')  # AdminGroupRequired
    extra_context = {'title': 'Product Update'}


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, AdminGroupRequired, DeleteView):
    queryset = Product.objects.filter(is_active=True)
    template_name = 'products/delete.html'
    success_url = reverse_lazy('productsapp:list')
    login_url = reverse_lazy('authapp:login_view')
    redirect_url = reverse_lazy('productsapp:list')  # AdminGroupRequired
    extra_context = {'title': 'Product Delete'}

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


########### функции для каталога и детального представления продукта##########
def catalog(request):
    categories = Category.objects.all()
    categories_paginator = Paginator(categories, 3)
    categories_page = request.GET.get('page')
    categories_items = categories_paginator.get_page(categories_page)
    context = {
        'title': 'Catalog',
        'categories': categories_items,
        'all_categories': Category.objects.all(),
        'limit_products': Product.get_limit(3)
    }

    return render(request, 'products/catalog.html', context)


def product(request, category, pk):
    result = {
        'category': category,
        'pk': pk,
        'product': Product.objects.get(id=pk, is_active=True),
        'categories': Category.objects.all()
    }

    return render(
        request,
        'products/product.html',
        result
    )
