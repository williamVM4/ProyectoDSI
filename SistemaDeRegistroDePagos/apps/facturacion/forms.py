from cProfile import label
from dataclasses import fields
from statistics import mode
from django.forms import ModelForm
from .models import *
from apps.inventario.models import cuentaBancaria, lote
from django import forms
class agregarPrimaForm(ModelForm):
    class Meta:
        model = prima
        fields = ('numeroReciboPrima','conceptoPrima',)
        label= {
            'numeroReciboPrima':('Numero de Recibo de la Prima: '),
            'conceptoPrima': ('Concepto Prima'),
        }
        help_texts = {
            'numeroReciboPrima':('Campo Obligatorio'),
            'conceptoPrima': ('Campo Obligatorio'),
        }



class pagoForm(ModelForm):
    class Meta:
        model = pago
        fields = {'monto','tipoPago','referencia','fechaPago','cuentaBancaria'}
        label = {
            'cuentaBancaria':('Cuenta Bancaria'),
            'monto':('Monto de la prima'),
            'tipoPago':('Tipo de Pago'),
            'referencia':('Referencia'),
            'fechaPago':('Fecha de pago de prima'),
        }
        help_texts = {
            'cuentaBancaria':('Campo Obligatorio'),
            'monto':('Campo Obligatorio'),
            'tipoPago':('Campo Obligatorio'),
            'referencia':('Campo Obligatorio'),
            'fechaPago':('Campo Obligatorio'),
        }
    def __init__(self, *args, **kwargs):
        id = kwargs.pop('id', None)
        super(pagoForm, self).__init__(*args, **kwargs)
        if id:  
            self.fields['cuentaBancaria'].queryset = cuentaBancaria.objects.filter(proyectoTuristico__id=id)
        

class agregarPagoMantenimientoForm(ModelForm):
    class Meta:
        model = pagoMantenimiento
        fields = {'numeroReciboMantenimiento','conceptoOtros','montoOtros'}
        label= {
            'numeroReciboMantenimiento':('Numero de Recibo'),
            'conceptoOtros': ('Concepto Otros'),
            'montoOtros': ('Monto Otros'),
        }
        help_texts = {
            'numeroReciboMantenimiento':('Campo Obligatorio'),
            'conceptoOtros': ('Campo Opcional'),
            'montoOtros': ('Campo Opcional'),
        }
    

class lotePagoForm(forms.Form):
    matricula = forms.ModelChoiceField(queryset=lote.objects.all(),label='Matricula',help_text = 'Campo Obligatorio')
    def __init__(self, *args, **kwargs):
        id = kwargs.pop('id', None)
        super().__init__(*args, **kwargs)
        if id:        
            self.fields['matricula'].queryset = lote.objects.filter(proyectoTuristico__id=id)



