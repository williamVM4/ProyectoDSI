from email.headerregistry import Group
from multiprocessing import context
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView
from apps.monitoreo.models import estadoCuenta, cuotaEstadoCuenta
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
        context['prima'] = prima.objects.all()     
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


    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
        lote = self.third_form_class(self.request.POST)
        
        prima = form.save(commit=False)
        pago = self.second_form_class(self.request.POST)
        try:
            detalle = detalleVenta.objects.get(lote = lote.data['matricula'], estado = True)
            pago.prima = prima
            prima.detalleVenta = detalle
            prima.save()
            pago.save()
            messages.success(self.request, 'La prima fue registrada con exito')
            return HttpResponseRedirect(self.get_url_redirect()) 
        except Exception:
            prima.delete()
            messages.error(self.request, 'Ocurrió un error al guardar la prima')
        return HttpResponseRedirect(self.get_url_redirect())

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
        lotef = self.third_form_class(self.request.POST)
        print(lotef.data['matricula'] + 'aaaa')
        detalle = detalleVenta.objects.get(lote = lotef.data['matricula'], estado = True)
        estaC = estadoCuenta.objects.get(detalleVenta = detalle)
        pagoM = form.save(commit=False)
        pago = self.second_form_class(self.request.POST)
        pago.pagoMantenimiento = pagoM
        
        cuotaE = cuotaEstadoCuenta(estadoCuenta = estaC,numeroCuota= 0, diasInteres= 0, 
                                    tasaInteres = 0, interesGenerado = 0, interesPagado = 0, 
                                    subTotal = 0, abonoCapital = 0, saldoCapital = 0, saldoInteres = 0,)                            
        cuotaE.save()
        pagoM.numeroCuotaEstadoCuenta = cuotaE
        pagoM.conceptoOtros = ''
        pagoM.montoOtros = 0
        pagoM.save()
        pago.save()
        return HttpResponseRedirect(self.get_url_redirect())
        

    
    

    
    

    