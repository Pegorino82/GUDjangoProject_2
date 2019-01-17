from rest_framework import serializers
from rest_framework.pagination import *

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    product_marker = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    # extra_kwargs = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'url',
            'name',
            'category',
            'short_text',
            'long_text',
            'now_price',
            'old_price',
            'currency',
            'product_marker',
            'image',
            'modified',
            'created',
            # 'extra_kwargs'
        ]

    def get_category(self, obj):
        return obj.category.name

    def get_product_marker(self, obj):
        return obj.product_marker.corner

    def get_image(self, obj):
        return obj.image.img.url

    # def get_extra_kwargs(self):
    #
    #     return super(ProductSerializer, self).get_extra_kwargs()