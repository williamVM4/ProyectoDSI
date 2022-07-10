from ast import If
from asyncio import current_task
from email.headerregistry import Group
from importlib.resources import contents
from multiprocessing import context
import re
from urllib import response
from xml.dom.minidom import Identified
from django.forms import NullBooleanField
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView,FormView, ListView, DetailView, UpdateView
from apps.monitoreo.models import estadoCuenta, cuotaEstadoCuenta, condicionesPago
from apps.inventario.models import cuentaBancaria,proyectoTuristico, asignacionLote, detalleVenta
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
from math import floor
from decimal import Decimal
from datetime import date, timedelta, time, datetime
from dateutil.relativedelta import relativedelta
from django.utils.dateparse import parse_datetime
import dateutil.parser

"Vista donde se listaran todos los pagos que se vayan registrando"
class caja(GroupRequiredMixin,TemplateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema',u'Operador del sistema']
    template_name = 'facturacion/caja.html'
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Se valida que exista el proyecto turistico"
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(**kwargs)
        "Se envian los parametros por contexto y los objetos de tipo pago"
        id = self.kwargs.get('idp', None) 
        context['idp'] = id
        context['pagos'] = pago.objects.all().order_by('-fechaRegistro')
        return context

"Vista de formulario para agregar prima"
class agregarPrima(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema',u'Operador del sistema']
    model = prima
    template_name = 'facturacion/Prima/agregarPrima.html'
    form_class = agregarPrimaForm #formulario con datos del modelo prima
    second_form_class = pagoForm #formulario con datos del modelo pago
    third_form_class = lotePagoForm #formulario con el detalle de venta

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Se valida si el proyecto turistico existe"
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs): 
        context = super(agregarPrima, self).get_context_data(**kwargs)
        "Se envia el id del proyecto y los formularios auxiliares por contexto"
        idp = self.kwargs.get('idp', None)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(id = idp)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(id = idp)
        context['idp'] = idp
        return context

    "url de exito del formulario"
    def get_url_redirect(self, **kwargs):
        idp = self.kwargs.get('idp', None)
        return reverse_lazy('caja', kwargs={'idp': idp})

    def form_valid(self, form, **kwargs):
        "Se obtienen los datos de los formularios"
        prima = form.save(commit=False)
        pago = self.second_form_class(self.request.POST).save(commit=False)
        lotef = self.third_form_class(self.request.POST).data['matricula']
        try:
            detalle = detalleVenta.objects.get(id = lotef)
            "validacion de que tenga propietarios"
            asig = asignacionLote.objects.filter(detalleVenta = detalle).exists()
            if asig is False:
                messages.error(self.request, 'Ocurrió un error, el lote '+detalle.lote.identificador+' no tiene propietarios registrados')
                return self.render_to_response(self.get_context_data(form=form, form2=self.second_form_class(self.request.POST), form3 = self.third_form_class(self.request.POST)))
            "validacion de que no tenga estado de cuenta"
            est = estadoCuenta.objects.filter(detalleVenta = detalle).exists()
            if est is True:
                messages.error(self.request, 'Ocurrió un error, el lote '+detalle.lote.identificador+' tiene un estado de cuenta generado. Ya no puede registrar más primas')
                return self.render_to_response(self.get_context_data(form=form, form2=self.second_form_class(self.request.POST), form3 = self.third_form_class(self.request.POST)))  
            pago.prima = prima
            pago.fechaRegistro=datetime.now()
            prima.detalleVenta = detalle
            "validacion de que el monto de prima no sea menor al precio de venta - descuento"
            if pago.monto > (detalle.precioVenta - detalle.descuento):
                messages.error(self.request, 'Ocurrió un error, el monto de la prima debe ser menor al precio de venta')
                return self.render_to_response(self.get_context_data(form=form, form2=self.second_form_class(self.request.POST), form3 = self.third_form_class(self.request.POST)))
            "guarda el usuario"
            user = get_current_user()
            if user is not None:
                prima.usuarioCreacion = user
            prima.save()
            pago.save()
            messages.success(self.request, 'La prima fue registrada con exito')
        except Exception:
            messages.error(self.request, 'Ocurrió un error al guardar la prima')
        return HttpResponseRedirect(self.get_url_redirect())

"Vista de formulario para agregar pago por mantenimiento"
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
    template_name = 'facturacion/PagoMantenimiento/agregarPagoMantenimiento.html'

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

        #Validacion de asignacion
        try:
             asig = asignacionLote.objects.filter(detalleVenta = detalle)
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el lote '+detalle.lote.identificador+' no tiene propietarios')
            return self.render_to_response(self.get_context_data(form=form)) 

        asig = asignacionLote.objects.filter(detalleVenta = detalle)

        #Validacion de estado de cuenta
        try:
            estaC = estadoCuenta.objects.get(detalleVenta = detalle)
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el lote '+detalle.lote.identificador+' no tiene un estado de cuenta generado. Establezca la venta para poder agregar un pago')
            return self.render_to_response(self.get_context_data(form=form))

        estadoC = estadoCuenta.objects.get(detalleVenta = detalle)
        condicion=condicionesPago.objects.get(detalleVenta=detalle)
        stringFechaPago=self.second_form_class(self.request.POST).data['fechaPago']
        stringFechaPago=stringFechaPago[0:4]+"-"+stringFechaPago[6:7]+"-"+stringFechaPago[8:10]
        fechaPago=dateutil.parser.parse(stringFechaPago).date()
        listadoPagos=pagoMantenimiento.objects.filter(numeroCuotaEstadoCuenta__estadoCuenta=estadoC).order_by('-fechaRegistro')
        primeraCuota="NO"
        saldoUltimaCuota=0
        saldoUltimoRecargo=0
        monto=0
        descuento=0
        montoOtros=0
        conceptoDescuento=""
        conceptoOtros=""
        observaciones=""
        
        #Verificar que existan cuotas de mantenimiento en el estado de cuenta
        try: 
            ultimoPagoListado=listadoPagos[0]
            ultimoPago=pago.objects.get(pagoMantenimiento = ultimoPagoListado)
        except Exception:
            primeraCuota="SI"
            pass

        #Validacion del monto
        try:
            monto=Decimal(self.second_form_class(self.request.POST).data['monto'])
            if monto==0:
                messages.error(self.request, 'Ocurrió un error, el monto no es un valor válido.')
                return self.render_to_response(self.get_context_data(form=form))  
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el monto no debe ser cero.')
            return self.render_to_response(self.get_context_data(form=form))

        #Obtenemos la fechas del corte, la cuota de pago, inicio y fin de mes
        fechaCorte=condicion.fechaEscrituracion
        stringFechaCadaMes="Fecha de pago "+fechaCorte.strftime("%d")+" de cada mes.\n"
        fechaUltimoRecargo=fechaCorte
        stringObservaciones=""
        stringRecargo=""
        valorPagado=monto
        fechaUltimoPago=fechaCorte

        #Validacion del monto en concepto de otros
        try:
            montoOtros=Decimal(self.form_class(self.request.POST).data['montoOtros'])
        except Exception:
            pass

        #Validacion del monto en concepto de descuento
        try:
            descuento=Decimal(self.form_class(self.request.POST).data['descuento'])
        except Exception:
            pass    

        #Si existe un monto en concepto de otros se lo restamos al valor pagado
        monto-=montoOtros
        valorRecargo=0
        abono=0

        #Calculo del ultimo pago ingresado
        if primeraCuota=="NO":
            fechaCorte=ultimoPago.pagoMantenimiento.fechaUltimoMtto
            saldoUltimaCuota=ultimoPago.pagoMantenimiento.abono
            fechaUltimoRecargo=ultimoPago.pagoMantenimiento.fechaUltimoRecargo
            saldoUltimoRecargo=ultimoPago.pagoMantenimiento.saldoRecargo
            fechaUltimoPago=ultimoPago.fechaPago
        
        #Validacion del concepto del descuento
        try:
            conceptoDescuento=self.form_class(self.request.POST).data['conceptoDescuento']
        except Exception:
            pass

        #Validacion del concepto de otros cargos
        try:
            conceptoOtros=self.form_class(self.request.POST).data['conceptoOtros']
        except Exception:
            pass

        #Validacion del concepto de las observaciones
        try:
            observaciones=self.second_form_class(self.request.POST).data['observaciones']
        except Exception:
            pass
            
        #Validacion de la fecha de pago
        if fechaPago<fechaUltimoPago:
            messages.error(self.request, 'Ocurrió un error, la fecha de pago debe ser mayor al último pago registrado en el estado de cuenta del lote. Fecha último pago '+fechaUltimoPago.strftime("%d/%m/%Y"))
            return self.render_to_response(self.get_context_data(form=form)) 
        
        #Validacion del concepto por descuento
        if descuento!=0 and conceptoDescuento=="":
            messages.error(self.request, 'Ocurrió un error, no se ha asignado un concepto al monto del descuento.')
            return self.render_to_response(self.get_context_data(form=form))

        #Validacion del concepto por otros pagos
        if montoOtros!=0 and conceptoOtros=="":
            messages.error(self.request, 'Ocurrió un error, no se ha asignado un concepto al monto por otros pagos.')
            return self.render_to_response(self.get_context_data(form=form))  

        #Validacion del monto a cancelar
        if montoOtros!=0 and descuento!=0:
            if valorPagado<(montoOtros+descuento):
                messages.error(self.request, 'Ocurrió un error, el monto no corresponde al valor a cancelar.')
                return self.render_to_response(self.get_context_data(form=form))
        elif montoOtros>valorPagado and descuento==0:
            messages.error(self.request, 'Ocurrió un error, el monto no corresponde al valor a cancelar en concepto de otros pagos.')
            return self.render_to_response(self.get_context_data(form=form))
        elif descuento>valorPagado and montoOtros==0:
            messages.error(self.request, 'Ocurrió un error, el monto no corresponde al valor a cancelar en concepto de descuento por recargo.')
            return self.render_to_response(self.get_context_data(form=form))

        #Validacion del monto de descuento, exista un recargo para cobrarlo
        fechaValidacion=fechaCorte + relativedelta(months=1)
        fechaValidacionActualizada=fechaActualizada(fechaValidacion,condicion.fechaEscrituracion)
        if  descuento !=0:
            if fechaPago>fechaValidacionActualizada:
                cantidadMeses=int(cantMeses(fechaPago,fechaUltimoRecargo))
                fechaRecargo=fechaUltimoRecargo+relativedelta(months=cantidadMeses)
                fechaRecargo=fechaActualizada(fechaRecargo, condicion.fechaEscrituracion)
                if fechaPago<=fechaRecargo:
                    cantidadMeses-=1
                montoMensajeRecargo=Decimal(cantidadMeses*condicion.multaMantenimiento)
                if descuento>montoMensajeRecargo:
                    messages.error(self.request, 'Ocurrió un error, el monto del descuento no debe ser mayor al cálculo del recargo. Recargo calculado: $ '+str(round(montoMensajeRecargo,2)))
                    return self.render_to_response(self.get_context_data(form=form)) 
            else:
                messages.error(self.request, 'Ocurrió un error, no existe un recargo al cual aplicar el descuento.')
                return self.render_to_response(self.get_context_data(form=form)) 

        #Calculo del recargo
        if monto>0:
            fechaValidacion=fechaCorte + relativedelta(months=1)
            if fechaPago>fechaActualizada(fechaValidacion,condicion.fechaEscrituracion):
                stringRecargo="\nRecargo:\n"
                cantidadMeses=int(cantMeses(fechaPago,fechaUltimoRecargo))
                fechaRecargo=fechaUltimoRecargo+relativedelta(months=cantidadMeses)
                fechaRecargo=fechaActualizada(fechaRecargo, condicion.fechaEscrituracion)
                if fechaPago<=fechaRecargo:
                    cantidadMeses-=1                
                monto=(cantidadMeses*condicion.multaMantenimiento)-saldoUltimoRecargo
                if valorPagado<monto:
                    monto=valorPagado
                if saldoUltimoRecargo==0:
                    if monto==condicion.multaMantenimiento:
                        fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                        stringRecargo+=printFecha(fechaUltimoRecargo)+" $ "+str(round(condicion.multaMantenimiento,2))+"\n"
                        monto-=condicion.multaMantenimiento
                    elif monto<condicion.multaMantenimiento:
                        fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                        stringRecargo+="Ab. "+printFecha(fechaUltimoRecargo)+" $ "+str(round(monto,2))+"\nSaldo "+printFecha(fechaUltimoRecargo)+" $ "+str(round(condicion.multaMantenimiento-monto,2))+"\n"
                    elif monto>condicion.multaMantenimiento:
                        abonoCuota=monto%condicion.multaMantenimiento
                        cantCuotas=floor(monto/condicion.multaMantenimiento)
                        if abonoCuota==0.0:
                            if cantCuotas>1:
                                for i in range(cantCuotas):
                                    fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                                    if i==0:
                                        stringRecargo+=printFecha(fechaUltimoRecargo)+" a "
                                    elif i==cantCuotas-1:
                                        stringRecargo+=printFecha(fechaUltimoRecargo)+" $ "+str(round(condicion.multaMantenimiento*cantCuotas,2))+"\n"
                                    monto-=condicion.multaMantenimiento
                            else:
                                fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                                stringRecargo+=printFecha(fechaUltimoRecargo)+" $ "+str(round(condicion.multaMantenimiento*cantCuotas,2))+"\n"
                                monto-=condicion.multaMantenimiento
                        else:
                            if cantCuotas>1:
                                for i in range(cantCuotas):
                                    fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                                    if i==0:
                                        stringRecargo+=printFecha(fechaUltimoRecargo)+" a "
                                    elif i==cantCuotas-1:
                                        stringRecargo+=printFecha(fechaUltimoRecargo)+" $ "+str(round(condicion.multaMantenimiento*cantCuotas,2))+"\n"
                                    monto-=condicion.multaMantenimiento
                            else:
                                fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                                stringRecargo+=printFecha(fechaUltimoRecargo)+" $ "+str(round(condicion.multaMantenimiento*cantCuotas,2))+"\n"
                                monto-=condicion.multaMantenimiento
                            fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                            stringRecargo+="Ab. "+printFecha(fechaUltimoRecargo)+" $ "+str(round(monto,2))+"\n"
                else:
                    valorCompl=condicion.multaMantenimiento-saldoUltimaCuota
                    if monto<=condicion.multaMantenimiento:
                        if monto==valorCompl:
                            stringRecargo+="Compl. "+printFecha(fechaUltimoRecargo)+" $ "+str(round(monto,2))+"\n"
                            monto=0.0
                        elif monto<valorCompl:
                            stringRecargo+="Ab. "+printFecha(fechaUltimoRecargo)+" $ "+str(round(monto,2))+"\n"
                            monto+=saldoUltimoRecargo
                        elif monto>valorCompl:
                            stringRecargo+="Compl. "+printFecha(fechaUltimoRecargo)+" $ "+str(round(valorCompl,2))+"\n"
                            monto-=valorCompl
                            fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                            stringRecargo+="Ab. "+printFecha(fechaUltimoRecargo)+" $ "+str(round(monto,2))+"\n"
                    elif monto>condicion.multaMantenimiento:
                        stringRecargo+="Compl. "+printFecha(fechaUltimoRecargo)+" $ "+str(round(valorCompl,2))+"\n"
                        monto-=valorCompl
                        abonoCuota=monto%condicion.multaMantenimiento
                        cantCuotas=floor(monto/condicion.multaMantenimiento)
                        if abonoCuota==0.0:
                            if cantCuotas>1:
                                for i in range(cantCuotas):
                                    fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                                    if i==0:
                                        stringRecargo+=printFecha(fechaUltimoRecargo)+" a "
                                    elif i==cantCuotas-1:
                                        stringRecargo+=printFecha(fechaUltimoRecargo)+" $ "+str(round(condicion.multaMantenimiento*cantCuotas,2))+"\n"
                                    monto-=condicion.multaMantenimiento
                            else:
                                fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                                stringRecargo+=printFecha(fechaUltimoRecargo)+" $ "+str(round(condicion.multaMantenimiento*cantCuotas,2))+"\n"
                                monto-=condicion.multaMantenimiento
                        else:
                            if cantCuotas>1:
                                for i in range(cantCuotas):
                                    fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                                    if i==0:
                                        stringRecargo+=printFecha(fechaUltimoRecargo)+" a "
                                    elif i==cantCuotas-1:
                                        stringRecargo+=printFecha(fechaUltimoRecargo)+" $ "+str(round(condicion.multaMantenimiento*cantCuotas,2))+"\n"
                                    monto-=condicion.multaMantenimiento
                            else:
                                fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                                stringRecargo+=printFecha(fechaUltimoRecargo)+" $ "+str(round(condicion.multaMantenimiento*cantCuotas,2))+"\n"
                                monto-=condicion.multaMantenimiento
                            fechaUltimoRecargo=fechaUltimoRecargo + relativedelta(months=1)
                            stringRecargo+="Ab. "+printFecha(fechaUltimoRecargo)+" $ "+str(round(monto,2))+"\n"
                    if monto!=0:
                        stringRecargo+="Saldo "+printFecha(fechaUltimoRecargo)+" $ "+str(round(condicion.multaMantenimiento-monto,2))+"\n"
                
                #Guardamos en variables locales lo obtenido del calculo del recargo, para proceder al calculo del mantenimiento
                valorRecargo=cantidadMeses*condicion.multaMantenimiento-descuento
                saldoUltimoRecargo=monto
                monto=valorPagado-valorRecargo-montoOtros
                abono=saldoUltimaCuota
                stringObservaciones=stringFechaCadaMes+"\nMantenimiento:\n"+"Saldo "+printFecha(fechaCorte)+" $ "+str(round(condicion.mantenimientoCuota-saldoUltimaCuota,2))+"\n"
        
        #Calulo del mantenimiento
        if monto>0:
            stringObservaciones=stringFechaCadaMes+"\nMantenimiento:\n"
            if saldoUltimaCuota==0:
                if monto==condicion.mantenimientoCuota:
                    fechaCorte=fechaCorte + relativedelta(months=1)
                    stringObservaciones+=printFecha(fechaCorte)+" $ "+str(round(condicion.mantenimientoCuota,2))+"\n"
                    monto-=condicion.mantenimientoCuota
                elif monto<condicion.mantenimientoCuota:
                    fechaCorte=fechaCorte + relativedelta(months=1)
                    stringObservaciones+="Ab. "+printFecha(fechaCorte)+" $ "+str(round(monto,2))+"\nSaldo "+printFecha(fechaCorte)+" $ "+str(round(condicion.mantenimientoCuota-monto,2))+"\n"
                elif monto>condicion.mantenimientoCuota:
                    abonoCuota=monto%condicion.mantenimientoCuota
                    cantCuotas=floor(monto/condicion.mantenimientoCuota)
                    if abonoCuota==0.0:
                        if cantCuotas>1:
                            for i in range(cantCuotas):
                                fechaCorte=fechaCorte + relativedelta(months=1)
                                if i==0:
                                    stringObservaciones+=printFecha(fechaCorte)+" a "
                                elif i==cantCuotas-1:
                                    stringObservaciones+=printFecha(fechaCorte)+" $ "+str(round(condicion.mantenimientoCuota*cantCuotas,2))+"\n"
                                monto-=condicion.mantenimientoCuota
                        else:
                            fechaCorte=fechaCorte + relativedelta(months=1)
                            stringObservaciones+=printFecha(fechaCorte)+" $ "+str(round(condicion.mantenimientoCuota*cantCuotas,2))+"\n"
                            monto-=condicion.mantenimientoCuota
                    else:
                        if cantCuotas>1:
                            for i in range(cantCuotas):
                                fechaCorte=fechaCorte + relativedelta(months=1)
                                if i==0:
                                    stringObservaciones+=printFecha(fechaCorte)+" a "
                                elif i==cantCuotas-1:
                                    stringObservaciones+=printFecha(fechaCorte)+" $ "+str(round(condicion.mantenimientoCuota*cantCuotas,2))+"\n"
                                monto-=condicion.mantenimientoCuota
                        else:
                            fechaCorte=fechaCorte + relativedelta(months=1)
                            stringObservaciones+=printFecha(fechaCorte)+" $ "+str(round(condicion.mantenimientoCuota*cantCuotas,2))+"\n"
                            monto-=condicion.mantenimientoCuota
                        fechaCorte=fechaCorte + relativedelta(months=1)
                        stringObservaciones+="Ab. "+printFecha(fechaCorte)+" $ "+str(round(monto,2))+"\n"
            else:
                valorCompl=condicion.mantenimientoCuota-saldoUltimaCuota
                if monto<=condicion.mantenimientoCuota:
                    if monto==valorCompl:
                        stringObservaciones+="Compl. "+printFecha(fechaCorte)+" $ "+str(round(monto,2))+"\n"
                        monto=0.0
                    elif monto<valorCompl:
                        stringObservaciones+="Ab. "+printFecha(fechaCorte)+" $ "+str(round(monto,2))+"\n"
                        monto+=saldoUltimaCuota
                    elif monto>valorCompl:
                        stringObservaciones+="Compl. "+printFecha(fechaCorte)+" $ "+str(round(valorCompl,2))+"\n"
                        monto-=valorCompl
                        fechaCorte=fechaCorte + relativedelta(months=1)
                        stringObservaciones+="Ab. "+printFecha(fechaCorte)+" $ "+str(round(monto,2))+"\n"
                elif monto>condicion.mantenimientoCuota:
                    stringObservaciones+="Compl. "+printFecha(fechaCorte)+" $ "+str(round(valorCompl,2))+"\n"
                    monto-=valorCompl
                    abonoCuota=monto%condicion.mantenimientoCuota
                    cantCuotas=floor(monto/condicion.mantenimientoCuota)
                    if abonoCuota==0.0:
                        if cantCuotas>1:
                            for i in range(cantCuotas):
                                fechaCorte=fechaCorte + relativedelta(months=1)
                                if i==0:
                                    stringObservaciones+=printFecha(fechaCorte)+" a "
                                elif i==cantCuotas-1:
                                    stringObservaciones+=printFecha(fechaCorte)+" $ "+str(round(condicion.mantenimientoCuota*cantCuotas,2))+"\n"
                                monto-=condicion.mantenimientoCuota
                        else:
                            fechaCorte=fechaCorte + relativedelta(months=1)
                            stringObservaciones+=printFecha(fechaCorte)+" $ "+str(round(condicion.mantenimientoCuota*cantCuotas,2))+"\n"
                            monto-=condicion.mantenimientoCuota
                    else:
                        if cantCuotas>1:
                            for i in range(cantCuotas):
                                fechaCorte=fechaCorte + relativedelta(months=1)
                                if i==0:
                                    stringObservaciones+=printFecha(fechaCorte)+" a "
                                elif i==cantCuotas-1:
                                    stringObservaciones+=printFecha(fechaCorte)+" $ "+str(round(condicion.mantenimientoCuota*cantCuotas,2))+"\n"
                                monto-=condicion.mantenimientoCuota
                        else:
                            fechaCorte=fechaCorte + relativedelta(months=1)
                            stringObservaciones+=printFecha(fechaCorte)+" $ "+str(round(condicion.mantenimientoCuota*cantCuotas,2))+"\n"
                            monto-=condicion.mantenimientoCuota
                        fechaCorte=fechaCorte + relativedelta(months=1)
                        stringObservaciones+="Ab. "+printFecha(fechaCorte)+" $ "+str(round(monto,2))+"\n"
            if monto!=0:
                stringObservaciones+="Saldo "+printFecha(fechaCorte)+" $ "+str(round(condicion.mantenimientoCuota-monto,2))+"\n"
        
        #Actualizamos el abono de la cuota de acuerdo a lo cancelado
        abono=monto
        if valorPagado==montoOtros:
            fechaCorte=ultimoPago.pagoMantenimiento.fechaUltimoMtto
            saldoUltimaCuota=ultimoPago.pagoMantenimiento.abono
            fechaUltimoRecargo=ultimoPago.pagoMantenimiento.fechaUltimoRecargo
            saldoUltimoRecargo=ultimoPago.pagoMantenimiento.saldoRecargo
            abono=saldoUltimaCuota
            valorPagado=0
            valorRecargo=0

        #Actualizamos la fecha del recargo de acuerdo a lo cancelado
        if saldoUltimoRecargo==0:
            if fechaUltimoRecargo<=fechaCorte:
                if fechaPago<=fechaCorte:
                    fechaUltimoRecargo=fechaCorte
        stringObservaciones+=stringRecargo
        
        #Imprimir el monto de otros si existe
        if montoOtros!=0:
            if montoOtros==valorPagado:
                stringObservaciones+="Otros:\n"+conceptoOtros+" $ "+str(round(montoOtros,2))+"\n"
            else:
                stringObservaciones+="\nOtros:\n"+conceptoOtros+" $ "+str(round(montoOtros,2))+"\n"
        
        #Imprimir el descuento si existe
        if descuento!=0:
            stringObservaciones+="\nDescuento de Recargo: $ "+str(round(descuento,2))+"\n"+conceptoDescuento+"\n"
        
        #Imprimir las observaciones si existen
        if observaciones!="":
            stringObservaciones+="\nObservaciones:\n"+observaciones

        #Guardamos el pago de mantenimiento en la base de datos
        pagoM = form.save(commit=False)
        pagoF = self.second_form_class(self.request.POST).save(commit=False)
        try:
            cuotaE = cuotaEstadoCuenta(estadoCuenta = estaC,numeroCuota= 0, diasInteres= 0, tasaInteres = 0, interesGenerado = 0, interesPagado = 0, subTotal = 0, abonoCapital = 0, saldoCapital = 0, saldoInteres = 0,)                            
            cuotaE.save()
            pagoM.numeroCuotaEstadoCuenta = cuotaE
            pagoM.fechaUltimoMtto=fechaActualizada(fechaCorte,condicion.fechaEscrituracion)
            pagoM.abono=abono
            pagoM.fechaUltimoRecargo=fechaActualizada(fechaUltimoRecargo,condicion.fechaEscrituracion)
            pagoM.saldoRecargo=saldoUltimoRecargo
            pagoM.mantenimiento=valorPagado-valorRecargo-montoOtros
            pagoM.recargoMtto=valorRecargo
            pagoM.conceptoDescuento=conceptoDescuento
            pagoM.descuento=descuento
            pagoM.conceptoOtros=conceptoOtros
            pagoM.montoOtros=montoOtros
            user = get_current_user()
            if user is not None:
                pagoM.usuarioCreacion = user
            pagoM.save()
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el lote '+detalle.lote.identificador+' no se le ha establecido una venta. Establezca las condiciones de pago del lote para poder agregar un pago')
            return self.render_to_response(self.get_context_data(form=form))   
        pagoF.pagoMantenimiento = pagoM
        pagoF.monto = valorPagado
        pagoF.observaciones = stringObservaciones
        if pagoF.tipoPago == 1:
            pagoF.referencia = ''
            pagoF.cuentaBancaria = None
        pagoF.save()
        return HttpResponseRedirect(self.get_url_redirect())

#Función que calcula la cantidad de meses entre dos meses
def cantMeses(fechaMayor, fechaMenor):
    return (fechaMayor.year - fechaMenor.year) * 12 + fechaMayor.month - fechaMenor.month

#Función que valida el día de la fecha
def fechaActualizada(fecha, fechaEscrituracion):
    diaFecha=int(fecha.strftime('%d'))
    diaFechaEscrituracion=int(fechaEscrituracion.strftime('%d'))
    if diaFecha == diaFechaEscrituracion:
        return fecha
    elif diaFecha<diaFechaEscrituracion:
        diferencia=diaFechaEscrituracion-diaFecha
        fecha=fecha+relativedelta(days=diferencia)
        return fecha
    else:
        diferencia=diaFecha-diaFechaEscrituracion
        fecha=fecha-relativedelta(days=diferencia)
        return fecha

#Función que convierte fecha en formato español
def printFecha(fecha):
    mes=int(fecha.strftime('%m'))
    stringFecha=""
    if mes==1:
        stringFecha="Enero/"+fecha.strftime('%y') 
    elif mes==2:
        stringFecha="Febrero/"+fecha.strftime('%y')
    elif mes==3:
        stringFecha= "Marzo/"+fecha.strftime('%y')
    elif mes==4:
        stringFecha="Abril/"+fecha.strftime('%y')
    elif mes==5:
        stringFecha="Mayo/"+fecha.strftime('%y')
    elif mes==6:
        stringFecha="Junio/"+fecha.strftime('%y')
    elif mes==7:
        stringFecha="Julio/"+fecha.strftime('%y')
    elif mes==8:
        stringFecha="Agosto/"+fecha.strftime('%y')
    elif mes==9:
        stringFecha="Septiembre/"+fecha.strftime('%y')
    elif mes==10:
        stringFecha="Octubre/"+fecha.strftime('%y')
    elif mes==11:
        stringFecha="Noviembre/"+fecha.strftime('%y')
    elif mes==12:
        stringFecha="Diciembre/"+fecha.strftime('%y')
    return stringFecha
        
#--------------------Views de cuentas Bancarias----------------------------
"Vista de la lista de cuentas bancarias"
class gestionarCuentasBancarias(GroupRequiredMixin,ListView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'facturacion/CuentasBancarias/gestionarCuentasBancarias.html'
    model = cuentaBancaria
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Validacion de que exista el proyecto"
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)
    
    "Se envia el parametro del id del proyecto por url y la lista de cuentas bancarias"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('idp', None) 
        context['idp'] = id
        context['cuentaBancaria'] = cuentaBancaria.objects.filter(proyectoTuristico__id=id)
        return context

"Vista del formulario para agregar cuentas bancarias"
class agregarCuentaBancaria(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'facturacion/CuentasBancarias/agregarCuentaBancaria.html'
    form_class = agregarCuentaBancariaForm
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Validacion de que exista el proyecto turistico"
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)
    
    "Metodo para obtener la url de exito"
    def get_url_redirect(self, **kwargs):
        idp = self.kwargs.get('idp', None) 
        return reverse_lazy('cuentas', kwargs={'idp': idp})

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        context['idp'] = idp         
        return context

    def form_valid(self, form, **kwargs):
        idp = self.kwargs.get('idp', None) 
        cuentaBancaria = form.save(commit=False)
        try:
            cuentaBancaria.proyectoTuristico = proyectoTuristico.objects.get(id=idp)
            cuentaBancaria.identificador = str(cuentaBancaria.numeroCuentaBancaria)
            cuentaBancaria.save()
            messages.success(self.request, 'La cuenta bancaria se ha guardado con éxito')
        except Exception:
            messages.error(self.request, 'Ocurrió un error al guardar la cuenta bancaria, la cuenta bancaria no es válido')
        return HttpResponseRedirect(self.get_url_redirect())
    
#Eliminar prima 
class EliminarPrima(GroupRequiredMixin,TemplateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema',u'Operador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) 
        id = self.kwargs.get('idv', None) 
        try:
            detalleVenta.objects.get(pk = id)
            return reverse_lazy('detalleLote', kwargs={'idp': idp, 'pk': id})
        except Exception:
            return reverse_lazy('gestionarLotes', kwargs={'idp': idp})

    def get(self,request,*args,**kwargs):
        context=super().get_context_data(**kwargs) 
        id = self.kwargs.get('id', None)
        try:
            primas = prima.objects.get(numeroReciboPrima = id)
            pagos = pago.objects.get(prima_id = id)
            try:
                condiciones = condicionesPago.objects.get(detalleVenta_id = primas.detalleVenta_id)
                messages.error(self.request, 'Error al eliminar la cuotra de prima, este lote ya cuenta con condiciones de pago establecidas.')
            except Exception:
                primas.delete() 
                pagos.delete()
                messages.success(self.request, 'La prima fue eliminada con exito.')      
        except Exception: 
            messages.error(self.request, 'Ocurrió un error al eliminar la prima, la prima no existe.')
        return HttpResponseRedirect(self.get_url_redirect())
        
#Modificar Prima 
class ModificarPrima(GroupRequiredMixin, UpdateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema',u'Operador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])  
            try:
                detallev= detalleVenta.objects.get(id = self.kwargs['idv'])
                try:
                    condicion = condicionesPago.objects.get(detalleVenta_id = detallev.id)
                    messages.error(self.request, 'Ocurrió un error. Ya existe condiciones de pago, no es posible modificar la cuota de prima')
                    return HttpResponseRedirect(reverse_lazy('detalleLote', kwargs={'idp': self.kwargs['idp'], 'pk': self.kwargs['idv']}))
                except Exception:
                    try:
                        primas = prima.objects.get(numeroReciboPrima=self.kwargs['pk'])
                        if primas.detalleVenta != detallev:
                            messages.error(self.request, 'Ocurrió un error, la cuota de prima no pertenece a el detalle de venta')
                            return HttpResponseRedirect(reverse_lazy('detalleLote', kwargs={'idp': self.kwargs['idp'], 'pk': self.kwargs['idv']}))
                    except Exception:
                        messages.error(self.request, 'Ocurrió un error, el recibo de prima no existe')
                        return HttpResponseRedirect(reverse_lazy('detalleLote', kwargs={'idp': self.kwargs['idp'], 'pk': self.kwargs['idv']}))
            except Exception:
                messages.error(self.request, 'Ocurrió un error, el detalle de venta no existe')
                return HttpResponseRedirect(reverse_lazy('home'))
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    model = prima
    second_model = pago
    third_model = lote
    template_name = 'facturacion/Prima/agregarPrima.html'
    form_class = agregarPrimaForm
    second_form_class = pagoForm
    third_form_class = lotePagoForm
    
    def get_context_data(self, **kwargs):
        context = super(ModificarPrima, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', None)
        primas = self.model.objects.get(numeroReciboPrima = pk)
        pagos = self.second_model.objects.get(prima_id = primas.numeroReciboPrima)        
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance = pagos)
        context['pk'] = pk   
        return context

    def get_form(self, form_class = None, **kwargs):
        form = super().get_form(form_class)
        form.fields['numeroReciboPrima'].disabled = True        
        return form

    def post(self, request, form_class = None, *args, **kwargs):
        self.object = self.get_object
        id_prima = kwargs['pk']       
        primas = self.model.objects.get(numeroReciboPrima = id_prima)
        pagos = self.second_model.objects.get(prima_id = primas.numeroReciboPrima)
        form = self.form_class(request.POST, instance = primas)
        form.fields['numeroReciboPrima'].disabled = True 
        
        form2 = self.second_form_class(request.POST, instance = pagos)
        idp = self.kwargs.get('idp', None) 
        id = self.kwargs.get('idv', None) 
        if form.is_valid() and form2.is_valid():
            primasF = form.save(commit = False)
            pagosF = form2.save(commit = False)          
            if pagosF.tipoPago == 1:
                pagosF.referencia = ''
                pagosF.cuentaBancaria = None

            primasF.save()
            pagosF.save()
            messages.success(self.request, 'Prima actualizada exitosamente')
        else: 
            messages.error(self.request, 'Ocurrió un error, el recibo de prima no se actualizo')
        return HttpResponseRedirect(reverse_lazy('detalleLote', kwargs={'idp': idp, 'pk': id}))  
       
    
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
            fecha = str(pagoRecibo.fechaPago).split(sep='-')
            f = reversed(fecha)
            
            for x in f:
                if ws.cell(row=15,column=2).value is None:
                    ws.cell(row=15,column=2).value = x 
                else:
                    ws.cell(row=15,column=2).value = str(ws.cell(row=15,column=2).value) +"                    "+x  
            ws['B15'].alignment = Alignment(horizontal="right",vertical="center")
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
                fecha = str(pagoRecibo.fechaPago).split(sep='-')
                f = reversed(fecha)
                
                for x in f:
                    if ws.cell(row=16,column=2).value is None:
                        ws.cell(row=16,column=2).value = x 
                    else:
                        ws.cell(row=16,column=2).value = str(ws.cell(row=16,column=2).value) +"                    "+x  
                ws['B16'].alignment = Alignment(horizontal="right",vertical="center")


                
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
    
    

    