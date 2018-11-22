from django import forms
from products.models import Category


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'short_text']