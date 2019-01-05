from django.db import models
# from django.dispatch import receiver
# from django.db.models.signals import post_save
from django.conf import settings
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
        #     print('*'*5+'delete'+'*'*5)
        #     print(self.quantity)
        #     print(self.product.quantity)
        #     print('*'*20)
        super().delete()

    def save(self, *args, **kwargs):
        # при добавлении в корзину убираем товар со склада
        self.product.quantity -= int(self.quantity)
        self.product.save()
        # print('*' * 5 + 'save' + '*' * 5)
        # print(self.quantity)
        # print(self.product.quantity)
        # print('*' * 20)
        super().save(*args, **kwargs)
