from django.urls import path

from gea.views import (
    About,
    CatastroLocalList,
    ExpedienteDetail,
    ExpedienteList,
    Home,
    PersonaDetail,
    PersonaList,
    caratula,
    catastro,
    dvapi,
    plano,
    set,
    sie,
    solicitud,
    visacion,
)

urlpatterns = [
    # Inicio
    path("", Home.as_view(), name="home"),
    # About
    path("acerca/", About.as_view(), name="about"),
    # Catastros Locales
    path("catastros-locales/", CatastroLocalList.as_view(), name="catastros_locales"),
    # Expedientes
    path("expedientes/", ExpedienteList.as_view(), name="expedientes"),
    path("expedientes/<int:pk>/", ExpedienteDetail.as_view(), name="expediente"),
    # Personas
    path("personas/", PersonaList.as_view(), name="personas"),
    path("personas/<int:pk>/", PersonaDetail.as_view(), name="persona"),
    # Notas
    path("solicitud/", solicitud, name="solicitud"),
    path("visacion/", visacion, name="visacion"),
    # Búsquedas
    path("plano/", plano, name="buscar_plano"),
    path("set/", set, name="buscar_set"),
    path("catastro/", catastro, name="buscar_catastro"),
    # Herramientas
    path("caratula/", caratula, name="caratula"),
    path("dvapi/", dvapi, name="dvapi"),
    path("sie/", sie, name="sie"),
]
