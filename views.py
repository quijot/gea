from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django import forms
from django.db.models import Count, Q

from .models import Expediente, Persona, Objeto, Lugar, Partida, CatastroLocal
from .gea_vars import CP, CP_DEFAULT, CP_dict, PROV, PROV_DEFAULT, CIRC, \
CIRC_DEFAULT, NOTA, LUGAR, Lugar_dict

from django.views.generic import TemplateView, ListView, DetailView


class CounterMixin(object):

    def get_context_data(self, **kwargs):
        context = super(CounterMixin, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context


class NumeroSearchMixin(object):

    def get_queryset(self):
        qset = super(NumeroSearchMixin, self).get_queryset()
        q = self.request.GET.get('search')
        if q:
            q = q.split(' ')
            for w in q:
                qset = qset.filter(
                    Q(id__contains=w) |
                    Q(inscripcion_numero__contains=w) |
                    Q(expedientepartida__partida__pii__contains=w) |
                    Q(expedientepersona__persona__nombres__icontains=w) |
                    Q(expedientepersona__persona__apellidos__icontains=w) |
                    Q(expedientelugar__lugar__nombre__icontains=w)
                ).distinct()
        return qset


class ExpedienteAbiertoMixin(object):

    def get_queryset(self):
        qset = super(ExpedienteAbiertoMixin, self).get_queryset()
        qset = qset.filter(
            Q(inscripcion_numero__isnull=True) &
            Q(cancelado=False) &
            Q(sin_inscripcion=False)
        )[:10]
        return qset


class Home(CounterMixin, NumeroSearchMixin, ExpedienteAbiertoMixin,
           ListView):
    template_name = 'home/index.html'
    model = Expediente
        
    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(*args, **kwargs)
        # last 5 inscriptos
        context['insc_list'] = Expediente.objects.filter(Q(inscripcion_numero__isnull=False) &
                                                         Q(inscripcion_fecha__isnull=False)).order_by('-inscripcion_fecha', 'inscripcion_numero')[:5]
        # ordenes pendientes
        context['ord_list'] = Expediente.objects.filter(Q(orden_numero__isnull=False) &
                                                        Q(inscripcion_numero__isnull=True) &
                                                        Q(orden_fecha__isnull=False)).order_by('-orden_fecha', 'orden_numero')[:5]
        # relevamientos
        context['relev_list'] = Expediente.objects.filter(fecha_medicion__isnull=False).order_by('-fecha_medicion')[:5]
        return context 

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Home, self).dispatch(*args, **kwargs)


class About(TemplateView):
    template_name = 'home/about.html'


class ExpedienteMixin(object):

    def get_queryset(self):
        qset = super(ExpedienteMixin, self).get_queryset()
        q = self.request.GET.get('pendiente')
        if q:  # orden pendiente
            qset = qset.filter(
                Q(inscripcion_numero__isnull=q) &
                Q(orden_numero__isnull=not q)
            )
        q = self.request.GET.get('inscripto')
        if q:  # plano inscripto
            qset = qset.filter(inscripcion_numero__isnull=not q)
        q = self.request.GET.get('cancelado')
        if q:  # expediente cancelado
            qset = qset.filter(cancelado=q)
        q = self.request.GET.get('duplicado')
        if q:  # duplicado
            qset = qset.filter(duplicado=q)
        q = self.request.GET.get('sin_inscr')
        if q:  # sin inscripcion
            qset = qset.filter(sin_inscripcion=q)
        return qset


