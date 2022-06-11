from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from .models import *
from apps.inventario.models import cuentaBancaria, detalleVenta, lote
from django import forms

class DateInput(forms.DateInput): 
    input_type = 'date'


class agregarPrimaForm(ModelForm):
    class Meta:
        model = prima
        fields = ('numeroReciboPrima','conceptoPrima',)
        label= {
            'numeroReciboPrima':_('Numero de Recibo de la Prima: '),
            'conceptoPrima': _('Concepto Prima'),
        }
        help_texts = {
            'numeroReciboPrima':_('Campo Obligatorio'),
            'conceptoPrima': _('Campo Obligatorio'),
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
            'cuentaBancaria':_('Cuenta Bancaria'),
            'monto':_('Monto de la prima'),
            'tipoPago':_('Tipo de Pago'),
            'referencia':_('Referencia'),
            'fechaPago':_('Fecha de pago de prima'),
            'observaciones':_('Ingrese observaciones')
        }
        help_texts = {
            'cuentaBancaria':('Campo Obligatorio'),
            'monto':('Campo Obligatorio'),
            'tipoPago':('Campo Obligatorio'),
            'referencia':('Campo Obligatorio'),
            'fechaPago':('Campo Obligatorio'),
            'observaciones':('Campo opcional')
        }

        widgets = { 'fechaPago': DateInput(), }
        
        

class agregarPagoMantenimientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(agregarPagoMantenimientoForm, self).__init__(*args, **kwargs)
            #self.fields['numeroReciboMantenimiento'].widget.error_messages = {'required': 'aaa'}

    class Meta:
        model = pagoMantenimiento
        fields = {'numeroReciboMantenimiento','conceptoOtros','montoOtros'}
        label= {
            'numeroReciboMantenimiento': _('Numero de Recibo'),
            'conceptoOtros': _('Concepto Otros'),
            'montoOtros': _('Monto Otros'),
        }
        help_texts = {
            'numeroReciboMantenimiento': _('Campo Obligatorio'),
            'conceptoOtros': _('Campo Opcional'),
            'montoOtros': _('Campo Opcional'),
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
            self.fields['nombreCuentaBancaria'].widget.attrs['pattern'] = "^([A-ZÑÁÉÍÓÚ]{1}[a-zñáéíóú]+[\s]*)+$"
            self.fields['tipoCuenta'].widget.attrs['pattern'] = "^([A-ZÑÁÉÍÓÚa-zñáéíóú]{1}[A-ZÑÁÉÍÓÚa-zñáéíóú]+[\s]*)+$"
            self.fields['banco'].widget.attrs['pattern'] = "^([A-ZÑÁÉÍÓÚa-zñáéíóú]{1}[A-ZÑÁÉÍÓÚa-zñáéíóú]+[\s]*)+$"
    class Meta:
        model = cuentaBancaria
        fields = ('numeroCuentaBancaria','nombreCuentaBancaria','tipoCuenta','banco')
        label= {
            'numeroCuentaBancaria': _('Numero cuenta bancaria'),
            'nombreCuentaBancaria': _('Nombre de cuenta'),
            'tipoCuenta': _('Tipo de cuenta'),
            'banco': _('Banco'),
        }
        help_texts = {
            'numeroCuentaBancaria': _('Campo Obligatorio'),
            'nombreCuentaBancaria': _('Campo Obligatorio'),
            'tipoCuenta': _('Campo Obligatorio'),
            'banco': _('Campo Obligatorio'),
        }

