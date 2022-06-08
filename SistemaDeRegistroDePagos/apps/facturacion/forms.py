from cProfile import label
from dataclasses import fields
from statistics import mode
from django.forms import ModelForm
from .models import *
from apps.inventario.models import lote
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
            'monto':(''),
            'tipoPago':(''),
            'referencia':(''),
            'fechaPago':(''),
        }
        help_texts = {
            'monto':(''),
            'tipoPago':(''),
            'referencia':(''),
            'fechaPago':(''),
        }

class agregarPagoMantenimientoForm(ModelForm):
    class Meta:
        model = pagoMantenimiento
        fields = {'numeroReciboMantenimiento','conceptoOtros','montoOtros'}

class lotePagoForm(forms.Form):
    matricula = forms.CharField(label='Matricula', max_length=100)
