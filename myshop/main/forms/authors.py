from django import forms
from main.models import Author


class MainAuthorForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        label='Your name',
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-model-input',
            }
        )
    )
    lastname = forms.CharField(
        max_length=150,
        label='Your surname',
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-model-input'
            }
        )
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.widgets.FileInput(
            attrs={
                'type': 'file',
                'class': 'form-model-file'
            }
        )
    )


class MainAuthorModelForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'lastname', 'photo']
