#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from gea.views import Home, catastros_locales, lugares, secciones, manzanas, \
parcelas, listado_alfabetico, caratula, solicitud, visacion, plano, set, \
catastro, dvapi, ExpedienteList, ExpedienteDetail, PersonaList, PersonaDetail, \
CatastroLocalList

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    # Catastros Locales
    url(r'^catastros-locales/$', CatastroLocalList.as_view(), name='catastros_locales'),
#     url(r'^catastros-locales/$', catastros_locales, name='catastros_locales'),
#     url(r'^catastros-locales/(?P<l>[^/]+)/$', lugares),
#     url(r'^catastros-locales/(?P<l>[^/]+)/(?P<s>[^/]+)/$', secciones),
#     url(r'^catastros-locales/(?P<l>[^/]+)/(?P<s>[^/]+)/(?P<m>[^/]+)/$',
#         manzanas),
    url(r'^catastros-locales/%s' %
    '(?P<l>[^/]+)/(?P<s>[^/]+)/(?P<m>[^/]+)/(?P<p>[^/]+)/$', parcelas),
    # Listado alfabético
    url(r'^listado-alfabetico/$', listado_alfabetico,
        name='listado_alfabetico'),
    url(r'^listado-alfabetico/(?P<inicial>[^/]+)/$', listado_alfabetico,
        name="listado_alfabetico"),
    # Expedientes
    url(r'^expedientes/$', ExpedienteList.as_view(), name="expedientes"),
    url(r'^expedientes/(?P<pk>\d+)/$', ExpedienteDetail.as_view(),
        name="expediente"),
    # Personas
    url(r'^personas/$', PersonaList.as_view(), name="personas"),
    url(r'^personas/(?P<pk>\d+)/$', PersonaDetail.as_view(),
        name="persona"),
    # Notas
    url(r'^caratula/$', caratula, name="caratula"),
    url(r'^solicitud/$', solicitud, name="solicitud"),
    url(r'^visacion/$', visacion, name="visacion"),
    # Búsquedas
    url(r'^plano/$', plano),
    url(r'^set/$', set),
    url(r'^catastro/$', catastro),
    # Herramientas
    url(r'^dvapi/$', dvapi, name='dvapi'),
)
