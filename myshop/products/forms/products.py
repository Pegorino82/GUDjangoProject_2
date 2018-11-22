from django import forms
from products.models import Product


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'short_text',
            'long_text',
            'now_price',
            'old_price',
            'currency',
            'product_marker',
            'image',
            ]
