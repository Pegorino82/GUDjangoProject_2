import json
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from django.http import JsonResponse
from django.core import serializers

from basket.models import Basket
from customers.models import Customer


def rest_basket_list(request):
    user = request.user
    obj_list = get_list_or_404(Basket, user=user)
    data = [obj.__dict__ for obj in obj_list]
    for i in data:
        i.pop('_state')

    return JsonResponse(
        {
            'results': data,
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
