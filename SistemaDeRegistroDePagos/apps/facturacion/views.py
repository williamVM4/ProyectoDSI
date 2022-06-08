from email.headerregistry import Group
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView
from apps.autenticacion.mixins import *
from .forms import *
from .models import *
from django.shortcuts import redirect, render
from django.contrib import messages

from apps.inventario.models import detalleVenta
# Create your views here.

class caja(GroupRequiredMixin,TemplateView):
    group_required = [u'Configurador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    template_name = 'facturacion/caja.html'

    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('idp', None) 
        context['idp'] = id
        context['pagosM'] = pagoMantenimiento.objects.all()
        context['pagosF'] = pagoFinanciamiento.objects.all()     
        return context

        

class agregarPrima(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
  
    template_name = 'facturacion/agregarPrima.html'
    form_class = agregarPrimaForm
    second_form_class = lote


    #success_url = reverse_lazy('')
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('id', None) 
        try:
            detalleVenta.objects.get(pk = id)
            return reverse_lazy('detalleLote', kwargs={'pk': id})
        except Exception:
            return reverse_lazy('gestionarLotes')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('id', None)
        idp = self.kwargs.get('idp', None) 
        context['idp'] = idp
        context['id'] = id         
        return context

    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
         # recojo el parametro 
        id = self.kwargs.get('id', None) 
        prima = form.save(commit=False)
        #poner try
        try:
            detalle = detalleVenta.objects.get(pk = id)
            prima.detalleVenta = detalle 
            prima.save()
            
            messages.success(self.request, 'La prima fue registrada con exito')
        except Exception:
            prima.delete()
            messages.error(self.request, 'Ocurrió un error al guardar la prima')
        return HttpResponseRedirect(self.get_url_redirect())

""" class agregarPagoMantenimiento(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    model = pagoMantenimiento
    form_class = agregarPagoMantenimientoForm
    template_name = 'facturacion/agregarPagoMantenimiento.html'"""
    
    

    
    

    