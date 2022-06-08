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
        fields = {'monto','tipoPago','referencia','fechaPago','cuentaBancaria'}
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
    #def __init__(self, *args, **kwargs): 
        #id = kwargs.pop('id', None) 
        #super(lotePagoForm, self).__init__(*args, **kwargs)
        #if id: 
            #self.fields['cuentaBancaria'].queryset = lote.objects.filter(lote__proyectoTuristico=id)

class agregarPagoMantenimientoForm(ModelForm):
    class Meta:
        model = pagoMantenimiento
        fields = {'numeroReciboMantenimiento','conceptoOtros','montoOtros'}
    

class lotePagoForm(forms.Form):
    matricula = forms.ModelChoiceField(queryset=lote.objects.all(),label='Matricula')
    def __init__(self, *args, **kwargs): 
        id = kwargs.pop('id', None) 
        super(lotePagoForm, self).__init__(*args, **kwargs)
        if id: 
            self.fields['matricula'].queryset = lote.objects.filter(lote__proyectoTuristico=id)



