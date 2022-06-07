from cProfile import label
from dataclasses import fields
from django.forms import ModelForm
from .models import prima

class agregarPrimaForm(ModelForm):
    class Meta:
        model = prima
        fields = ('numeroReciboPrima','fechaPrima','montoPrima','conceptoPrima')
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