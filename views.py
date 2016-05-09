#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render_to_response, \
    RequestContext

from django import forms
from django.db.models import Q, Count

from .models import Expediente, Persona, Objeto, Lugar, Partida, CatastroLocal
from .gea_vars import CP, CP_dict, PROV, CIRC, NOTA, LUGAR, Lugar_dict

from django.views.generic import TemplateView, ListView, DetailView

ftp_url = 'ftp://zentyal.estudio.lan'


class Home(TemplateView):
    template_name = 'portada.html'


class CounterMixin(object):

    def get_context_data(self, **kwargs):
        context = super(CounterMixin, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context


class NumeroSearchMixin(object):

    def get_queryset(self):
        queryset = super(NumeroSearchMixin, self).get_queryset()
        q = self.request.GET.get('search')
        if q:
            return queryset.filter(
                Q(id__contains=q) |
                Q(inscripcion_numero__contains=q)
            )
        return queryset


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
        if q:  # duplicado
            qset = qset.filter(sin_inscripcion=q)
        return qset


class ExpedienteList(CounterMixin, NumeroSearchMixin,
  ExpedienteMixin, ListView):
    template_name = 'expediente_list.html'
    model = Expediente
    paginate_by = 10

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class
        property value.
        """
        return self.request.GET.get('paginate_by', self.paginate_by)


class ExpedienteDetail(DetailView):
    template_name = 'expediente_detail.html'
    model = Expediente


class NombreSearchMixin(object):

    def get_queryset(self):
        queryset = super(NombreSearchMixin, self).get_queryset()
        q = self.request.GET.get('search')
        if q:
            q = q.split(' ')
            for w in q:
                queryset = queryset.filter(
                    Q(nombres__icontains=w) |
                    Q(apellidos__icontains=w) |
                    Q(nombres_alternativos__icontains=w) |
                    Q(apellidos_alternativos__icontains=w)
                )
        return queryset


class PersonaList(CounterMixin, NombreSearchMixin, ListView):
    template_name = 'persona_list.html'
    model = Persona
    paginate_by = 50


class PersonaDetail(DetailView):
    template_name = 'persona_detail.html'
    model = Persona


def listado_alfabetico(request, inicial=None):
    # datasets
    pers_list = Persona.objects.all().order_by('apellidos', 'nombres')
    # filtering
    if inicial is not None:
        pers_list = pers_list.filter(apellidos__istartswith=inicial)
    # pagination
    paginator = Paginator(pers_list, 50)
    page = request.GET.get('page')
    try:
        personas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        personas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        personas = paginator.page(paginator.num_pages)
    template = loader.get_template('listado_alfabetico.html')
    context = Context({
        'cl': personas,
        'inicial': inicial,
    })
    return HttpResponse(template.render(context))


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


#class CatastroLocalList(CounterMixin, LugarSearchMixin, SeccionSearchMixin,
#  ManzanaSearchMixin, ParcelaSearchMixin, ListView):
class CatastroLocalList(CounterMixin, CLMixin, ListView):
    template_name = 'catastros_locales.html'
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


def catastros_locales(request):
    return parcelas(request)


def lugares(request, l):
    return parcelas(request, l)


def secciones(request, l, s):
    return parcelas(request, l, s)


def manzanas(request, l, s, m):
    return parcelas(request, l, s, m)


def parcelas(request, l=None, s='all', m='all', p='all'):
    # datasets
    lugares = Lugar.objects.values_list('nombre', flat=True).filter(
        Q(expedientelugar__catastrolocal__seccion__isnull=False) |
        Q(expedientelugar__catastrolocal__manzana__isnull=False) |
        Q(expedientelugar__catastrolocal__parcela__isnull=False)
        ).distinct().order_by('nombre')
    exp_list = Expediente.objects.all().distinct().order_by(
        'expedientelugar__catastrolocal__seccion',
        'expedientelugar__catastrolocal__manzana',
        'expedientelugar__catastrolocal__parcela')
    secciones = CatastroLocal.objects.all()
    manzanas = CatastroLocal.objects.all()
    parcelas = CatastroLocal.objects.all()
    # filtering
    exp_list = exp_list.filter(expedientelugar__lugar__nombre=l)
    secciones = secciones.filter(expediente_lugar__lugar__nombre=l)
    manzanas = manzanas.filter(expediente_lugar__lugar__nombre=l)
    parcelas = parcelas.filter(expediente_lugar__lugar__nombre=l)
    if s is 'None':
        s = None
    if s != 'all':
        exp_list = exp_list.filter(expedientelugar__catastrolocal__seccion=s)
        manzanas = manzanas.filter(seccion=s)
        parcelas = parcelas.filter(seccion=s)
    if m is 'None':
        m = None
    if m != 'all':
        exp_list = exp_list.filter(expedientelugar__catastrolocal__manzana=m)
        parcelas = parcelas.filter(manzana=m)
    if p is 'None':
        p = None
    if p != 'all':
        exp_list = exp_list.filter(expedientelugar__catastrolocal__parcela=p)
    # ordering
    secciones = secciones.values_list(
        'seccion', flat=True).distinct().order_by('seccion')
    manzanas = manzanas.values_list(
        'manzana', flat=True).distinct().order_by('manzana')
    parcelas = parcelas.values_list(
        'parcela', flat=True).distinct().order_by('parcela')
    # pagination
    paginator = Paginator(exp_list, 10)
    page = request.GET.get('page')
    try:
        expedientes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        expedientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        expedientes = paginator.page(paginator.num_pages)
    template = loader.get_template('listado_catastros_locales.html')
    context = Context({
        'cl': expedientes,
        'lugares': lugares,
        'secciones': secciones,
        'manzanas': manzanas,
        'parcelas': parcelas,
        'lugar': l,
        'seccion': s,
        'manzana': m,
        'parcela': p,
    })
    return HttpResponse(template.render(context))


class CaratulaForm(forms.Form):
    expte_nro = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'ej: 4300'}))
    inmueble = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'ej: Una fracción de terreno...'
        }), required=False)
    tomo = forms.IntegerField(required=False)
    par = forms.BooleanField(required=False)
    folio = forms.IntegerField(required=False)
    numero = forms.IntegerField(required=False)
    fecha = forms.DateField(required=False)
    obs = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'ej: Modifica el Lote Nº 1 del Plano Nº 23.456. Etc.'
        }), required=False)


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
            template = loader.get_template('caratula.html')
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

    return render(request, 'caratula_form.html', {
        'form': form,
    })


class SolicitudForm(forms.Form):
    expte_nro = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'ej: 4300'}))
    circunscripcion = forms.ChoiceField(choices=CIRC, initial=u'SANTA FE')
    domicilio_fiscal = forms.CharField(max_length=40, widget=forms.TextInput(
        attrs={'placeholder': 'ej: San Martín 430'}))
    localidad = forms.ChoiceField(choices=CP, initial=u'GÁLVEZ')
    provincia = forms.ChoiceField(choices=PROV, initial=u'SANTA FE')
    nota_titulo = forms.ChoiceField(
        choices=NOTA, initial=u'DECLARATORIA DE HEREDEROS')
    nota = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Ingrese el texto de la nota correspondiente'
        }), required=False)


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
            template = loader.get_template('solic.html')
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

    return render(request, 'solic_form.html', {
        'form': form,
    })


class VisacionForm(forms.Form):
    expte_nro = forms.IntegerField()
    lugar = forms.ChoiceField(choices=LUGAR, initial=0)


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
            return render_to_response('visac.html', {
                "e": e,
                "sr": sr,
                "localidad": localidad
            }, context_instance=RequestContext(request))
    else:
        form = VisacionForm()  # An unbound form

    return render(request, 'visac_form.html', {
        'form': form,
    })


#
# Buscar Plano por Nro
#
class PlanoForm(forms.Form):
    circunscripcion = forms.IntegerField(min_value=1, max_value=2, initial=1)
    nro_inscripcion = forms.IntegerField(min_value=1, max_value=999999)


def plano(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = PlanoForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            circ = form.cleaned_data['circunscripcion']
            nro = form.cleaned_data['nro_inscripcion']
            return HttpResponseRedirect(
                '%s/planos/%s/%06d.pdf' % (ftp_url, circ, nro))
    else:
        form = PlanoForm()  # An unbound form

    return render(request, 'plano_form.html', {
        'form': form,
    })

#
# Buscar Set de Datos por PII
#


class SetForm(forms.Form):
    partida = forms.IntegerField(min_value=1, max_value=999999)
    sub_pii = forms.IntegerField(min_value=0, max_value=9999, initial=0)


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

    return render(request, 'set_form.html', {
        'form': form,
    })

#
# Calcular Digito Verificador de la PII
#


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
            return render_to_response('dvapi_form.html', {
                'dv': dv,
                'form': form
            }, context_instance=RequestContext(request))
    else:
        form = DVAPIForm()  # An unbound form

    return render(request, 'dvapi_form.html', {
        'form': form,
    })


class DVAPIForm(forms.Form):
    dp = forms.IntegerField(min_value=1, max_value=19, initial=11)
    ds = forms.IntegerField(min_value=1, max_value=99, initial=8)
    sd = forms.IntegerField(min_value=0, max_value=99, initial=0)
    partida = forms.IntegerField(min_value=1, max_value=999999)
    sub_pii = forms.IntegerField(min_value=0, max_value=9999, initial=0)

#
#
# Presupuestos
#
#


def presup(request, persona=None, objeto=None):
    # p = get_object_or_404(Persona, =eid)
    return render_to_response('presup.html', {
        "persona": persona,
        "objeto": objeto
    }, context_instance=RequestContext(request))


class PresupForm(forms.Form):
    persona = forms.ModelChoiceField(
        queryset=Persona.objects.all(), empty_label=None)
    objeto = forms.ModelChoiceField(
        queryset=Objeto.objects.all(), empty_label=None)
    lugar = forms.ModelChoiceField(queryset=Lugar.objects.all())
    partida = forms.ModelChoiceField(queryset=Partida.objects.all())
    monto = forms.FloatField(required=False)


def presup_form(request):
    if request.method == 'POST':  # If the form has been submitted...
            # VisacionForm was defined in the previous section
        form = PresupForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            persona = form.cleaned_data['persona']
            objeto = form.cleaned_data['objeto']
            # lugar = form.cleaned_data['lugar']
            # partida = form.cleaned_data['partida']
            # monto = form.cleaned_data['monto']

            # Redirect after POST
            return HttpResponseRedirect(
                '/gea/presup/%s/%s' % (persona, objeto))
    else:
        form = PresupForm()  # An unbound form

    return render(request, 'presup_form.html', {
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

    return render(request, 'catastro_form.html', {
        'form': form,
    })
