from django import forms

from images.models import Image

class ImageModelForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'img']