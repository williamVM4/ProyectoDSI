from email.headerregistry import Group
from multiprocessing import context
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView
from apps.monitoreo.models import estadoCuenta
from apps.autenticacion.mixins import *
from .forms import *
from .models import *
from django.shortcuts import redirect, render
from django.contrib import messages

from apps.inventario.models import detalleVenta
# Create your views here.

class caja(GroupRequiredMixin,TemplateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema',u'Operador del sistema']
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
    
    model = prima
    template_name = 'facturacion/agregarPrima.html'
    form_class = agregarPrimaForm
    second_form_class = pagoForm
    third_form_class = lotePagoForm
    def get_context_data(self, **kwargs): 
        context = super(agregarPrima, self).get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(initial={'id':self.kwargs.get('id',None)})
        if 'form3' not in context:
            context['form3'] = self.third_form_class(initial={'id': self.kwargs.get('id', None)})
        return context

    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        return reverse_lazy('caja', kwargs={'idp': idp})


    def form_valid(self, request, *arg, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        form3 = self.third_form_class(request.POST)
        detalle = detalleVenta.objects.filter(lote = form3).filter(estado = 'True')
        estaC = estadoCuenta.objects.get(detalleVenta = detalle)
        form.detalleVenta = estaC
        form.save() 


"""        try:
            
            
            messages.success(self.request, 'La prima fue registrada con exito')
        except Exception:
            primaP.delete()
            messages.error(self.request, 'Ocurrió un error al guardar la prima')
        return HttpResponseRedirect(self.get_url_redirect())"""

class agregarPagoMantenimiento(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema',u'Operador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    model = pagoMantenimiento
    form_class = agregarPagoMantenimientoForm
    second_form_class = pagoForm
    third_form_class = lotePagoForm
    template_name = 'facturacion/agregarPagoMantenimiento.html'

    def get_context_data(self, **kwargs):
        context = super(agregarPagoMantenimiento, self).get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(id = idp)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(id = idp)
        context['idp'] = idp
        return context 
    
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        return reverse_lazy('caja', kwargs={'idp': idp})

    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
        lote = self.third_form_class(self.request.POST)
        detalle = detalleVenta.objects.filter(lote = lote.cleaned_data['lote']).filter(estado = 'True')
        estaC = estadoCuenta.objects.filter(detalleVenta = detalle)
        pagoM = form.save(commit=False)
        pago = self.second_form_class(self.request.POST)
        pago.fields['pagoMantenimiento'] = pagoM
        pago.save()

    
    

    
    

    