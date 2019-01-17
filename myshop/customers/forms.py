from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from customers.models import Customer, CustomerProfile


class CustomerCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'birth_date', '_avatar']


class CustomerUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'password', 'email', 'birth_date', '_avatar']

class CustomerModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    class Meta:
        model = Customer
        fields = ['username', 'password', 'birth_date', 'email', '_avatar']
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
            'email': forms.widgets.TextInput(
                attrs={
                    'class': 'form-control',
                    'value': ''
                }
            ),
            'birth_date': forms.widgets.DateInput(
                attrs={
                    'class': 'form-control',
                    'style': 'width: 200px;',
                    'placeholder': '1999-12-31'
                }
            ),
        }


class CustomerProfileModelForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['aboutMe', 'gender']

    def __init__(self, *args, **kwargs):
        super(CustomerProfileModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
