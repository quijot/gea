from django.contrib import admin

from nested_admin import NestedAdmin as NestedModelAdmin, NestedStackedInline
from django.contrib.admin import TabularInline as NestedTabularInline

# models
from gea.models import Antecedente, Catastro, CatastroLocal, Circunscripcion, \
Comprobante, Dp, Ds, Sd, Expediente, ExpedienteLugar, ExpedienteObjeto, \
ExpedientePartida, ExpedientePersona, ExpedienteProfesional, Lugar, Objeto, \
Pago, Partida, PartidaDominio, Persona, Presupuesto, Profesional, Titulo, Zona

from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

import unicodedata


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

#
# Custom Filters
#

# Expedientes
class InscriptoFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('inscripto')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'inscripto'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'si':
            return queryset.filter(inscripcion_numero__isnull=False)
        if self.value() == 'no':
            return queryset.filter(inscripcion_numero__isnull=True)


class TieneOrdenFilter(admin.SimpleListFilter):
    title = _('tiene orden')
    parameter_name = 'orden'

    def lookups(self, request, model_admin):
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.filter(orden_numero__isnull=False)
        if self.value() == 'no':
            return queryset.filter(orden_numero__isnull=True)


class TieneOrdenPendienteFilter(admin.SimpleListFilter):
    title = _('orden pendiente')
    parameter_name = 'orden_pendiente'

    def lookups(self, request, model_admin):
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.filter(
                orden_numero__isnull=False,
                inscripcion_numero__isnull=True)
        if self.value() == 'no':
            return queryset.exclude(
                orden_numero__isnull=False,
                inscripcion_numero__isnull=True)


class TieneAntecedentesFilter(admin.SimpleListFilter):
    title = _('tiene antecedentes')
    parameter_name = 'antecedente'

    def lookups(self, request, model_admin):
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.filter(antecedente__isnull=False)
        if self.value() == 'no':
            return queryset.filter(antecedente__isnull=True)


class TieneObjetoFilter(admin.SimpleListFilter):
    title = _('tiene objeto')
    parameter_name = 'objeto'

    def lookups(self, request, model_admin):
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.filter(expedienteobjeto__isnull=False)
        if self.value() == 'no':
            return queryset.filter(expedienteobjeto__isnull=True)


class TienePlanoFilter(admin.SimpleListFilter):
    title = _('tiene plano cargado')
    parameter_name = 'plano'

    def lookups(self, request, model_admin):
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.exclude(plano_ruta__isnull=True)
        if self.value() == 'no':
            return queryset.exclude(plano_ruta__isnull=False)


class TieneSetFilter(admin.SimpleListFilter):
    title = _('tiene informe cargado')
    parameter_name = 'informe'

    def lookups(self, request, model_admin):
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.exclude(set_ruta__isnull=True)
        if self.value() == 'no':
            return queryset.exclude(set_ruta__isnull=False)


# Personas
class CantidadDeExpedientesPorPersonaFilter(admin.SimpleListFilter):
    title = _('cantidad de expedientes por persona')
    parameter_name = 'expedientes'

    def lookups(self, request, model_admin):
        return (
            ('0', _('Ninguno')),
            ('1', _('1')),
            ('2', _('2')),
            ('3', _('3')),
            ('4+', _('4 o +')),
        )

    def queryset(self, request, queryset):
        qs = queryset.annotate(entry_count=Count('expedientepersona'))
        if self.value() == '0':
            qs = qs.filter(entry_count=0)
            return qs
        if self.value() == '1':
            qs = qs.filter(entry_count=1)
            return qs
        if self.value() == '2':
            qs = qs.filter(entry_count=2)
            return qs
        if self.value() == '3':
            qs = qs.filter(entry_count=3)
            return qs
        if self.value() == '4+':
            qs = qs.filter(entry_count__gt=3)
            return qs


