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
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        # количество уникальных товаров
        items = self.items.select_related()
        return len(items)

    def get_order_price(self):
        total = 0
        for item in self.items.all():
            total += item.product.now_price * item.quantity
        return total

    def delete(self):
        self.is_active = False

    def __str__(self):
        full_name = self.user.get_full_name()
        username = full_name if full_name else self.user.username
        return f'{username}, order: {self.id}, created: {self.created.strftime("%Y-%m-%d %H:%M")}'


class OrderItem(models.Model):
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

    def get_order_item_price(self):
        # стоимость позиции
        return self.product.now_price * self.quantity

    def __str__(self):
        return self.product.name
