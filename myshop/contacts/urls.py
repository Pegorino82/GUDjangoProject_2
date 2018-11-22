from django.urls import path

from . import views

app_name = 'contactsapp'

urlpatterns = [
    path('', views.contacts, name='contacts'),
]