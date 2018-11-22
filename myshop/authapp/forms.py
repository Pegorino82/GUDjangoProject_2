import hashlib
import random
from django import forms
from django.core.exceptions import ValidationError
from customers.models import Customer


class CustomerModelForm(forms.ModelForm):
    birth_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'date',
                'class': 'form-model-date'
            }
        )
    )

    confirm_password = forms.CharField(
        max_length=250,
        widget=forms.PasswordInput
    )

    def save(self):
        new_user = super().save(commit=False)

        psw = new_user.password
        new_user.set_password(psw)

        new_user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        new_user.activation_key = hashlib.sha1((new_user.email + salt).encode('utf8')).hexdigest()
        new_user.save()

        return new_user

    class Meta:
        model = Customer
        fields = ['username', 'password', 'confirm_password', 'email', 'birth_date', '_avatar']
        widgets = {
            'username': forms.widgets.TextInput(
                attrs={
                    'class': 'form-control',
                    'value': ''
                }
            ),
            'password': forms.widgets.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'password',
                    'value': ''
                }
            ),
            # TODO сделать автозаполнение данными из модели
            'birth_date': forms.widgets.DateInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 200px;'
                }
            ),
        }
