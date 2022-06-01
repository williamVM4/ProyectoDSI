from dataclasses import fields
from django.forms import ModelForm
from .models import propietario

class PropietarioForm(ModelForm):
    class Meta:
        model=propietario
        fields=('nombrePropietario','direccion','profesion','trabajo','direccionTrabajo','telefonoTrabajo','telefonoCasa','telefonoCelular','correoElectronico')