# Objetos
class CantidadDeExpedientesPorObjetoFilter(admin.SimpleListFilter):
    title = _('cantidad de expedientes por objeto')
    parameter_name = 'expedientes'

    def lookups(self, request, model_admin):
        return (
            ('0', _('Ninguno')),
            ('10', _('entre 1 y 10')),
            ('50', _('entre 10 y 50')),
            ('100', _('entre 50 y 100')),
            ('100+', _('100 o +')),
        )

    def queryset(self, request, queryset):
        qs = queryset.annotate(entry_count=Count('expedienteobjeto'))
        if self.value() == '0':
            qs = qs.filter(entry_count=0)
            return qs
        if self.value() == '10':
            qs = qs.filter(entry_count__gte=1).filter(entry_count__lt=10)
            return qs
        if self.value() == '50':
            qs = qs.filter(entry_count__gte=10).filter(entry_count__lt=50)
            return qs
        if self.value() == '100':
            qs = qs.filter(entry_count__gte=50).filter(entry_count__lt=100)
            return qs
        if self.value() == '100+':
            qs = qs.filter(entry_count__gte=100)
            return qs


class AntecedenteAdmin(admin.ModelAdmin):
    list_filter = [
        'inscripcion_numero',
        'duplicado',
        TienePlanoFilter,
        ]
    list_display = (
        'expediente',
        'expediente_modificado',
        'inscripcion_numero',
        'duplicado',
        'obs',
        'ver_plano')
#    list_editable = (
#        'expediente_modificado',
#        'inscripcion_numero',
#        'duplicado',
#        'obs')
#        'plano_ruta')
    search_fields = ['expediente__id', 'expediente_modificado__id',
                     'inscripcion_numero', 'duplicado', 'obs']
    actions_on_bottom = True
    list_per_page = 20
    save_on_top = True
    ordering = ['expediente', '-expediente_modificado', 'inscripcion_numero']

    def ver_plano(self, obj):
        if obj.plano != '' and obj.plano is not None:
            return '<a href="%s">%s</a>' % (obj.plano.url,
                                            obj.inscripcion_numero)
        else:
            return None
    ver_plano.allow_tags = True
    ver_plano.short_description = 'Ver plano'
    ver_plano.admin_order_field = 'plano'
admin.site.register(Antecedente, AntecedenteAdmin)


class CatastroAdmin(admin.ModelAdmin):
    list_filter = [
        'zona', 'seccion', 'poligono', 'manzana', 'parcela', 'subparcela']
    search_fields = [
        'zona', 'seccion', 'poligono', 'manzana', 'parcela', 'subparcela']
    actions_on_bottom = True
    list_per_page = 20
    save_on_top = True
    ordering = ['zona', 'seccion', 'poligono',
                'manzana', 'parcela', 'subparcela']
admin.site.register(Catastro, CatastroAdmin)


class CatastroLocalAdmin(NestedModelAdmin):
    list_display = (
        'seccion', 'manzana', 'parcela', 'subparcela', 'suburbana', 'poligono')
    list_filter = ['seccion', 'manzana']
    search_fields = [
        'seccion',
        'manzana',
        'parcela',
        'subparcela',
        'suburbana',
        'poligono',
        'expediente_lugar__expediente__id',
        'expediente_lugar__lugar__nombre']
    actions_on_bottom = True
    list_per_page = 20
    save_on_top = True
    ordering = ['seccion', 'manzana', 'parcela',
                'subparcela', 'suburbana', 'poligono']
admin.site.register(CatastroLocal, CatastroLocalAdmin)


class CircunscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'orden')
    #list_editable = ('nombre', 'orden')
    search_fields = ['id', 'nombre', 'orden']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Circunscripcion, CircunscripcionAdmin)


admin.site.register(Comprobante)


class DpAdmin(admin.ModelAdmin):
    list_display = ('dp', 'nombre', 'habitantes', 'superficie', 'cabecera',
                    'circunscripcion')
    list_filter = ['circunscripcion', 'circunscripcion__orden']
    search_fields = ['dp', 'nombre', 'habitantes', 'superficie', 'cabecera',
                     'circunscripcion__nombre']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Dp, DpAdmin)


class DsAdmin(admin.ModelAdmin):
    list_display = ('id', 'dp', 'distrito', 'nombre')
    list_filter = ['dp', 'dp__nombre']
    search_fields = ['dp__nombre', 'ds', 'nombre']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Ds, DsAdmin)


