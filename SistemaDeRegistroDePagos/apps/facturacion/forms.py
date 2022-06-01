from dataclasses import fields
from django.forms import ModelForm
from .models import prima

class agregarPrimaForm(ModelForm):
    class Meta:
        model = prima
        fields = ('numeroReciboPrima','fechaPrima','montoPrima','conceptoPrima')