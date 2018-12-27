import hashlib
import random
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from customers.models import Customer


class CustomerLoginForm(AuthenticationForm):
    class Meta:
        model = Customer
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(CustomerLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CustomerAuthModelForm(UserCreationForm):
    # email = forms.EmailField(
    #     max_length=258,
    #     required=True
    # )
    #
    # confirm_password = forms.CharField(
    #     max_length=250,
    #     widget=forms.PasswordInput
    # )

    # def clean_confirm_password(self):
    #     password = self.cleaned_data.get('password')
    #     confirm_password = self.cleaned_data.get('confirm_password')
    #
    #     if password and confirm_password and password != confirm_password:
    #         raise forms.ValidationError('Password is not confirmed!')
    #
    #     return self.cleaned_data

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
        fields = ['username', 'password1', 'password2', 'email', 'birth_date', '_avatar']

    def __init__(self, *args, **kwargs):
        super(CustomerAuthModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['value'] = ''
            field.help_text = ''
            if field_name == 'birth_date':
                field.widget.attrs['placeholder'] = 'YYYY-MM-DD'
