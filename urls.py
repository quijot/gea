from django.conf.urls import patterns, include, url

from gea import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
#    url(r'^solic/(?P<eid>\d+)/(?P<domfiscal>(\w|\s|,|.|-|_|\\)*)/(?P<localidad>(\w|\s)*)/(?P<cp>\w*)$', views.solic),
#    url(r'^visac/(?P<eid>\d+)/(?P<sr>(\w|\s|,|.|-|_)*)/(?P<localidad>(\w|\s|,|.|-|_)*)$', views.visac),
#    url(r'^plano/(?P<circunscripcion>\d{1})/(?P<nro_inscripcion>\d{6})$', views.plano),
#    url(r'^set/(?P<pii>\d{6})(?P<sub_pii>\d{4})$', views.set),
#    url(r'^dvapi/(?P<dv>\d)$', views.dvapi),
    url(r'^solicitud/$', views.solic),
    url(r'^visacion/$', views.visacion),
    url(r'^plano/$', views.plano),
    url(r'^set/$', views.set),
    url(r'^catastro/$', views.catastro),
    url(r'^dvapi/$', views.dvapi),
    url(
       r'^presup/(?P<persona>(\w|\s|,|.|-|_)*)/(?P<objeto>(\w|\s|,|.|-|_)*)$',
       views.presup),
    url(r'^presup_form/$', views.presup_form),
)
