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
        fields = {'monto','tipoPago','referencia','fechaPago'}
        label = {
            'monto':('Monto de la prima'),
            'tipoPago':('Tipo de Pago'),
            'referencia':('Referencia'),
            'fechaPago':('Fecha de pago de prima'),
        }
        help_texts = {
            'monto':('Campo Obligatorio'),
            'tipoPago':('Campo Obligatorio'),
            'referencia':('Campo Obligatorio'),
            'fechaPago':('Campo Obligatorio'),
        }
class bancoPagoForm(forms.Form):
    banco = forms.ModelChoiceField(queryset = cuentaBancaria.objects.all(), label = 'banco')
    ields = {'bancox',}
    help_texts = {
            'bancox':('Campo Obligatorio'),
        }
    def __init__(self, *args, **kwargs):
        id = kwargs.pop('id', None)
        super(bancoPagoForm, self).__init__(*args, **kwargs)
        if id:
            self.fields('banco').queryset = cuentaBancaria.objects.filter(cuentaBancaria__banco=id)
        

"""class agregarPagoMantenimientoForm(ModelForm):
    class Meta:
        model = pagoMantenimiento
        fields = ('numeroReciboMantenimiento','fechaPago','monto','conceptoOtros','montoOtros')"""
