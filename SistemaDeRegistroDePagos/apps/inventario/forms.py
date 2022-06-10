from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from .models import propietario, detalleVenta, lote, proyectoTuristico
from django.contrib.admin.widgets import FilteredSelectMultiple

class PropietarioForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(PropietarioForm, self).__init__(*args, **kwargs)
            self.fields['dui'].widget.attrs['pattern'] = "[0-9]{8}[ -][0-9]{1}"
            self.fields['telefonoTrabajo'].widget.attrs['pattern'] = "[0-9]{4}[ -][0-9]{4}"
            self.fields['telefonoCasa'].widget.attrs['pattern'] = "[0-9]{4}[ -][0-9]{4}"
            self.fields['telefonoCelular'].widget.attrs['pattern'] = "[0-9]{4}[ -][0-9]{4}"
            self.fields['correoElectronico'].widget.attrs['pattern'] = "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2, 4}$"

    class Meta:
        model=propietario
        fields=('dui','nombrePropietario','direccion','profesion','trabajo','direccionTrabajo','telefonoTrabajo','telefonoCasa','telefonoCelular','correoElectronico')
        labels = {
            'dui': _('DUI:'),
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
            'trabajo': _('Campo Opcional'),
            'direccionTrabajo': _('Campo Opcional'),
            'telefonoTrabajo': _('Campo Opcional'),
            'telefonoCasa': _('Campo Opcional'),
            'telefonoCelular': _('Campo Obligatorio'),
            'correoElectronico': _('Campo Opcional'),
        }
        error_messages = {
            'nombrePropietario': {
                'max_length': _("El dato ingresado es demasiado largo"),
            },
        }

class DetalleVentaForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(DetalleVentaForm, self).__init__(*args, **kwargs)
            self.fields['precioVenta'].widget.attrs['pattern'] = "[0-9]{3}"
            self.fields['descuento'].widget.attrs['pattern'] = "[0-9]{3}"
            self.fields['estado'].widget.attrs['pattern'] = "[A-Z]{5}"
    class Meta:
        model=detalleVenta
        fields=('precioVenta','descuento','estado')
        labels = {
            'precioVenta': _('Precio de venta:'),
            'descuento': _('Descuento:'),
            'estado': _('Estado:'),
        }
        help_texts = {
            'precioVenta': _('Campo Obligatorio'),
            'descuento': _('Campo Obligatorio'),
            'estado': _('Campo Obligatorio'),
        }

class detalleVentaPropietarioForm(ModelForm):

    class Meta:
        model=detalleVenta
        fields=('propietarios',)

class LoteForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(LoteForm, self).__init__(*args, **kwargs)
            self.fields['matriculaLote'].widget.attrs['pattern'] = "[0-9]{8}"
            self.fields['numeroLote'].widget.attrs['pattern'] = "[0-9]{3}"
            self.fields['poligono'].widget.attrs['pattern'] = "[A-Z]{1}"
            self.fields['areaMCuadrado'].widget.attrs['pattern'] = "[0-9]{5}"
            self.fields['areaVCuadrada'].widget.attrs['pattern'] = "[0-9]{5}"

    class Meta:
        model=lote
        fields=('matriculaLote','proyectoTuristico','numeroLote','poligono','areaMCuadrado','areaVCuadrada')
        labels = {
            'matriculaLote': _('Matrícula:'),
            'numeroLote': _('Número de lote:'),
            'poligono': _('Polígono:'),
            'areaMCuadrado': _('Área en metros cuadrados:'),
            'areaVCuadrada': _('Área en varas cuadradas:'),
        }
        help_texts = {
            'matriculaLote': _('Campo Obligatorio'),
            'numeroLote': _('Campo Obligatorio'),
            'poligono': _('Campo Obligatorio'),
            'areaMCuadrado': _('Campo Obligatorio'),
            'areaVCuadrada': _('Campo Obligatorio'),
        }

class agregarProyectoForm(ModelForm):
    class Meta:
        model= proyectoTuristico
        fields=('nombreProyectoTuristico','empresa')
        labels = {
            'nombreProyectoTuristico': _('Nombre Proyecto Turistico:'),
            'empresa': _('Empresa:'),
        }
        help_texts = {
            'nombreProyectoTuristico': _('Campo Obligatorio'),
            'empresa': _('Campo Obligatorio'),
        }
        error_messages = {
            'nombreProyectoTuristico': {
                'max_length': _("El dato ingresado es demasiado largo"),
            },
        }