class ExpedienteList(CounterMixin, NumeroSearchMixin, ExpedienteMixin,
                     ListView):
    template_name = 'lists/expediente_list.html'
    model = Expediente
    paginate_by = 10

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class
        property value.
        """
        return self.request.GET.get('paginate_by', self.paginate_by)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExpedienteList, self).dispatch(*args, **kwargs)


class ExpedienteDetail(DetailView):
    template_name = 'lists/expediente_detail.html'
    model = Expediente

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExpedienteDetail, self).dispatch(*args, **kwargs)


class NombreSearchMixin(object):

    def get_queryset(self):
        qset = super(NombreSearchMixin, self).get_queryset()
        q = self.request.GET.get('search')
        if q:
            q = q.split(' ')
            for w in q:
                qset = qset.filter(
                    Q(nombres__icontains=w) |
                    Q(apellidos__icontains=w) |
                    Q(nombres_alternativos__icontains=w) |
                    Q(apellidos_alternativos__icontains=w) |
                    Q(expedientepersona__expediente__id__contains=w) |
                    Q(expedientepersona__expediente__inscripcion_numero__contains=w) |
                    Q(expedientepersona__expediente__expedientepartida__partida__pii__contains=w) |
                    Q(expedientepersona__expediente__expedientelugar__lugar__nombre__icontains=w)
                ).distinct()
        return qset


class PersonaList(CounterMixin, NombreSearchMixin, ListView):
    template_name = 'lists/persona_list.html'
    model = Persona
    paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonaList, self).dispatch(*args, **kwargs)


class PersonaDetail(DetailView):
    template_name = 'lists/persona_detail.html'
    model = Persona

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonaDetail, self).dispatch(*args, **kwargs)


class LugarSearchMixin(object):

    def get_queryset(self):
        queryset = super(LugarSearchMixin, self).get_queryset()
        q = self.request.GET.get('lugar')
        if q:
            return queryset.filter(expedientelugar__lugar__nombre=q)
        return queryset


class SeccionSearchMixin(object):

    def get_queryset(self):
        queryset = super(SeccionSearchMixin, self).get_queryset()
        q = self.request.GET.get('seccion')
        if q:
            return queryset.filter(expedientelugar__catastrolocal__seccion=q)
        return queryset


class ManzanaSearchMixin(object):

    def get_queryset(self):
        queryset = super(ManzanaSearchMixin, self).get_queryset()
        q = self.request.GET.get('manzana')
        if q:
            return queryset.filter(expedientelugar__catastrolocal__manzana=q)
        return queryset


class ParcelaSearchMixin(object):

    def get_queryset(self):
        queryset = super(ParcelaSearchMixin, self).get_queryset()
        q = self.request.GET.get('parcela')
        if q:
            return queryset.filter(expedientelugar__catastrolocal__parcela=q)
        return queryset


class CLMixin(object):

    def get_queryset(self):
        qset = super(CLMixin, self).get_queryset()
        q = self.request.GET.get('lugar')
        if q is not None:
            qset = qset.filter(expedientelugar__lugar__nombre=q).distinct()
        q = self.request.GET.get('seccion')
        if q is not None:
            qset = qset.filter(expedientelugar__catastrolocal__seccion=q)
        q = self.request.GET.get('manzana')
        if q is not None:
            qset = qset.filter(expedientelugar__catastrolocal__manzana=q)
        q = self.request.GET.get('parcela')
        if q is not None:
            qset = qset.filter(expedientelugar__catastrolocal__parcela=q)
        return qset


class CatastroLocalList(CounterMixin, CLMixin, ListView):
    template_name = 'lists/catastros_locales.html'
    model = Expediente
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CatastroLocalList, self).get_context_data(**kwargs)
        l = self.request.GET.get('lugar')
        context['lugar'] = l
        s = self.request.GET.get('seccion')
        context['seccion'] = s
        m = self.request.GET.get('manzana')
        context['manzana'] = m
        p = self.request.GET.get('parcela')
        context['parcela'] = p
        context['lugares'] = Lugar.objects.values_list('nombre',
          flat=True).order_by('nombre')
        context['secciones'] = CatastroLocal.objects.filter(
          expediente_lugar__lugar__nombre=l).values_list('seccion',
          flat=True).distinct().order_by('seccion')
        context['manzanas'] = CatastroLocal.objects.filter(
          expediente_lugar__lugar__nombre=l).filter(seccion=s).values_list(
          'manzana', flat=True).distinct().order_by('manzana')
        context['parcelas'] = CatastroLocal.objects.filter(
          expediente_lugar__lugar__nombre=l).filter(Q(seccion=s) &
          Q(manzana=m)).values_list(
          'parcela', flat=True).distinct().order_by('parcela')
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CatastroLocalList, self).dispatch(*args, **kwargs)


class CaratulaForm(forms.Form):
    expte_nro = forms.IntegerField(label='Expediente Nº',
        widget=forms.NumberInput(attrs={'placeholder': 'ej: 4300'}))
    inmueble = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'ej: Una fracción de terreno...'
        }), required=False)
    tomo = forms.IntegerField(required=False)
    par = forms.BooleanField(required=False)
    folio = forms.IntegerField(required=False)
    numero = forms.IntegerField(label='Número', required=False)
    fecha = forms.DateField(required=False)
    obs = forms.CharField(label='Observaciones',
        widget=forms.Textarea(attrs={
        'placeholder': 'ej: Modifica el Lote Nº 1 del Plano Nº 23.456. Etc.'
        }), required=False)


@login_required
def caratula(request):
    if request.method == 'POST':  # If the form has been submitted...
        # CaratulaForm was defined in the previous section
        form = CaratulaForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            expediente_id = form.cleaned_data['expte_nro']
            inmueble = form.cleaned_data['inmueble']
            tomo = form.cleaned_data['tomo']
            par = form.cleaned_data['par']
            folio = form.cleaned_data['folio']
            numero = form.cleaned_data['numero']
            fecha = form.cleaned_data['fecha']
            obs = form.cleaned_data['obs']

            e = get_object_or_404(Expediente, id=expediente_id)
            template = loader.get_template('tools/caratula.html')
            context = Context({
                'e': e,
                'inmueble': inmueble,
                'tomo': tomo,
                'par': par,
                'folio': folio,
                'numero': numero,
                'fecha_dominio': fecha,
                'obs': obs,
            })
            return HttpResponse(template.render(context))
    else:
        form = CaratulaForm()  # An unbound form

    return render(request, 'tools/caratula_form.html', {
        'form': form,
    })


class SolicitudForm(forms.Form):
    expte_nro = forms.IntegerField(label='Expediente Nº',
        widget=forms.NumberInput(attrs={'placeholder': 'ej: 4300'}))
    circunscripcion = forms.ChoiceField(label='Circunscripción', choices=CIRC, initial=CIRC_DEFAULT)
    domicilio_fiscal = forms.CharField(max_length=40, widget=forms.TextInput(
        attrs={'placeholder': 'ej: San Martín 430'}))
    localidad = forms.ChoiceField(choices=CP, initial=CP_DEFAULT)
    provincia = forms.ChoiceField(choices=PROV, initial=PROV_DEFAULT)
    nota_titulo = forms.ChoiceField(label='Nota título', choices=NOTA)
    nota = forms.CharField(label='Nota contenido',
        widget=forms.Textarea(attrs={
        'placeholder': 'Ingrese el texto de la nota correspondiente'
        }), required=False)


@login_required
def solicitud(request):
    if request.method == 'POST':  # If the form has been submitted...
        # SolicitudForm was defined in the previous section
        form = SolicitudForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            expediente_id = form.cleaned_data['expte_nro']
            circunscripcion = form.cleaned_data['circunscripcion']
            domicilio_fiscal = form.cleaned_data['domicilio_fiscal']
            # codigo_postal = form.cleaned_data['localidad']
            loc = form.cleaned_data['localidad']
            localidad = CP_dict[loc].split(' - ')[0]
            codigo_postal = CP_dict[loc].split(' - ')[1]
            provincia = form.cleaned_data['provincia']
            nota_titulo = form.cleaned_data['nota_titulo']
            nota = form.cleaned_data['nota']

            e = get_object_or_404(Expediente, id=expediente_id)
            template = loader.get_template('doc/solic.html')
            context = Context({
                'e': e,
                'domfiscal': domicilio_fiscal,
                'circunscripcion': circunscripcion,
                'localidad': localidad,
                'cp': codigo_postal,
                'provincia': provincia,
                'nota_titulo': nota_titulo,
                'nota': nota,
            })
            return HttpResponse(template.render(context))
    else:
        form = SolicitudForm()  # An unbound form

    return render(request, 'doc/solic_form.html', {
        'form': form,
    })


class VisacionForm(forms.Form):
    expte_nro = forms.IntegerField(label='Expediente Nº')
    lugar = forms.ChoiceField(choices=LUGAR, initial=0)


@login_required
def visacion(request):
    if request.method == 'POST':  # If the form has been submitted...
        # VisacionForm was defined in the previous section
        form = VisacionForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            eid = form.cleaned_data['expte_nro']
            lugar = form.cleaned_data['lugar']
            sr = Lugar_dict[int(lugar)][0]
            localidad = Lugar_dict[int(lugar)][1]

            e = get_object_or_404(Expediente, id=eid)
            # Redirect after POST
            return render_to_response('doc/visac.html', {
                "e": e,
                "sr": sr,
                "localidad": localidad
            }, context_instance=RequestContext(request))
    else:
        form = VisacionForm()  # An unbound form

    return render(request, 'doc/visac_form.html', {
        'form': form,
    })


#
# Buscar Plano por Nro
#
ftp_url = 'ftp://zentyal.estudio.lan'


class PlanoForm(forms.Form):
    circ = forms.IntegerField(label='Circunscripción', min_value=1, max_value=2, initial=1)
    n_insc = forms.IntegerField(label='Plano Nº', min_value=1, max_value=999999)


@login_required
def plano(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = PlanoForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            circ = form.cleaned_data['circ']
            nro = form.cleaned_data['n_insc']
            return HttpResponseRedirect(
                '%s/planos/%s/%06d.pdf' % (ftp_url, circ, nro))
    else:
        form = PlanoForm()  # An unbound form

    return render(request, 'search/plano_form.html', {
        'form': form,
    })


#
# Buscar Set de Datos por PII
#
class SetForm(forms.Form):
    partida = forms.IntegerField(min_value=1, max_value=999999)
    sub_pii = forms.IntegerField(label='Subpartida', min_value=0, max_value=9999, initial=0)


@login_required
def set(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = SetForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            pii = form.cleaned_data['partida']
            sub_pii = form.cleaned_data['sub_pii']
            return HttpResponseRedirect(
                '%s/set/%06d%04d.pdf' % (ftp_url, pii, sub_pii))
    else:
        form = SetForm()  # An unbound form

    return render(request, 'search/set_form.html', {
        'form': form,
    })


#
# Calcular Digito Verificador de la PII
#
class DVAPIForm(forms.Form):
    dp = forms.IntegerField(label='DP (departamento)', min_value=1, max_value=19, initial=11)
    ds = forms.IntegerField(label='DS (distrito)', min_value=1, max_value=99, initial=8)
    sd = forms.IntegerField(label='SD (subdistrito)', min_value=0, max_value=99, initial=0)
    partida = forms.IntegerField(min_value=1, max_value=999999)
    sub_pii = forms.IntegerField(label='Subpartida', min_value=0, max_value=9999, initial=0)


def get_dvapi(dp, ds, sd, pii, subpii):
    coef = '9731'
    _coef = coef + coef + coef + coef
    strpii = '%02d%02d%02d%06d%04d' % (dp, ds, sd, pii, subpii)
    suma = 0
    for i in range(0, len(strpii)):
        m = str(int(strpii[i]) * int(_coef[i]))
        suma += int(m[len(m) - 1])
    return (10 - (suma % 10)) % 10


def dvapi(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = DVAPIForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            dp = form.cleaned_data['dp']
            ds = form.cleaned_data['ds']
            sd = form.cleaned_data['sd']
            pii = form.cleaned_data['partida']
            sub_pii = form.cleaned_data['sub_pii']
            dv = get_dvapi(dp, ds, sd, pii, sub_pii)
            return render_to_response('tools/dvapi_form.html', {
                'dv': dv,
                'form': form
            }, context_instance=RequestContext(request))
    else:
        form = DVAPIForm()  # An unbound form

    return render(request, 'tools/dvapi_form.html', {
        'form': form,
    })


#
# Consultar estado en Sistema de Información de Expedientes del SCIT
#
class SIEForm(forms.Form):
    mesa = forms.IntegerField(min_value=13401, max_value=13401, initial=13401)
    nro = forms.IntegerField(label='Número', min_value=1, max_value=9999999)
    digito = forms.IntegerField(label='Dígito', min_value=0, max_value=9, initial=0)


def sie(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = SIEForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            mesa = form.cleaned_data['mesa']
            nro = form.cleaned_data['nro']
            dv = form.cleaned_data['digito']
            #dv = get_dvsie(mesa, nro)
            return HttpResponseRedirect(
                'https://www.santafe.gov.ar/index.php/apps/sie?mesa=%d&numero=%d&digito=%d' % (mesa, nro, dv))
    else:
        form = SIEForm()  # An unbound form

    return render(request, 'tools/sie_form.html', {
        'form': form,
    })


#
#
# Exptes x Catastro Local
#
#
class CLForm(forms.Form):
    lugar = forms.ModelChoiceField(queryset=Lugar.objects.exclude(
                nombre__startswith='Colonia').exclude(
                nombre__startswith='Zona Rural').exclude(
                nombre__startswith='Zona de Islas'), required=False)
    seccion = forms.CharField(max_length=4, required=False)
    manzana = forms.CharField(max_length=4, required=False)
    parcela = forms.CharField(max_length=4, required=False)


@login_required
def catastro(request):
    if request.method == 'POST':  # If the form has been submitted...
        # VisacionForm was defined in the previous section
        form = CLForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            lugar = form.cleaned_data['lugar']
            seccion = form.cleaned_data['seccion']
            manzana = form.cleaned_data['manzana']
            parcela = form.cleaned_data['parcela']

            filtro = u'?'
            if lugar is not None:
                filtro = u'%s%s%s' % (
                    filtro, u'&expedientelugar__lugar__nombre=', lugar)
            if seccion != '':
                filtro = u'%s%s%s' % (
                    filtro,
                    u'&expedientelugar__catastrolocal__seccion=',
                    seccion
                )
            if manzana != '':
                filtro = u'%s%s%s' % (
                    filtro,
                    u'&expedientelugar__catastrolocal__manzana=',
                    manzana
                )
            if parcela != '':
                filtro = u'%s%s%s' % (
                    filtro,
                    u'&expedientelugar__catastrolocal__parcela=',
                    parcela
                )
            # Redirect after POST
            return HttpResponseRedirect('/admin/gea/expediente/%s' % filtro)
    else:
        form = CLForm()  # An unbound form

    return render(request, 'tools/catastro_form.html', {
        'form': form,
    })


######
###### EXPERIMENTAL
######
from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

class QuerysetCalendar(HTMLCalendar):

    def __init__(self, queryset, datefield):
        self.datefield = datefield
        super(QuerysetCalendar, self).__init__()
        self.queryset_by_date = self.group_by_day(queryset)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.queryset_by_date:
                cssclass += ' filled'
                body = ['<ul>']
                for item in self.queryset_by_date[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % item.get_absolute_url())
                    body.append(esc(item))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', ' ')


    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(QuerysetCalendar, self).formatmonth(year, month)

    def group_by_day(self, queryset):
        field = lambda item: getattr(item, self.datefield).day
        return dict(
            [(day, list(items)) for day, items in groupby(queryset, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

#######

from django.utils.safestring import mark_safe


@login_required
def calendar(request, year, month):
    e = Expediente.objects.order_by('fecha_medicion').filter(
        fecha_medicion__year=year, fecha_medicion__month=month
        )
    cal = QuerysetCalendar(e, 'fecha_medicion').formatmonth(int(year), int(month))
    return render_to_response('tools/calendar.html', {'calendar': mark_safe(cal),})
