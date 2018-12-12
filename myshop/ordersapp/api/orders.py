from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.db.models import Q

from functools import reduce
import json

from ordersapp.models import Order, OrderItem
from products.models import Product


class OrderCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('customersapp:customer')
    product_model = apps.get_model('products', 'product')

    def post(self, request):
        data = json.loads(request.body)
        products_ids = data.keys()
        products_list = self.product_model.objects.filter(
            reduce(
                lambda q_obj, product_id: q_obj | Q(pk=product_id),
                data.keys(),
                Q()
            )
        )


        order = Order.objects.create(user=request.user)
        for product in products_list:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=data.get(str(product.id))
            )

        return JsonResponse(
            {
                'success_url': reverse('ordersapp:detail', kwargs={'pk': order.id})
                # 'success_url': reverse('articlesapp:list')
            }
        )

    def get(self, request):
        return JsonResponse(
            {
                'test': 'OK'
            }
        )


@login_required(login_url=reverse_lazy('customersapp:customer'))
def rest_create_order(request, *args, **kwargs):
    if request.method == 'POST':

        data = json.loads(request.body)
        products_ids = data.keys()
        products_list = Product.objects.filter(
            reduce(
                lambda product_id, q_obj: q_obj | Q(pk=product_id), products_ids,
                Q()
            )
        )

        order = Order.objects.create(user=request.user)
        for product in products_list:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=data.get(product.id)
            )

        return JsonResponse(
            {
                'success_url': reverse('ordersapp:detail', kwargs={'pk': order.id})
            }
        )

    return JsonResponse(
        {
            'test': 'OK'
        }
    )
