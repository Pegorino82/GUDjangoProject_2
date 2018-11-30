import hashlib
import random
from django import forms
from django.core.exceptions import ValidationError
from customers.models import Customer


class CustomerAuthModelForm(forms.ModelForm):

    email = forms.EmailField(
        max_length=258,
        required=True
    )

    confirm_password = forms.CharField(
        max_length=250,
        widget=forms.PasswordInput
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password is not confirmed!')

        return self.cleaned_data

    def save(self):
        new_user = super().save(commit=False)

        psw = self.cleaned_data.get('password')
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

            'birth_date': forms.widgets.DateInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 200px;',
                    'placeholder': 'YYYY-MM-DD'
                }
            ),
        }
