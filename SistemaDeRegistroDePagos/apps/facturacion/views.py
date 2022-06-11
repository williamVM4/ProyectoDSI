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
from django.contrib.auth.models import User
from datetime import date
from datetime import datetime


from apps.inventario.models import detalleVenta
# Create your views here.

class caja(GroupRequiredMixin,TemplateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema',u'Operador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
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
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)
    
    model = prima
    template_name = 'facturacion/agregarPrima.html'
    form_class = agregarPrimaForm
    second_form_class = pagoForm
    third_form_class = lotePagoForm
    def get_context_data(self, **kwargs): 
        context = super(agregarPrima, self).get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(initial={'id':self.kwargs.get('id',None)})
        if 'form3' not in context:
            context['form3'] = self.third_form_class(initial={'id': self.kwargs.get('id', None)})
        context['idp'] = idp
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
            lotef = self.third_form_class(self.request.POST).data['matricula']
            detalle = detalleVenta.objects.get(id = lotef)
            try:
                asig = asignacionLote.objects.get(detalleVenta = detalle)
                try:
                    est = estadoCuenta.objects.get(detalleVenta = detalle)
                    messages.error(self.request, 'Ocurrió un error, el lote '+detalle.lote.identificador+' tiene un estado de cuenta generado. Ya no puede agregar mas primas')
                    return self.render_to_response(self.get_context_data(form=form))  
                except Exception:
                    pass
            except Exception:
                messages.error(self.request, 'Ocurrió un error, el lote '+detalle.lote.identificador+' no tiene propietarios')
                return self.render_to_response(self.get_context_data(form=form))     
            pago.prima = prima
            prima.detalleVenta = detalle
            user = get_current_user()
            if user is not None:
                prima.usuarioCreacion = user
            prima.save()
            pago.save()
            messages.success(self.request, 'La prima fue registrada con exito')
        except Exception:
            prima.delete()
            messages.error(self.request, 'Ocurrió un error al guardar la prima')
        return HttpResponseRedirect(self.get_url_redirect())

