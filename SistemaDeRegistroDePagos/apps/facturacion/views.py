from email.headerregistry import Group
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView
from apps.autenticacion.mixins import *
from .forms import *
from .models import *
from django.shortcuts import redirect, render

# Create your views here.

class caja(GroupRequiredMixin,TemplateView):
    group_required = [u'Configurador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    template_name = 'facturacion/caja.html'

    def get_context_data(self, *args, **kwargs):
        pagosM = pagoMantenimiento.objects.all()
        pagosF = pagoFinanciamiento.objects.all()
        return {'pagosM': pagosM, 'pagosF': pagosF}

class agregarPrima(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    model = prima
    form_class = agregarPrimaForm
    template_name = 'facturacion/agregarPrima.html'

class agregarPagoMantenimiento(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    model = pagoMantenimiento
    form_class = agregarPagoMantenimientoForm
    template_name = 'facturacion/agregarPagoMantenimiento.html'
    
    

    
    

    