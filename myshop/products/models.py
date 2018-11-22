from django.db import models
from django.db.models import Q, QuerySet

from images.models import Image


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True)
    short_text = models.CharField(
        max_length=150,
        null=True,
        blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductMarker(models.Model):
    corner = models.CharField(
        max_length=45,
        null=True,
        blank=True,
        unique=True
    )

    def __str__(self):
        return self.corner


def default_image():
    return Image.objects.get(name='default')


def default_product_marker():
    return ProductMarker.objects.get(corner='None')


def default_category():
    return Category.objects.get(name='New category')


class Product(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True)
    short_text = models.CharField(
        max_length=150,
        null=True,
        blank=True)
    long_text = models.CharField(
        max_length=350,
        null=True,
        blank=True)
    now_price = models.DecimalField(
        max_digits=10,
        decimal_places=2)
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    currency = models.CharField(
        max_length=50,
        default='₽'
    )

    product_marker = models.ForeignKey(
        'products.ProductMarker',
        on_delete=models.PROTECT,
        default=default_product_marker
    )
    category = models.ForeignKey(
        'products.Category',
        on_delete=models.CASCADE,
        default=default_category
    )
    image = models.ForeignKey(
        'images.Image',
        on_delete=models.PROTECT,
        default=default_image
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name

    @classmethod
    def get_limit(cls, limit):
        categories = Category.objects.all()
        res = list()
        for cat in categories:
            for prod in cls.objects.filter(category=cat.id, is_active=True)[:limit]:
                res.append(prod)

        return res
