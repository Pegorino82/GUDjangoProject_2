from basket.models import Basket


def basket(request):
    basket = []
    basket_total = 0
    basket_currency = None

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        basket_total = sum([p.product.now_price for p in basket]) if basket else basket_total
        basket_currency = basket[0].product.currency if basket else basket_currency

    return {
        'basket': basket,
        'basket_total': basket_total,
        'basket_currency': basket_currency
    }
