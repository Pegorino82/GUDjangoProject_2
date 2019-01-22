from django.db import models
# from django.dispatch import receiver
# from django.db.models.signals import post_save
from django.conf import settings
from django.utils.functional import cached_property
from products.models import Product


# from ordersapp.models import OrderItem


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=0
    )
    add_datetime = models.DateTimeField(
        auto_now_add=True
    )

    def delete(self, using=None, keep_parents=False):
        # при удалении товара его количество возвращается на склад
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()

    def save(self, *args, **kwargs):
        # при добавлении в корзину убираем товар со склада
        self.product.quantity -= int(self.quantity)
        self.product.save()
        super().save(*args, **kwargs)

    @cached_property
    def get_cached_items(self):
        return self.user.basket.select_related()

    @property
    def get_product_cost(self):
        return self.product.now_price * self.quantity

    @property
    def get_total_quantity(self):
        # _items = Basket.objects.filter(user=self.user).select_related()
        _items = self.get_cached_items
        _total_quantity = sum(map(lambda x: x.quantity, _items))
        return _total_quantity

    @property
    def get_total_cost(self):
        # _items = Basket.objects.filter(user=self.user).select_related()
        _items = self.get_cached_items
        _total_cost = sum(map(lambda x: x.product.now_price * x.quantity, _items))
        return _total_cost
