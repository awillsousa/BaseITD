from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^acordao/$', views.index, name='index'),
    url(r'^$', views.acordao_list, name='home'),
    url(r'^acordao/$', views.acordao_list, name='acordao_lista'),
    url(r'^acordao/id=(?P<id_acordao>.*)/$', views.acordao_detail, name='acordao_detail'),
]
