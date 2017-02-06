from django.conf.urls import url

from gea.views import Home, About, \
CatastroLocalList, \
ExpedienteList, ExpedienteDetail, \
PersonaList, PersonaDetail, \
solicitud, visacion, \
plano, set, catastro, \
caratula, dvapi, sie, calendar


urlpatterns = [
    # Inicio
    url(r'^$', Home.as_view(), name='home'),
    # Abouto
    url(r'^acerca/$', About.as_view(), name='about'),
    # Catastros Locales
    url(r'^catastros-locales/$', CatastroLocalList.as_view(), name='catastros_locales'),
    # Expedientes
    url(r'^expedientes/$', ExpedienteList.as_view(), name="expedientes"),
    url(r'^expedientes/(?P<pk>\d+)/$', ExpedienteDetail.as_view(), name="expediente"),
    # Personas
    url(r'^personas/$', PersonaList.as_view(), name="personas"),
    url(r'^personas/(?P<pk>\d+)/$', PersonaDetail.as_view(), name="persona"),
    # Notas
    url(r'^solicitud/$', solicitud, name="solicitud"),
    url(r'^visacion/$', visacion, name="visacion"),
    # Búsquedas
    url(r'^plano/$', plano, name="buscar_plano"),
    url(r'^set/$', set, name="buscar_set"),
    url(r'^catastro/$', catastro, name="buscar_catastro"),
    # Herramientas
    url(r'^caratula/$', caratula, name="caratula"),
    url(r'^dvapi/$', dvapi, name='dvapi'),
    url(r'^sie/$', sie, name='sie'),
    url(r'^cal/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', calendar, name='cal'),
#    url(r'^cal/$', calendar, name='cal'),
]
