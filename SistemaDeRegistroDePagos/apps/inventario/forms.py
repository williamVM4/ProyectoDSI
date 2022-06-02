from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from .models import propietario, detalleVenta

class PropietarioForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(PropietarioForm, self).__init__(*args, **kwargs)
            self.fields['telefonoTrabajo'].widget.attrs['pattern'] = "[0-9]{4}[ -][0-9]{4}"
            self.fields['telefonoCasa'].widget.attrs['pattern'] = "[0-9]{4}[ -][0-9]{4}"
            self.fields['telefonoCelular'].widget.attrs['pattern'] = "[0-9]{4}[ -][0-9]{4}"

    class Meta:
        model=propietario
        fields=('dui','nombrePropietario','direccion','profesion','trabajo','direccionTrabajo','telefonoTrabajo','telefonoCasa','telefonoCelular','correoElectronico')
        labels = {
            'nombrePropietario': _('Nombre:'),
            'direccion': _('Dirección:'),
            'profesion': _('Profesión:'),
            'trabajo': _('Trabajo:'),
            'direccionTrabajo': _('Dirección del trabajo:'),
            'telefonoTrabajo': _('Telefono del trabajo:'),
            'telefonoCasa': _('Telefono de casa:'),
            'telefonoCelular': _('Telefono celular:'),
            'correoElectronico': _('Correo electronico:'),
        }
        help_texts = {
            'dui': _('Campo Obligatorio'),
            'nombrePropietario': _('Campo Obligatorio'),
            'direccion': _('Campo Obligatorio'),
            'profesion': _('Campo Obligatorio'),
            'telefonoCelular': _('Campo Obligatorio'),
        }
        error_messages = {
            'nombrePropietario': {
                'max_length': _("El dato ingresado es demasiado largo"),
            },
        }

class detalleVentaPropietarioForm(ModelForm):
    class Meta:
        model=detalleVenta
        fields=('propietarios',)