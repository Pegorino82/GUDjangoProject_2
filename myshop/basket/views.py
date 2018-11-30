from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.template.loader import render_to_string

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from basket.models import Basket
from products.models import Product


class ModelBasketList(LoginRequiredMixin, ListView):
    model = Basket
    template_name = 'basket/basket.html'
    succes_url = 'basketapp:list'
    login_url = 'authapp:login_view'


@login_required(login_url='/auth/login/')
def basket(request):
    template_name = 'basket/basket.html'
    return render(request, template_name, {'basket': basket})


@login_required(login_url='/auth/login/')
def add_product(request, **kwargs):
    pk = kwargs.get('pk')
    prod = Product.objects.get(pk=pk)
    old_basket = Basket.objects.filter(product=prod, user=request.user)
    if old_basket:
        old_basket[0].quantity += 1
        old_basket[0].save()
    else:
        new_basket = Basket(product=prod, user=request.user)
        new_basket.quantity += 1
        new_basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/auth/login/')
def remove_product(request, **kwargs):
    pk = kwargs.get('pk')
    prod = Product.objects.get(pk=pk)
    old_basket = Basket.objects.filter(product=prod, user=request.user)
    if old_basket and old_basket[0].quantity > 0:
        old_basket[0].quantity -= 1
        old_basket[0].save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/auth/login/')
def delete_product(request, **kwargs):
    pk = kwargs.get('pk')
    prod = Basket.objects.get(pk=pk)
    prod.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/auth/login/')
def edit_basket(request, pk, quantity, **kwargs):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=pk)
        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()
        basket_items = Basket.objects.filter(user=request.user).order_by('product.category')
        content = {
            'basket_items': basket_items,
        }
        result = render_to_string('basket/components/product.html', content)

        return JsonResponse({'result': result})
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
