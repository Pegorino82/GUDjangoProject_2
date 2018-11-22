from django.urls import path, re_path

from authapp import views

app_name = 'authapp'

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('logup/', views.logup_view, name='logup_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('verify/', views.verify, name='verify'),
]