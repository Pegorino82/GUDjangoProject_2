from django import forms
from main.models import MainPageContent


class MainArticleModelForm(forms.ModelForm):
    date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-model-date'
            }
        )
    )

    class Meta:
        model = MainPageContent
        fields = ['chapter', 'content', 'date', 'author']
