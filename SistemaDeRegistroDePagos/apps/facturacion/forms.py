from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
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
        fields = {'numeroReciboMantenimiento','conceptoOtros','montoOtros'}
        label= {
            'numeroReciboMantenimiento': ('Numero de Recibo'),
            'conceptoOtros': ('Concepto Otros'),
            'montoOtros': ('Monto Otros'),
        }
        help_texts = {
            'numeroReciboMantenimiento': ('Campo Obligatorio'),
            'conceptoOtros': ('Campo Opcional'),
            'montoOtros': ('Campo Opcional'),
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
            'numeroCuentaBancaria': _('Campo Obligatorio. Solo se permiten numeros'),
            'nombreCuentaBancaria': _('Campo Obligatorio. El nombre de la cuenta debe iniciar con mayuscula, no debe contener numeros'),
            'tipoCuenta': _('Campo Obligatorio. El nombre del tipo de cuenta debe iniciar con mayuscula, no debe contener numeros'),
            'banco': _('Campo Obligatorio. El nombre del banco debe iniciar con mayuscula, no debe contener numeros'),
        }

