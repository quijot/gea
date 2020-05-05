from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from .models import (
    Antecedente,
    Catastro,
    CatastroLocal,
    Circunscripcion,
    Comprobante,
    Dp,
    Ds,
    Expediente,
    ExpedienteLugar,
    ExpedientePartida,
    ExpedientePersona,
    Lugar,
    Objeto,
    Pago,
    Partida,
    PartidaDominio,
    Persona,
    Presupuesto,
    Profesional,
    Sd,
    Titulo,
    Zona,
)

# -----------------------------------------------------------------------------
# Custom Filters
# -----------------------------------------------------------------------------

# Expedientes


class InscriptoFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("inscripto")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "inscripto"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ("si", _("Si")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == "si":
            return queryset.filter(inscripcion_numero__isnull=False)
        if self.value() == "no":
            return queryset.filter(inscripcion_numero__isnull=True)


class TieneOrdenFilter(admin.SimpleListFilter):
    title = _("tiene orden")
    parameter_name = "orden"

    def lookups(self, request, model_admin):
        return (
            ("si", _("Si")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "si":
            return queryset.filter(orden_numero__isnull=False)
        if self.value() == "no":
            return queryset.filter(orden_numero__isnull=True)


class TieneOrdenPendienteFilter(admin.SimpleListFilter):
    title = _("orden pendiente")
    parameter_name = "orden_pendiente"

    def lookups(self, request, model_admin):
        return (
            ("si", _("Si")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "si":
            return queryset.filter(
                orden_numero__isnull=False, inscripcion_numero__isnull=True
            )
        if self.value() == "no":
            return queryset.exclude(
                orden_numero__isnull=False, inscripcion_numero__isnull=True
            )


class TieneAntecedentesFilter(admin.SimpleListFilter):
    title = _("tiene antecedentes")
    parameter_name = "antecedente"

    def lookups(self, request, model_admin):
        return (
            ("si", _("Si")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "si":
            return queryset.filter(antecedente__isnull=False)
        if self.value() == "no":
            return queryset.filter(antecedente__isnull=True)


class TieneObjetoFilter(admin.SimpleListFilter):
    title = _("tiene objeto")
    parameter_name = "objeto"

    def lookups(self, request, model_admin):
        return (
            ("si", _("Si")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "si":
            return queryset.filter(objetos__isnull=False)
        if self.value() == "no":
            return queryset.filter(objetos__isnull=True)


class TienePlanoFilter(admin.SimpleListFilter):
    title = _("tiene plano cargado")
    parameter_name = "plano_ruta"

    def lookups(self, request, model_admin):
        return (
            ("si", _("Si")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "si":
            return queryset.exclude(plano_ruta__isnull=True)
        if self.value() == "no":
            return queryset.exclude(plano_ruta__isnull=False)


class TieneSetFilter(admin.SimpleListFilter):
    title = _("tiene informe cargado")
    parameter_name = "informe"

    def lookups(self, request, model_admin):
        return (
            ("si", _("Si")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "si":
            return queryset.exclude(set_ruta__isnull=True)
        if self.value() == "no":
            return queryset.exclude(set_ruta__isnull=False)


# -----------------------------------------------------------------------------
# Inlines
# -----------------------------------------------------------------------------

# Expedientes


class CatastroLocalInline(NestedTabularInline):
    classes = ("extrapretty", "collapse")
    model = CatastroLocal
    extra = 0
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "10"})},
    }


class ExpedienteLugarInline(NestedStackedInline):
    classes = ["extrapretty"]
    model = ExpedienteLugar
    extra = 0
    inlines = [CatastroLocalInline]


class ExpedientePersonaInline(NestedStackedInline):
    classes = ["extrapretty"]
    model = ExpedientePersona
    extra = 0
    ordering = ["-comitente"]


class CatastroInline(NestedTabularInline):
    classes = ("extrapretty", "collapse")
    model = Catastro
    extra = 0
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "10"})},
    }


class ExpedientePartidaInline(NestedStackedInline):
    classes = ["extrapretty"]
    model = ExpedientePartida
    extra = 0
    inlines = [CatastroInline]
    exclude = ["set_ruta"]


class AntecedenteInline(NestedTabularInline):
    classes = ["extrapretty"]
    model = Antecedente
    fk_name = "expediente"
    extra = 0
    ordering = ["-expediente_modificado", "-inscripcion_numero"]


# -----------------------------------------------------------------------------
# Admin
# -----------------------------------------------------------------------------
admin.site.register(Antecedente)
admin.site.register(Catastro)
admin.site.register(CatastroLocal)
admin.site.register(Circunscripcion)
admin.site.register(Comprobante)
admin.site.register(Dp)
admin.site.register(Ds)
admin.site.register(ExpedienteLugar)
admin.site.register(ExpedientePartida)
admin.site.register(ExpedientePersona)
admin.site.register(Lugar)
admin.site.register(Objeto)
admin.site.register(Pago)
admin.site.register(Partida)
admin.site.register(PartidaDominio)
admin.site.register(Persona)
admin.site.register(Presupuesto)
admin.site.register(Profesional)
admin.site.register(Sd)
admin.site.register(Titulo)
admin.site.register(Zona)


@admin.register(Expediente)
class ExpedienteAdmin(NestedModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [("id", "fecha_plano", "created", "modified")],
                "classes": ("extrapretty"),
            },
        ),
        ("Estado", {"fields": [("fecha_medicion",)], "classes": ("extrapretty")},),
        (
            "SCIT - Servicio de Catastro e Información Territorial",
            {
                "fields": [
                    (
                        "inscripcion_numero",
                        "inscripcion_fecha",
                        "duplicado",
                        "sin_inscripcion",
                    )
                ],
                "classes": ("extrapretty"),
            },
        ),
        (
            "Orden de Trabajo CoPA",
            {"fields": [("orden_numero", "orden_fecha")], "classes": ("extrapretty"),},
        ),
        (
            "Otros",
            {
                "fields": [("cancelado", "cancelado_por"), ("plano_ruta", "ver_plano")],
                "classes": ("extrapretty", "collapse"),
            },
        ),
        ("Objetos", {"fields": [("objetos")], "classes": ("extrapretty")}),
        (
            "Profesionales Firmantes",
            {"fields": [("profesionales_firmantes")], "classes": ("extrapretty"),},
        ),
    ]
    readonly_fields = ("created", "modified", "ver_plano")
    inlines = [
        ExpedienteLugarInline,
        ExpedientePersonaInline,
        ExpedientePartidaInline,
        AntecedenteInline,
    ]
    list_display = (
        "id",
        "created",
        "fecha_medicion",
        "fecha_plano",
        "inscripcion_numero",
        "inscripcion_fecha",
        "duplicado",
        "sin_inscripcion",
        "orden_numero",
        "orden_fecha",
        "cancelado",
        "ver_plano",
    )
    list_editable = (
        # "fecha_medicion",
        # "fecha_plano",
        # "inscripcion_numero",
        # "inscripcion_fecha",
        # "duplicado",
        # "orden_numero",
        # "orden_fecha",
        # "sin_inscripcion",
        # "cancelado",
        # "plano_ruta",
    )
    list_filter = [
        InscriptoFilter,
        "duplicado",
        "sin_inscripcion",
        TieneOrdenFilter,
        TieneOrdenPendienteFilter,
        "cancelado",
        "cancelado_por",
        TienePlanoFilter,
        "expedientelugar__lugar__nombre",
        "expedientelugar__catastrolocal__seccion",
        "expedientelugar__catastrolocal__manzana",
        "expedientelugar__catastrolocal__parcela",
        "expedientepersona__usufructo",
        TieneObjetoFilter,
        TieneAntecedentesFilter,
    ]
    search_fields = [
        "id",
        "fecha_plano",
        "inscripcion_numero",
        "inscripcion_fecha",
        "orden_numero",
        "orden_fecha",
        "cancelado_por",
        "expedientelugar__lugar__nombre",
        "expedientepersona__persona__apellidos",
        "expedientepersona__persona__nombres",
        "expedientepersona__persona__apellidos_alternativos",
        "expedientepersona__persona__nombres_alternativos",
        "profesionales_firmantes__apellidos",
        "profesionales_firmantes__nombres",
        "objetos__nombre",
        "expedientepartida__partida__pii",
        "antecedente__expediente_modificado__id",
        "antecedente__inscripcion_numero",
    ]
    actions_on_bottom = True
    date_hierarchy = "inscripcion_fecha"
    list_per_page = 20
    save_on_top = True

    def ver_plano(self, obj):
        if obj.plano_ruta != "" and obj.plano_ruta is not None:
            return '<a href="%s">%s</a>' % (obj.plano_ruta, obj.inscripcion_numero)
        else:
            return None

    ver_plano.allow_tags = True
    ver_plano.short_description = "Ver plano"
    ver_plano.admin_order_field = "plano_ruta"
