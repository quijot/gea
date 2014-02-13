from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from gea.models import Persona, Expediente, ExpedientePersona
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    exp_list   = Expediente.objects.order_by('-id')
    paginator = Paginator(exp_list, 20)
    page = request.GET.get('page')
    try:
        expedientes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        expedientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        expedientes = paginator.page(paginator.num_pages)
    template = loader.get_template('listado_comun.html')
    context  = Context({
        'cl': expedientes,
    })
    return HttpResponse(template.render(context))
