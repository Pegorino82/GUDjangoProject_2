from django.shortcuts import reverse, render, redirect, get_object_or_404, get_list_or_404

from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator

from rest_framework.viewsets import ModelViewSet

from products.serializers import ProductSerializer
from products.models import Product, ProductMarker, Category
from images.models import Image


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# ?name=Api_product&short_text=short_text&long_text=long_text&now_price=1000&old_price=5000&product_marker=1&category=32&image=3

def rest_product_create(request):
    req = request.GET

    name = req.get('name')
    short_text = req.get('short_text')
    long_text = req.get('long_text')
    now_price = req.get('now_price')
    old_price = req.get('old_price')
    product_marker = req.get('product_marker')
    category = req.get('category')
    image = req.get('image')

    product = Product.objects.create(
        name=name,
        short_text=short_text,
        long_text=long_text,
        now_price=float(now_price),
        old_price=float(old_price),
        product_marker=ProductMarker.objects.get(id=int(product_marker)),
        category=Category.objects.get(id=int(category)),
        image=Image.objects.get(id=int(image))
    )
    product.save()

    obj = get_object_or_404(Product, name=name)
    data = obj.__dict__
    data.pop('_state')
    data.pop('id')

    return JsonResponse(
        {
            'results': data
        }
    )


def rest_product_list(request):
    quantity_per_page = request.GET.get('quantity_per_page') if request.GET.get('quantity_per_page') else 3
    query_set = get_list_or_404(Product)
    paginator = Paginator(query_set, quantity_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    rout_url = reverse('rest_products:rest_list')
    data = list(
        map(
            lambda itm: {
                'id': itm.id,
                'name': itm.name,
                'short_text': itm.short_text[:50] + '...' if (
                        itm.short_text and len(itm.short_text) > 50) else itm.short_text,
                'now_price': itm.now_price,
                'old_price': itm.old_price,
                'currency': itm.currency,
                'product_marker': itm.product_marker.corner,
                'category': itm.category.name,
                'image': itm.image.img.url
            },
            page
        )
    )

    result = {
        'next_url': f'{rout_url}?page={page.next_page_number()}' if page.has_next() else None,
        'previous_url': f'{rout_url}?page={page.previous_page_number()}' if page.has_previous() else None,
        'page': page.number,
        'count': paginator.count,
        'pages_all': int(paginator.count) // int(quantity_per_page) + 1,
        'results': data
    }

    return JsonResponse(result)


def rest_product_detail(request, **kwargs):
    pk = kwargs.get('pk')
    obj = get_object_or_404(Product, id=pk)
    data = {
        'id': pk,
        'name': obj.name,
        'short_text': obj.short_text[:50] + '...' if len(obj.short_text) > 50 else obj.short_text,
        'long_text': obj.short_text[:50] + '...' if len(obj.long_text) > 50 else obj.long_text,
        'now_price': obj.now_price,
        'old_price': obj.old_price,
        'currency': obj.currency,
        'product_marker': obj.product_marker.corner,
        'category': obj.category.name,
        'image': obj.image.img.url,
    }

    return JsonResponse(
        {
            'results': data
        }
    )


# ?name=Api_updated
# TODO foreign keys update
def rest_product_update(request, **kwargs):
    pk = kwargs.get('pk')
    obj = get_object_or_404(Product, id=pk)
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


def rest_product_delete(request, **kwargs):
    pk = kwargs.get('pk')
    obj = get_object_or_404(Product, id=pk)
    # obj.delete()
    obj.is_active = False
    obj.save()

    return JsonResponse(
        {
            'results': 'OK'
        }
    )

# забираем из БД товары, находящися в localStorage
def rest_basket_json(request, **kwargs):
    queryset = []
    if 'id_in' in request.GET:
        prods = list(map(int, request.GET['id_in'].split(',')))
        for id_ in prods:
            try:
                # obj = get_object_or_404(Product, id=id_)
                obj = Product.objects.get(id=id_)
                data = {
                    'id': obj.id,
                    'name': obj.name,
                    'now_price': obj.now_price,
                    'currency': obj.currency,
                    'product_marker': obj.product_marker.corner,
                    'category': obj.category.name,
                }
            except Exception as err:
                data = {'error': err}
            queryset.append(data)
    return JsonResponse(
        {
            'results': queryset
        }
    )
