from email.headerregistry import Group
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView
from apps.autenticacion.mixins import *
from .forms import *
from django.shortcuts import redirect, render

# Create your views here.


class agregarPrima(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    model = prima
    form_class = agregarPrimaForm
    template_name = 'facturacion/agregarPrima.html'
    
    

    
    

    