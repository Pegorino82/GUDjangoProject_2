from django.db import models


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )
    status = models.CharField(
        max_length=3,
        choices=ORDER_STATUS_CHOICES,
        default=FORMING
    )
    is_active = models.BooleanField(
        default=False
    )

    def get_total_quantity(self):
        # общее количество товаров
        items = self.items.select_related()
        return sum(list(map(lambda item: item.quantity, items)))

    def get_product_type_quantity(self):
        # количество уникальных товаров
        items = self.items.select_related()
        return len(items)

    def get_order_price(self):
        # стоимость всего заказа
        items = self.items.select_related()
        return sum(list(map(lambda item: item.get_order_item_price, items)))

    def delete(self):
        print('*' * 20)
        print('delete', self)
        print('*' * 20)
        # удаляем заказ, при этом добавляем количество товаров из заказа на склад
        for item in self.items.select_related():
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        self.save()

    def __str__(self):
        full_name = self.user.get_full_name()
        username = full_name if full_name else self.user.username
        return f'{username}, order: {self.id}, created: {self.created.strftime("%Y-%m-%d %H:%M")}'


class OrderItemQueryset(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(OrderItemQueryset, self).delete(*args, **kwargs)


class OrderItem(models.Model):
    objects = OrderItemQueryset.as_manager()
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    @property
    def get_order_item_price(self):
        # стоимость позиции
        return self.product.now_price * self.quantity

    def delete(self, using=None, keep_parents=False):
        # при удалении товара его количество возвращается на склад
        self.product.quantity += self.quantity
        self.product.save()
        super(self.__class__, self).delete()

    def __str__(self):
        return self.product.name
