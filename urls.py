from django.conf.urls import patterns, url

from gea import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
