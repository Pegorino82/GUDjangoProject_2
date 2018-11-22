from django.urls import path, re_path

from myshopadmin.views import ModelCreate, ModelUpdate, ModelDelete, ModelDetail, \
    ModelList, index

app_name = 'myshopadminapp'

urlpatterns = [
    path('', index, name='index'),
    re_path(r'^(?P<app>\w+)/(?P<model>\w+)/create/$', ModelCreate.as_view(), name='create'),
    re_path(r'^(?P<app>\w+)/(?P<model>\w+)/update/(?P<pk>\d+)/$', ModelUpdate.as_view(), name='update'),
    re_path(r'^(?P<app>\w+)/(?P<model>\w+)/delete/(?P<pk>\d+)/$', ModelDelete.as_view(), name='delete'),
    re_path(r'^(?P<app>\w+)/(?P<model>\w+)/(?P<pk>\d+)/$', ModelDetail.as_view(), name='detail'),
    re_path(r'^(?P<app>\w+)/(?P<model>\w+)/$', ModelList.as_view(), name='list'),
]
