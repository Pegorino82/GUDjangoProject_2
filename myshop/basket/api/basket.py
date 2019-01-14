import json
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from django.http import JsonResponse, Http404, HttpResponseNotFound
from django.core import serializers

from basket.models import Basket


def rest_basket_list(request):
    user = request.user
    if not user.is_anonymous:
        obj_list = Basket.objects.filter(user=user)
        if len(obj_list) > 0:
            # data = [obj.__dict__ for obj in obj_list]
            data = [obj.__dict__ for obj in obj_list]
            print('*>>'*20, data)
            for i in data:
                i.pop('_state')

            items = sum([item['quantity'] for item in data])

            total_cost = 0
            for item in Basket.objects.filter(user=user):
                total_cost += item.product.now_price * item.quantity

        else:
            data = []
            items = 0
            total_cost = 0

        widget_data = {
            'items': items,
            'total_cost': total_cost
        }

        return JsonResponse(
            {
                'results': data,
                'widget_data': widget_data
            }
        )
    else:
        # raise Http404('No Basket matches the given query.')
        return JsonResponse(
            {
                'widget_data': {
                    'items': 'нет',
                    'total_cost': 0
                }
            }
        )


def rest_basket_detail(request):
    pk = request.GET.get('id')
    obj = get_object_or_404(Basket, id=pk)
    data = obj.__dict__
    data.pop('_state')

    return JsonResponse(
        {
            'results': data,
        }
    )


def rest_basket_update(request):
    pk = request.GET.get('id')
    obj = get_object_or_404(Basket, id=pk)
    for key, val in request.GET.items():
        setattr(obj, key, val)
    obj.save()

    data = obj.__dict__
    data.pop('_state')
    data.pop('id')

    return JsonResponse(
        {
            'results': data
        }
    )

def rest_basket_delete(request):
    pk = request.GET.get('id')
    obj = get_object_or_404(Basket, id=pk)
    obj.delete()

    data = {'OK'}

    return JsonResponse(
        {
            'results': data
        }
    )
