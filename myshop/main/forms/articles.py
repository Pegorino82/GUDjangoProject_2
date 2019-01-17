from django import forms
from main.models import MainPageContent


class MainArticleModelForm(forms.ModelForm):

    class Meta:
        model = MainPageContent
        fields = ['chapter', 'content', 'author']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
