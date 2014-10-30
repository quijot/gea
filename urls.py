# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from gea import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^solic/(?P<eid>\d+)/(?P<domfiscal>(\w|\s|,|.|-|_|/|\\)*)/(?P<localidad>(\w|\s)*)/(?P<cp>\w*)$', views.solic),
    url(r'^solicitud/$', views.solic_form),
    url(r'^visac/(?P<eid>\d+)/(?P<sr>(\w|\s|,|.|-|_)*)/(?P<localidad>(\w|\s|,|.|-|_)*)$', views.visac),
    url(r'^visacion/$', views.visac_form),
    url(r'^plano/(?P<circunscripcion>\d{1})/(?P<nro_inscripcion>\d{6})$', views.plano),
    url(r'^plano_form/$', views.plano_form),
    url(r'^set/(?P<pii>\d{6})(?P<sub_pii>\d{4})$', views.set),
    url(r'^set_form/$', views.set_form),
    url(r'^dvapi/(?P<dv>\d)$', views.dvapi),
    url(r'^dvapi_form/$', views.dvapi_form),
    url(r'^presup/(?P<persona>(\w|\s|,|.|-|_)*)/(?P<objeto>(\w|\s|,|.|-|_)*)$', views.presup),
    url(r'^presup_form/$', views.presup_form),
    url(r'^catastro_form/$', views.catastro_form),
)
