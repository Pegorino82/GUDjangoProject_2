from django import forms
from products.models import Category


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'short_text']

    def __init__(self, *args, **kwargs):
        super(CategoryModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
