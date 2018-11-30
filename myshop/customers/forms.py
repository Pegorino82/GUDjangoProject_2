from django import forms
from customers.models import Customer, CustomerProfile


class CustomerModelForm(forms.ModelForm):
    # birth_date = forms.DateField(
    #     input_formats=['%Y-%m-%d'],
    #     widget=forms.DateTimeInput(
    #         attrs={
    #             'type': 'date',
    #             'class': 'form-model-date'
    #         }
    #     )
    # )

    class Meta:
        model = Customer
        fields = ['username', 'password', 'birth_date', '_avatar']
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

class CustomerProfileModelForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['aboutMe', 'gender']

    def __init__(self, *args, **kwargs):
        super(CustomerProfileModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
