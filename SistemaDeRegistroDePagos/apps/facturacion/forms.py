from dataclasses import fields
from django.forms import ModelForm
from .models import pagoMantenimiento, prima

class agregarPrimaForm(ModelForm):
    class Meta:
        model = prima
        fields = ('numeroReciboPrima','fechaPrima','montoPrima','conceptoPrima')

class agregarPagoMantenimientoForm(ModelForm):
    class Meta:
        model = pagoMantenimiento
        fields = ('numeroReciboMantenimiento','fechaPago','monto','conceptoOtros','montoOtros')