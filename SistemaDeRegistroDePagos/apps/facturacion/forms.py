from dataclasses import fields
from django.utils.translation import gettext_lazy as _
from django.forms import CheckboxInput, ModelForm, widgets
from .models import *
from apps.inventario.models import cuentaBancaria, detalleVenta, lote
from django import forms

class DateInput(forms.DateInput): 
    input_type = 'date'


class agregarPrimaForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(agregarPrimaForm, self).__init__(*args, **kwargs)
            self.fields['numeroReciboPrima'] = forms.IntegerField()
    class Meta:
        model = prima
        fields = ('numeroReciboPrima','conceptoPrima',)
        label= {
            'numeroReciboPrima':('Numero de Recibo de la Prima: '),
            'conceptoPrima': ('Concepto Prima: '),
        }
        help_texts = {
            'numeroReciboPrima':('Campo Obligatorio'),
            'conceptoPrima': ('Campo Obligatorio'),
        }


class pagoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        id = kwargs.pop('id', None)
        super(pagoForm, self).__init__(*args, **kwargs)
        if id:  
            self.fields['cuentaBancaria'].queryset = cuentaBancaria.objects.filter(proyectoTuristico__id=id)
                
    class Meta:
        model = pago
        fields = {'monto','tipoPago','referencia','fechaPago','cuentaBancaria','observaciones'}
        label = {
            'cuentaBancaria':('Cuenta Bancaria'),
            'monto':('Monto de la prima'),
            'tipoPago':('Tipo de Pago'),
            'referencia':('Referencia'),
            'fechaPago':('Fecha de pago de prima'),
            'observaciones':('Ingrese observaciones')
        }
        help_texts = {
            'cuentaBancaria':('Campo Obligatorio'),
            'monto':('Campo Obligatorio'),
            'tipoPago':('Campo Obligatorio'),
            'referencia':('Campo Obligatorio'),
            'fechaPago':('Campo Obligatorio'),
            'observaciones':('Campo opcional')
        }

        widgets = { 'fechaPago': DateInput(format=('%Y-%m-%d')), }
      
        
        

class agregarPagoMantenimientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(agregarPagoMantenimientoForm, self).__init__(*args, **kwargs)
            self.fields['numeroReciboMantenimiento'] = forms.IntegerField()

    class Meta:
        model = pagoMantenimiento
        fields = {'numeroReciboMantenimiento','conceptoOtros','montoOtros','conceptoDescuento','descuento'}
        label= {
            'numeroReciboMantenimiento': ('N??mero de Recibo'),
            'conceptoOtros': ('Concepto por Otros Pagos'),
            'montoOtros': ('Monto por Otros Pagos'),
            'conceptoDescuento': ('Concepto por Descuento de Recargo'),
            'descuento': ('Monto por Descuento de Recargo'),
        }
        help_texts = {
            'numeroReciboMantenimiento': ('Campo Obligatorio'),
            'conceptoOtros': ('Campo Opcional'),
            'montoOtros': ('Campo Opcional'),
            'conceptoDescuento': ('Campo Opcional'),
            'descuento': ('Campo Opcional'),
        }
        #error_messages={'required':_("First name is required.")}

class agregarPagoFinanciamientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(agregarPagoMantenimientoForm, self).__init__(*args, **kwargs)
            self.fields['numeroReciboMantenimiento'] = forms.IntegerField()

    class Meta:
        model = pagoMantenimiento
        fields = {'numeroReciboMantenimiento','conceptoOtros','montoOtros','conceptoDescuento','descuento'}
        label= {
            'numeroReciboMantenimiento': ('N??mero de Recibo'),
            'conceptoOtros': ('Concepto por Otros Pagos'),
            'montoOtros': ('Monto por Otros Pagos'),
            'conceptoDescuento': ('Concepto por Descuento de Recargo'),
            'descuento': ('Monto por Descuento de Recargo'),
        }
        help_texts = {
            'numeroReciboMantenimiento': ('Campo Obligatorio'),
            'conceptoOtros': ('Campo Opcional'),
            'montoOtros': ('Campo Opcional'),
            'conceptoDescuento': ('Campo Opcional'),
            'descuento': ('Campo Opcional'),
        }
        #error_messages={'required':_("First name is required.")}

class lotePagoForm(forms.Form):
    matricula = forms.ModelChoiceField(queryset=detalleVenta.objects.all(),label='Lote',help_text = 'Campo Obligatorio. Se muestran solo los lotes que tiene una venta activa')
    def __init__(self, *args, **kwargs):
        id = kwargs.pop('id', None)
        super().__init__(*args, **kwargs)
        if id:        
            self.fields['matricula'].queryset = detalleVenta.objects.filter(lote__proyectoTuristico__id=id, estado=True)

class agregarCuentaBancariaForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(agregarCuentaBancariaForm, self).__init__(*args, **kwargs)
            self.fields['numeroCuentaBancaria'].widget.attrs['pattern'] = "[0-9]{6,20}"
            self.fields['nombreCuentaBancaria'].widget.attrs['pattern'] = "^([A-Z????????????]{1}[a-z????????????]+[\s]*)+$"
            self.fields['tipoCuenta'].widget.attrs['pattern'] = "^([A-Z????????????a-z????????????]{1}[A-Z????????????a-z????????????]+[\s]*)+$"
            self.fields['banco'].widget.attrs['pattern'] = "^([A-Z????????????a-z????????????]{1}[A-Z????????????a-z????????????]+[\s]*)+$"
    class Meta:
        model = cuentaBancaria
        fields = ('numeroCuentaBancaria','nombreCuentaBancaria','tipoCuenta','banco')
        label= {
            'numeroCuentaBancaria': _('Numero de cuenta bancaria'),
            'nombreCuentaBancaria': _('Nombre de cuenta'),
            'tipoCuenta': _('Tipo de cuenta'),
            'banco': _('Banco'),
        }
        help_texts = {
            'numeroCuentaBancaria': _('Campo Obligatorio. Solo se permiten numeros con un min??mo de 6 d??gitos y m??ximo 20.'),
            'nombreCuentaBancaria': _('Campo Obligatorio. Escriba un nombre propio, teniendo en cuenta que no se permiten n??meros.'),
            'tipoCuenta': _('Campo Obligatorio. Escriba un nombre propio, teniendo en cuenta que no se permiten n??meros.'),
            'banco': _('Campo Obligatorio. Escriba un nombre propio, teniendo en cuenta que no se permiten n??meros.'),
        }


class resumenForm(forms.Form):
   
    resumenPrima = forms.BooleanField(required=False, initial=False)
    resumenPagoM = forms.BooleanField(required=False, initial=False)
    resumenPagoF = forms.BooleanField(required=False, initial=False)
    fechaInicio = forms.DateField(widget=DateInput())
    fechaFin = forms.DateField(widget=DateInput())
   