class agregarPagoMantenimiento(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema',u'Operador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
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
        lotef = self.third_form_class(self.request.POST).data['matricula']
        detalle = detalleVenta.objects.get(id = lotef)
        try:
                asig = asignacionLote.objects.get(detalleVenta = detalle)
                try:
                    estaC = estadoCuenta.objects.get(detalleVenta = detalle)
                except Exception:
                    messages.error(self.request, 'Ocurrió un error, el lote '+detalle.lote.identificador+' no tiene un estado de cuenta generado. Genere un estado de cuenta para poder agregar un pago')
                    return self.render_to_response(self.get_context_data(form=form))   
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el lote '+detalle.lote.identificador+' no tiene propietarios')
            return self.render_to_response(self.get_context_data(form=form)) 
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
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
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
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
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
            #tamanio columnas
            ws.column_dimensions['A'].width = 9.57
            ws.column_dimensions['B'].width = 13
            ws.column_dimensions['C'].width = 2.71
            ws.column_dimensions['D'].width = 11.14
            ws.column_dimensions['E'].width = 15.43
            ws.column_dimensions['F'].width = 11
            ws.column_dimensions['G'].width = 20.29
            ws.column_dimensions['H'].width = 9.71
            ws.column_dimensions['I'].width = 0
            ws.row_dimensions[1].height = 24.75
            ws.row_dimensions[2].height = 20.25
            ws.row_dimensions[3].height = 14
            ws.row_dimensions[4].height = 18.75
            ws.row_dimensions[5].height = 35.5
            ws.row_dimensions[6].height = 17.25
            ws.row_dimensions[7].height = 15
            ws.row_dimensions[8].height = 17.25
            ws.row_dimensions[9].height = 13.5
            ws.row_dimensions[10].height = 16.5
            ws.row_dimensions[11].height = 15.75
            ws.row_dimensions[12].height = 12
            ws.row_dimensions[13].height = 10.5
            ws.row_dimensions[14].height = 10.5
            ws.row_dimensions[15].height = 14.25
            ws.row_dimensions[16].height = 15.75
            ws.row_dimensions[17].height = 15.75
            ws.row_dimensions[18].height = 18
            ws.row_dimensions[19].height = 24
            ws['F5'] = 0
            ws['F7'] = 0
            ws['F8'] = 0
            ws['F9'] = 0
            ws.merge_cells('B2:F2')
            ws.merge_cells('B15:F15')
            ws['F5'].number_format = '0.00'
            ws['F7'].number_format = '0.00'
            ws['F8'].number_format = '0.00'
            ws['F9'].number_format = '0.00'
            ws['F10'].number_format = '0.00'  
            ws['F11'].number_format = '0.00'
            ws['B1'].number_format = '0.00'
            primaRecibo = prima.objects.get(numeroReciboPrima = pagoRecibo.prima_id )
            detalle = detalleVenta.objects.get(id = primaRecibo.detalleVenta_id)
            asigna = asignacionLote.objects.get(detalleVenta_id = detalle.id)
            nombre = propietario.objects.get(dui = asigna.propietario_id)
            lotes = lote.objects.get(matriculaLote = detalle.lote_id)
            usuario = User.objects.get(id = primaRecibo.usuarioCreacion_id)
            ws['G1'] = "Nº "+primaRecibo.numeroReciboPrima  
            ws['B2'] = nombre.nombrePropietario
            ws['B2'].alignment = Alignment(horizontal="center",vertical="center")
            ws['B4'].alignment = Alignment(horizontal="center",vertical="center")
            ws['C4'].alignment = Alignment(horizontal="center",vertical="center")
            ws['B4'] = lotes.numeroLote
            ws['C4'] = lotes.poligono
            ws['F10'] = pagoRecibo.monto
            ws['F11'] = "=SUM(F5:F10)"
            ws['B19'] = usuario.first_name
            ws['B1'] = '=F11'
            fecha = pagoRecibo.fechaPago
            
            

            ws['B15'] = fecha
            
            if pagoRecibo.tipoPago == 1:
                    ws['E18'] = "Pago realizado en efectivo"
            else:
                banco = cuentaBancaria.objects.get(numeroCuentaBancaria = pagoRecibo.cuentaBancaria_id)
                ws['E18'] = "Pago realizado en "+banco.banco+" Cta. No. "+banco.numeroCuentaBancaria
                ws['E19'] = "a/n de Decatur, S.A. Ref. " + pagoRecibo.referencia
        else:
            if pagoRecibo.pagoMantenimiento_id:
                ws.column_dimensions['A'].width = 9.43
                ws.column_dimensions['B'].width = 9.71
                ws.column_dimensions['C'].width = 1.29
                ws.column_dimensions['D'].width = 10.71
                ws.column_dimensions['E'].width = 14.14
                ws.column_dimensions['F'].width = 12.14
                ws.column_dimensions['G'].width = 10.71
                ws.column_dimensions['H'].width = 15.43
                ws.column_dimensions['I'].width = 10.71
                ws.row_dimensions[1].height = 11.75
                ws.row_dimensions[2].height = 12.5
                ws.row_dimensions[3].height = 27.75
                ws.row_dimensions[4].height = 18
                ws.row_dimensions[5].height = 15.75
                ws.row_dimensions[6].height = 18.75
                ws.row_dimensions[7].height = 15.75
                ws.row_dimensions[8].height = 18.75
                ws.row_dimensions[9].height = 17.25
                ws.row_dimensions[10].height = 15.75
                ws.row_dimensions[11].height = 21
                ws.row_dimensions[12].height = 15.75
                ws.row_dimensions[13].height = 22.5
                ws.row_dimensions[14].height = 15.75
                ws.row_dimensions[15].height = 15
                ws.row_dimensions[16].height = 18
                ws.row_dimensions[17].height = 15.75
                ws.row_dimensions[18].height = 15.75
                ws.row_dimensions[19].height = 18
                ws.row_dimensions[20].height = 21.75
                ws.row_dimensions[21].height = 12.75
                ws['F7'].number_format = ' 0.00'
                ws['F8'].number_format = ' 0.00'
                ws['F9'].number_format = ' 0.00'
                ws['F10'].number_format = ' 0.00'
                ws['F11'].number_format = ' 0.00'  
                ws['F12'].number_format = ' 0.00'
                ws['F13'].number_format = ' 0.00'
                ws['B3'].number_format = ' 0.00'
                ws['F7'] = 0
                ws['F8'] = 0
                ws['F9'] = 0
                ws['F10'] = 0
                ws['F11'] = 0
                ws['F12'] = 0
                ws['F13'] = 0
                ws['B3'] = 0
                pagoMRecibo = pagoMantenimiento.objects.get(numeroReciboMantenimiento = pagoRecibo.pagoMantenimiento_id)
                usuario = User.objects.get(id = pagoMRecibo.usuarioCreacion_id)
                cuotaEstado = cuotaEstadoCuenta.objects.get(id = pagoMRecibo.numeroCuotaEstadoCuenta_id)
                estadoC = estadoCuenta.objects.get(id = cuotaEstado.estadoCuenta_id)
                detalle = detalleVenta.objects.get(id = estadoC.detalleVenta_id)
                asigna = asignacionLote.objects.get(detalleVenta_id = detalle.id)
                nombre = propietario.objects.get(dui = asigna.propietario_id)
                lotes = lote.objects.get(matriculaLote = detalle.lote_id)
                ws['H3'] = "Nº "+pagoMRecibo.numeroReciboMantenimiento
                ws.merge_cells('B4:F4')
                ws.merge_cells('B16:F16')
                ws.merge_cells('B12:E12')
                ws['F7'] = pagoRecibo.monto
                ws['F13'] = '=SUM(F7:F12)'
                ws['B3'] = '=F13'
                ws['B20'] = usuario.first_name
                ws['E18'].font = Font(size=10)
                ws['E19'].font = Font(size=10)
                ws['B16'] = pagoRecibo.fechaPago
                ws['F12'] = pagoMRecibo.montoOtros
                ws['B12'] = "  "+pagoMRecibo.conceptoOtros
                ws['B4'].alignment = Alignment(horizontal="center",vertical="center")
                ws['B4'] = nombre.nombrePropietario
                ws['D5'].alignment = Alignment(horizontal="center",vertical="center")
                ws['E5'].alignment = Alignment(horizontal="center",vertical="center")
                ws['D5'] = lotes.numeroLote
                ws['E5'] = lotes.poligono

                if pagoRecibo.tipoPago == 1:
                    ws['E18'] = "Pago realizado en efectivo"
                else:
                    banco = cuentaBancaria.objects.get(numeroCuentaBancaria = pagoRecibo.cuentaBancaria_id)
                    ws['E18'] = "Pago realizado en "+banco.banco+" Cta. No. "+banco.numeroCuentaBancaria
                    ws['E19'] = "a/n de Decatur, S.A. Ref. " + pagoRecibo.referencia
                
                                
       

        nombre_archivo = "Recibo.xlsx"
        response = HttpResponse()
        contenido = "attachment; filename = {0}".format(nombre_archivo)
        response["Content-Disposition"]= contenido
        wb.save(response)
        return response
    
    

    