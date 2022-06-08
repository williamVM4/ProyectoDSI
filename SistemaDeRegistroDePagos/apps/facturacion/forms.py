from cProfile import label
from dataclasses import fields
from django.forms import ModelForm
from .models import pagoMantenimiento, prima

"""class agregarPrimaForm(ModelForm):
    class Meta:
        model = prima
        fields = ('numeroReciboPrima','fechaPrima','montoPrima','conceptoPrima','tipoPago','referencia','cuentaBancaria',)
        label= {
            'numeroReciboPrima':('Numero de Recibo de la Prima: '),
            'fechaPrima': ('Fecha Prima'),
            'montoPrima': ('Monto Prima'),
            'conceptoPrima': ('Concepto Prima'),
        }
        help_texts = {
            'numeroReciboPrima':('Campo Obligatorio'),
            'fechaPrima': ('Campo Obligatorio'),
            'montoPrima': ('Campo Obligatorio'),
            'conceptoPrima': ('Campo Obligatorio'),
        }

class agregarPagoMantenimientoForm(ModelForm):
    class Meta:
        model = pagoMantenimiento
        fields = ('numeroReciboMantenimiento','fechaPago','monto','conceptoOtros','montoOtros')"""
