from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from gea.models import Persona, Expediente, ExpedientePersona

def index(request):
    latest_exp_list = Expediente.objects.order_by('-id')[:5]
    template = loader.get_template('gea/index.html')
    context = Context({
        'latest_exp_list': latest_exp_list,
    })
    return HttpResponse(template.render(context))