class SdAdmin(admin.ModelAdmin):
    list_display = ('id', 'dp', 'ds', 'subdistrito', 'dp_nombre', 'ds_nombre',
                    'nombre')
    list_filter = ['ds__dp', 'ds__dp__nombre', 'ds', 'ds__nombre']
    search_fields = ['ds__dp__nombre', 'ds__nombre', 'sd', 'nombre']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Sd, SdAdmin)


class CatastroLocalInline(NestedStackedInline):
    model = CatastroLocal
    extra = 0


class ExpedienteLugarInline(NestedStackedInline):
    classes = ('grp-collapse grp-open',)
    model = ExpedienteLugar
    extra = 0
    inlines = [CatastroLocalInline]


class ExpedienteObjetoInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = ExpedienteObjeto
    extra = 0


class ExpedientePersonaInline(NestedStackedInline):
    classes = ('grp-collapse grp-open',)
    model = ExpedientePersona
    extra = 0
    ordering = ['-comitente']


class ExpedienteProfesionalInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = ExpedienteProfesional
    extra = 0


class CatastroInline(NestedStackedInline):
    model = Catastro
    extra = 0


class ExpedientePartidaInline(NestedStackedInline):
    classes = ('grp-collapse grp-open',)
    model = ExpedientePartida
    extra = 0
    inlines = [CatastroInline]


class AntecedenteInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = Antecedente
    fk_name = 'expediente'
    extra = 0
    ordering = ['-expediente_modificado', '-inscripcion_numero']


class PagoInline(NestedStackedInline):
    model = Pago
    extra = 0


class PresupuestoInline(NestedStackedInline):
    model = Presupuesto
    extra = 0
    inlines = [PagoInline]


class ExpedienteAdmin(NestedModelAdmin):
    fieldsets = [
        (None, {
            'fields': [('id', 'fecha_plano', 'created', 'modified')],
            'classes': ('wide', 'extrapretty'),
        }),
        ('Estado', {
            'fields': [('fecha_medicion', )],
            'classes': ('wide', 'extrapretty'),
        }),
        ('SCIT - Servicio de Catastro e Información Territorial', {
            'fields': [('inscripcion_numero', 'inscripcion_fecha', 'duplicado', 'sin_inscripcion')],
            'classes': ('wide', 'extrapretty', 'grp-collapse grp-open',),
        }),
        ('Orden de Trabajo CoPA - Colegio de Profesionales de la Agrimensura', {
            'fields': [('orden_numero', 'orden_fecha')],
            'classes': ('wide', 'extrapretty', 'grp-collapse grp-open',),
        }),
        ('Otros', {
            'fields': [('cancelado', 'cancelado_por'), ('plano', 'ver_plano')],
            'classes': ('wide', 'extrapretty', 'grp-collapse grp-open',),
        }),
    ]
    readonly_fields = ('created', 'modified', 'ver_plano')
    inlines = [
        ExpedienteLugarInline,
        ExpedienteObjetoInline,
        ExpedientePersonaInline,
        ExpedienteProfesionalInline,
        ExpedientePartidaInline,
        AntecedenteInline]
    list_display = (
        'id',
        'fecha_medicion',
        'fecha_plano',
        'inscripcion_numero',
        'inscripcion_fecha',
        'duplicado',
        'sin_inscripcion',
        'orden_numero',
        'orden_fecha',
        'cancelado',
        'ver_plano')
        #'plano_ruta')
    list_editable = (
#       'fecha_medicion',
#        'fecha_plano',
#        'inscripcion_numero',
#        'inscripcion_fecha',
#        'duplicado',
#        'orden_numero',
#        'orden_fecha',
#        'sin_inscripcion',
#        'cancelado',
#        'plano_ruta'
    )
    list_filter = [InscriptoFilter, 'duplicado', 'sin_inscripcion',
                   TieneOrdenFilter, TieneOrdenPendienteFilter, 'cancelado',
                   'cancelado_por', TienePlanoFilter,
                   'expedientelugar__lugar__nombre',
                   'expedientelugar__catastrolocal__seccion',
                   'expedientelugar__catastrolocal__manzana',
                   'expedientelugar__catastrolocal__parcela',
                   'expedientepersona__usufructo',
                   TieneObjetoFilter, TieneAntecedentesFilter]
    search_fields = [
        'id',
        'fecha_plano',
        'inscripcion_numero',
        'inscripcion_fecha',
        'orden_numero',
        'orden_fecha',
        'cancelado_por',
        'expedientelugar__lugar__nombre',
        'expedientepersona__persona__apellidos',
        'expedientepersona__persona__nombres',
        'expedientepersona__persona__apellidos_alternativos',
        'expedientepersona__persona__nombres_alternativos',
        'expedienteprofesional__profesional__apellidos',
        'expedienteobjeto__objeto__nombre',
        'expedientepartida__partida__pii',
        'antecedente__expediente_modificado__id',
        'antecedente__inscripcion_numero']
    actions_on_bottom = True
    date_hierarchy = 'inscripcion_fecha'
    list_per_page = 20
    save_on_top = True

    def ver_plano(self, obj):
        if obj.plano != '' and obj.plano is not None:
            return '<a href="%s">%s</a>' % (obj.plano.url,
                                            obj.inscripcion_numero)
        else:
            return None
    ver_plano.allow_tags = True
    ver_plano.short_description = 'Ver plano'
    ver_plano.admin_order_field = 'plano'
