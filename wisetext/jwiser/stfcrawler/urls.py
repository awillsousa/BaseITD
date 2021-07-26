from django.conf.urls import url

from . import views
from .views import ListaAcordaosView, HomePageView

app_name = 'stfcrawler'
urlpatterns = [

    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^acordao/$', ListaAcordaosView.as_view(), name='lista'),
    url(r'^acordao/id=(?P<id_acordao>.*)/$', views.detail, name='detail'),    
    url(r'^acordao/add/$', views.acordao_add, name='acordao_add'),
]
