from django.conf.urls import url
from . import  views


app_name = 'api'

urlpatterns = [
    url(r'^getPK/$', views.getPK, name='getPK'),
    url(r'^newE/$', views.newE, name='newE'),
    url(r'^exist/$', views.exist, name='exist')
]