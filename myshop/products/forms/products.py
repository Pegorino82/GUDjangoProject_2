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

    def __init__(self, *args, **kwargs):
        super(ProductModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