admin.site.register(Expediente, ExpedienteAdmin)


class ExpedienteLugarAdmin(admin.ModelAdmin):
    inlines = [CatastroLocalInline]
    list_display = ('expediente', 'lugar')
    list_filter = ['catastrolocal__seccion', 'catastrolocal__manzana',
                   'catastrolocal__parcela', 'lugar__nombre']
    search_fields = ['expediente__id', 'lugar__nombre']
    actions_on_bottom = True
    list_per_page = 20
    save_on_top = True
admin.site.register(ExpedienteLugar, ExpedienteLugarAdmin)


class ExpedientePartidaAdmin(admin.ModelAdmin):
    inlines = [CatastroInline]
    list_display = ('expediente', 'partida', 'ver_informe_catastral')
    list_filter = [TieneSetFilter,]
    search_fields = ['expediente__id', 'partida__pii',]
    list_select_related = True
    list_per_page = 20

    def ver_informe_catastral(self, obj):
        if obj.informe_catastral != '' and obj.informe_catastral is not None:
            return '<a href="%s">%s</a>' % (obj.informe_catastral, obj.partida)
        else:
            return None
    ver_informe_catastral.allow_tags = True
    ver_informe_catastral.short_description = 'Informe Catastral'
    ver_informe_catastral.admin_order_field = 'partida'
admin.site.register(ExpedientePartida, ExpedientePartidaAdmin)


class LugarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'obs')
    list_editable = ('obs',)
    search_fields = ['nombre', 'obs']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Lugar, LugarAdmin)


class ObjetoAdmin(admin.ModelAdmin):
    list_filter = [CantidadDeExpedientesPorObjetoFilter]
    search_fields = ['nombre']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Objeto, ObjetoAdmin)

admin.site.register(Pago)


class PartidaDominioInline(admin.TabularInline):
    model = PartidaDominio
    extra = 0


class PartidaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [('sd', 'pii', 'subpii', 'api')]}),
    ]
    readonly_fields = ('api', )
    inlines = [PartidaDominioInline]
    #list_display = ('id', 'sd', 'pii', 'subpii', 'api')
    list_filter = ['sd__ds__dp__nombre']
    search_fields = [
        'pii', 'sd__nombre', 'sd__ds__nombre', 'sd__ds__dp__nombre']
    actions_on_bottom = True
    save_on_top = True
    list_per_page = 20
    list_select_related = True
admin.site.register(Partida, PartidaAdmin)


class PersonaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
         'fields': [('apellidos', 'nombres'), ('apellidos_alternativos', 'nombres_alternativos')]
        }),
        ('Contacto', {
         'fields': [('domicilio', 'lugar'), ('telefono', 'celular'), 'email']
        }),
        ('DNI/CUIT/CUIL/CDI', {
         'fields': [('tipo_doc', 'documento'), 'cuit_cuil']
        }),
    ]
    inlines = [ExpedientePersonaInline]
    list_display = ('nombre_completo', 'domicilio', 'lugar', 'show_telefono',
                    'celular', 'email', 'show_tipo_doc', 'documento',
                    'show_cuit')
    list_filter = [CantidadDeExpedientesPorPersonaFilter, 'lugar']
    search_fields = [
        'nombres',
        'apellidos',
        'nombres_alternativos',
        'apellidos_alternativos',
        'domicilio',
        'telefono',
        'celular',
        'email',
        'cuit_cuil',
        'expedientepersona__expediente__id']
    actions_on_bottom = True
    save_on_top = True

    def show_telefono(self, obj):
        if obj.telefono == '' or obj.telefono is None:
            if obj.nombres == '' or obj.nombres is None:
                return '<a href="http://www.paginasblancas.com.ar/es-ar/persona/%s/santa-fe">buscar</a>' % strip_accents(
                    obj.apellidos.replace(
                        '.',
                        ''))
            else:
                return '<a href="http://www.paginasblancas.com.ar/es-ar/persona/%s-%s/santa-fe">buscar</a>' % (strip_accents(
                    obj.nombres.split(' ')[0].replace(
                        '.',
                        '')),
                    strip_accents(
                    obj.apellidos.split(' ')[0].replace(
                        '.',
                        '')))
        else:
            return obj.telefono
    show_telefono.allow_tags = True
    show_telefono.short_description = 'Telefono'
    show_telefono.admin_order_field = 'telefono'

    def show_cuit(self, obj):
        if obj.cuit_cuil == '' or obj.cuit_cuil is None:
            nombre = strip_accents(obj.nombres.replace('.', ''))
            apellido = strip_accents(
                obj.apellidos.replace(
                    '.', '').replace(
                    ' SA', '').replace(
                    ' SRL', '').replace(
                    ' SCC', '').replace(
                    ' SACIFI', '').replace(
                    ' SH', '').replace(
                    ' HNOS', ''))
            return '<a href="http://www.cuitonline.com/search.php?q=%s+%s">buscar</a>' % (
                nombre, apellido)
        else:
            cuit_cuil = obj.cuit_cuil.replace('-', '')
            return '<a href="http://www.cuitonline.com/constancia/inscripcion/%s">%s</a>' % (
                cuit_cuil, obj.cuit_cuil)
    show_cuit.allow_tags = True
    show_cuit.short_description = 'CUIT/CUIL/CDI'
    show_cuit.admin_order_field = 'cuit_cuil'
admin.site.register(Persona, PersonaAdmin)


class ProfesionalAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
         'fields': [('apellidos', 'nombres'),
                    ('titulo', 'icopa')]}),
        ('Contacto', {
         'fields': [('domicilio', 'lugar'),
                    ('telefono', 'celular'),
                    ('email', 'web')]}),
        ('DNI/CUIT/CUIL/CDI', {
         'fields': ['cuit_cuil']}),
        ('Otra info', {
         'fields': [('habilitado', 'jubilado', 'fallecido')]}),
    ]
    list_display = (
        'nombre_completo',
        'titulo',
        'icopa',
        'domicilio',
        'lugar',
        'telefono',
        'celular',
        'email',
        'web',
        'cuit_cuil')
    list_filter = [
        'habilitado', 'jubilado', 'fallecido', 'titulo__nombre', 'lugar']
    search_fields = ['nombres', 'apellidos', 'icopa', 'domicilio',
                     'telefono', 'celular', 'email', 'web', 'cuit_cuil']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Profesional, ProfesionalAdmin)


class PresupuestoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
         'fields': [('expediente'),
                    ('monto', 'fecha', 'porcentaje_cancelado'),
                    ('obs')]}), ]
    inlines = [PagoInline]
    list_display = (
        'expediente', 'monto', 'fecha', 'porcentaje_cancelado', 'obs')
    list_filter = ['expediente__id']
    search_fields = ['expediente__id']
    actions_on_bottom = True
    date_hierarchy = 'fecha'
    list_per_page = 20
    save_on_top = True
admin.site.register(Presupuesto, PresupuestoAdmin)
admin.site.register(Titulo)


class ZonaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion')
    search_fields = ['id', 'descripcion']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Zona, ZonaAdmin)
