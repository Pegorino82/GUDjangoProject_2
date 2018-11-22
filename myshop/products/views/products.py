from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from customers.mixins import AdminGroupRequired
from products.models import Product, Category
from products.forms import ProductModelForm


def catalog(request):
    categories = Category.objects.all()
    categories_paginator = Paginator(categories, 3)
    categories_page = request.GET.get('page')
    categories_items = categories_paginator.get_page(categories_page)
    context = {
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

    return render(request,
                  'products/product.html',
                  result
                  )


class ModelCreateProduct(LoginRequiredMixin, AdminGroupRequired, CreateView):
    model = Product
    template_name = 'products/create.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('productsapp:list')
    login_url = reverse_lazy('customersapp:customer')
    redirect_url = reverse_lazy('productsapp:list')


class ModelListProduct(ListView):
    # model = Product
    queryset = Product.objects.filter(is_active=True)
    template_name = 'products/products_list.html'
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super(ModelListProduct, self).get_context_data(**kwargs)
        context['results'] = self.items
        return context

    def get(self, request, *args, **kwargs):
        # query = self.model.objects.all()
        paginator = Paginator(self.queryset, 3)
        page = request.GET.get('page')
        self.items = paginator.get_page(page)
        return super(ModelListProduct, self).get(request, *args, **kwargs)


class ModelDetailProduct(DetailView):
    # model = Product
    queryset = Product.objects.filter(is_active=True)
    template_name = 'products/detail.html'
    context_object_name = 'product'


class ModelUpdateProduct(LoginRequiredMixin, AdminGroupRequired, UpdateView):
    # model = Product
    queryset = Product.objects.filter(is_active=True)
    template_name = 'products/update.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('productsapp:catalog')
    login_url = reverse_lazy('customersapp:customer')
    redirect_url = reverse_lazy('productsapp:list')


class ModelDeleteProduct(LoginRequiredMixin, UserPassesTestMixin, AdminGroupRequired,  DeleteView):
    # model = Product
    queryset = Product.objects.filter(is_active=True)
    template_name = 'products/delete.html'
    success_url = reverse_lazy('productsapp:list')
    login_url = reverse_lazy('customersapp:customer')
    redirect_url = reverse_lazy('productsapp:list')

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.obj = self.queryset.get(pk=pk)
        self.obj.is_active = False
        self.obj.save()

        return super(ModelDeleteProduct, self).post(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #
    #     return super(ModelDeleteProduct, self).post(request)