from django.shortcuts import reverse, render, redirect, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse

from products.models import Category


def rest_category_list(request):
    query_set = get_list_or_404(Category)
    quantity_per_page = request.GET.get('quantity_per_page') if request.GET.get('quantity_per_page') else len(query_set)
    paginator = Paginator(query_set, quantity_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    rout_url = reverse('rest_categories:rest_list')
    data = list(
        map(
            lambda itm: {
                'name': itm.name,
                'short_text': itm.short_text[:50] + '...' if (
                        itm.short_text and len(itm.short_text) > 50) else itm.short_text,
            },
            page
        )
    )

    result = {
        'next_url': f'{rout_url}?page={page.next_page_number()}' if page.has_next() else None,
        'previous_url': f'{rout_url}?page={page.previous_page_number()}' if page.has_previous() else None,
        'page': page.number,
        'pages_all': int(paginator.count) // int(quantity_per_page) + 1,
        'count': paginator.count,
        'results': data
    }

    return JsonResponse(result)


def rest_category_detail(request, **kwargs):
    pk = kwargs.get('pk')
    obj = get_object_or_404(Category, id=pk)
    data = obj.__dict__
    data.pop('_state')
    data.pop('id')

    return JsonResponse(
        {
            'results': data
        }
    )
