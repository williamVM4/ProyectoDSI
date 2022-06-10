from asyncio import current_task
from email.headerregistry import Group
from importlib.resources import contents
from multiprocessing import context
from urllib import response
from xml.dom.minidom import Identified
from django.forms import NullBooleanField
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView,FormView, ListView, DetailView
from apps.monitoreo.models import estadoCuenta, cuotaEstadoCuenta
from apps.inventario.models import cuentaBancaria,proyectoTuristico
from apps.autenticacion.mixins import *
from .forms import *
from .models import *
from apps.inventario.models import *
from django.shortcuts import redirect, render
from django.contrib import messages
from crum import get_current_user
from django.http.response import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import *


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
        context['pagos'] = pago.objects.all().order_by('-fechaPago')
        return context

        

class agregarPrima(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema',u'Operador del sistema']
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
        pago = self.second_form_class(self.request.POST).save(commit=False)
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
        detalle = detalleVenta.objects.get(lote = lotef.data['matricula'], estado = True)
        estaC = estadoCuenta.objects.get(detalleVenta = detalle)
        pagoM = form.save(commit=False)
        pago = self.second_form_class(self.request.POST).save(commit=False)
        
        cuotaE = cuotaEstadoCuenta(estadoCuenta = estaC,numeroCuota= 0, diasInteres= 0, 
                                    tasaInteres = 0, interesGenerado = 0, interesPagado = 0, 
                                    subTotal = 0, abonoCapital = 0, saldoCapital = 0, saldoInteres = 0,)                            
        cuotaE.save()
        pagoM.numeroCuotaEstadoCuenta = cuotaE
        user = get_current_user()
        if user is not None:
            pagoM.usuarioCreacion = user
        pagoM.save()
        pago.pagoMantenimiento = pagoM
        pago.save()
        return HttpResponseRedirect(self.get_url_redirect())
        
# Views de cuentas Bancarias
class gestionarCuentasBancarias(GroupRequiredMixin,ListView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    template_name = 'facturacion/CuentasBancarias/gestionarCuentasBancarias.html'
    model = cuentaBancaria

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('idp', None) 
        context['idp'] = id
        context['cuentaBancaria'] = cuentaBancaria.objects.filter(proyectoTuristico__id=id)
        return context

class agregarCuentaBancaria(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    template_name = 'facturacion/CuentasBancarias/agregarCuentaBancaria.html'
    form_class = agregarCuentaBancariaForm
    
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) 
        return reverse_lazy('cuentas', kwargs={'idp': idp})

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        context['idp'] = idp         
        return context

    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) 
        cuentaBancaria = form.save(commit=False)
        try:
            cuentaBancaria.proyectoTuristico = proyectoTuristico.objects.get(id=idp)
            cuentaBancaria.identificador = str(cuentaBancaria.numeroCuentaBancaria)
            cuentaBancaria.save()
            messages.success(self.request, 'La cuenta bancaria se ha guardado con éxito')
        except Exception:
            cuentaBancaria.delete()
            messages.error(self.request, 'Ocurrió un error al guardar la cuenta bancaria, la cuenta bancaria no es válido')
        return HttpResponseRedirect(self.get_url_redirect())
    
    
class Recibo(TemplateView):

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) 
        id = self.kwargs.get('pk', None)
        context['idp'] = idp
        context['id'] = id
        return context

    
    def get(self,request,*args,**kwargs):
        context=super().get_context_data(**kwargs)
         # recojo el parametro 
        idp = self.kwargs.get('idp', None) 
        id = self.kwargs.get('pk', None)
        pagoRecibo = pago.objects.get(pk = id)
        wb = Workbook()
        ws = wb.active
        ws.title = "Recibo"

        if pagoRecibo.prima_id:
            primaRecibo = prima.objects.get(numeroReciboPrima = pagoRecibo.prima_id )
            ws['B1'] = "Nº "+primaRecibo.numeroReciboPrima
            ws.merge_cells('B6:F6')
        
        else:
            if pagoRecibo.pagoMantenimiento_id:
                pagoMRecibo = pagoMantenimiento.objects.get(numeroReciboMantenimiento = pagoRecibo.pagoMantenimiento_id)
                ws['B1'] = "Nº "+pagoMRecibo.numeroReciboMantenimiento
        
       

        nombre_archivo = "Recibo.xlsx"
        response = HttpResponse()
        contenido = "attachment; filename = {0}".format(nombre_archivo)
        response["Content-Disposition"]= contenido
        wb.save(response)
        return response
    
    

    