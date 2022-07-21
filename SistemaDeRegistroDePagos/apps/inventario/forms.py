from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, ValidationError
from .models import asignacionProyecto, propietario, detalleVenta, lote, proyectoTuristico
from apps.monitoreo.models import condicionesPago
from django import forms

class DateInput(forms.DateInput): 
    input_type = 'date'

class PropietarioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.idp = kwargs.pop('idp', None)
        super(PropietarioForm, self).__init__(*args, **kwargs)
        self.fields['dui'].widget.attrs['pattern'] = "[0-9]{8}[ -][0-9]{1}"
        self.fields['telefonoTrabajo'].widget.attrs['pattern'] = "[0-9]{4}[ -][0-9]{4}"
        self.fields['telefonoTrabajo'].widget.attrs['data-mask'] = "[0-9]{4}[ -][0-9]{4}"
        self.fields['nombrePropietario'].widget.attrs['pattern'] = "^([A-ZÑÁÉÍÓÚa-zñáéíóú]{1}[A-ZÑÁÉÍÓÚa-zñáéíóú]+[\s]*)+$"
        self.fields['telefonoCasa'].widget.attrs['pattern'] = "[0-9]{4}[ -][0-9]{4}"
        self.fields['telefonoTrabajo'].widget.attrs['pattern'] = "[0-9]{4}[ -][0-9]{4}"
        self.fields['correoElectronico'].widget.attrs['pattern'] = "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2, 4}$"

    class Meta:
        model=propietario
        fields=('dui','nombrePropietario','direccion','profesion','trabajo','direccionTrabajo','telefonoTrabajo','telefonoCasa','telefonoCelular','correoElectronico')
        labels = {
            'dui': _('DUI:'),
            'nombrePropietario': _('Nombre:'),
            'direccion': _('Dirección particular:'),
            'profesion': _('Profesión:'),
            'trabajo': _('Lugar de trabajo:'),
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
    def clean_dui(self):
        dui = self.cleaned_data["dui"]
        asigPro = asignacionProyecto.objects.filter(propietario__dui = dui, proyectoTuristico__id = self.idp).exists()
        if asigPro is True:
            raise ValidationError("Ya existe una persona registrada con este dui, en este proyecto Turistico")
        return dui

class DetalleVentaForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(DetalleVentaForm, self).__init__(*args, **kwargs)
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
            'precioVenta': _('Campo Obligatorio. Solo se permiten números, punto decimal y su parte decimal no debe exceder 2 dígitos'),
            'descuento': _('Campo Obligatorio. Solo se permiten números, punto decimal y su parte decimal no debe exceder 2 dígitos'),
            'estado': _('Campo Obligatorio'),
        }
    def clean_descuento(self):
        descuento = self.cleaned_data["descuento"]
        precioV = self.cleaned_data["precioVenta"]
        if descuento > precioV:
            raise ValidationError("El descuento no puede ser mayor al precio de venta")
        return descuento
    

class detalleVentaPropietarioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        idp = kwargs.pop('idp', None)
        super().__init__(*args, **kwargs)
        if idp:        
            self.fields['propietarios'].queryset = asignacionProyecto.objects.filter(proyectoTuristico__id=idp)

    class Meta:
        model=detalleVenta
        fields=('propietarios',)

class LoteForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(LoteForm, self).__init__(*args, **kwargs)
            self.fields['matriculaLote'].widget.attrs['pattern'] = "^\d{8}"
            self.fields['numeroLote'].widget.attrs['pattern'] = "^\d{1}(\d+)?"
            self.fields['poligono'].widget.attrs['pattern'] = "^([A-Z]{1}[a-z]?)"
            self.fields['areaMCuadrado'].widget.attrs['pattern'] = "^\d+(.{1}\d{2})?"
            self.fields['areaVCuadrada'].widget.attrs['pattern'] = "^\d+(.{1}\d{2})?"

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
            'matriculaLote': _('Campo Obligatorio. Solo se permiten números, minimo 8 carácteres numericos'),
            'numeroLote': _('Campo Obligatorio. Solo se permiten números, minimo 1 carácter numérico'),
            'poligono': _('Campo Obligatorio. Pa=Polígono(P)Porcion(a)'),
            'areaMCuadrado': _('Campo Obligatorio. Solo se permiten números, punto decimal y su parte decimal no debe exceder 2 dígitos'),
            'areaVCuadrada': _('Campo Obligatorio'),
        }
    
    def clean_matriculaLote(self):
        data = self.cleaned_data["matriculaLote"]
        existe = lote.objects.filter(matriculaLote=data).exists()
        if existe is True:
            raise ValidationError("Ya existe un lote registrado con la matricula ingresada.")
        return data
    


class agregarProyectoForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(agregarProyectoForm, self).__init__(*args, **kwargs)
            self.fields['nombreProyectoTuristico'].widget.attrs['pattern'] = "^([A-ZÑÁÉÍÓÚa-zñáéíóú]{1}[A-ZÑÁÉÍÓÚa-zñáéíóú]+[\s]*)+$"
            self.fields['empresa'].widget.attrs['pattern'] = "^([A-ZÑÁÉÍÓÚa-zñáéíóú]{1}[A-ZÑÁÉÍÓÚa-zñáéíóú]+[\s]*)+$"
    class Meta:
        model= proyectoTuristico
        fields=('nombreProyectoTuristico','empresa')
        labels = {
            'nombreProyectoTuristico': _('Nombre Proyecto Turistico:'),
            'empresa': _('Empresa:'),
        }
        help_texts = {
            'nombreProyectoTuristico': _('Campo Obligatorio. Escriba un nombre propio, teniendo en cuenta que no se permiten números ni caracteres especiales.'),
            'empresa': _('Campo Obligatorio. Escriba un nombre propio, teniendo en cuenta que no se permiten números ni caracteres especiales.'),
        }
        error_messages = {
            'nombreProyectoTuristico': {
                'max_length': _("El dato ingresado es demasiado largo"),
            },
        }
    def clean_nombreProyectoTuristico(self):
        nombreProyectoTuristico = self.cleaned_data["nombreProyectoTuristico"]
        if proyectoTuristico.objects.filter(nombreProyectoTuristico = nombreProyectoTuristico).exists():
            raise ValidationError("Ya existe un Proyecto Turistico registrado con este nombre")
        return nombreProyectoTuristico

class condicionPagoForm(ModelForm):

    class Meta:
        model=condicionesPago
        fields=('fechaEscrituracion','montoFinanciamiento','plazo','tasaInteres','cuotaKi','comisionCuota','mantenimientoCuota','multaMantenimiento','multaFinanciamiento')
        labels = {
            'fechaEscrituracion': _('Fecha de escrituración:'),
            'montoFinanciamiento': _('Monto de financiamiento:'),
            'plazo': _('Plazo:'),
            'tasaInteres': _('Tasa de interés:'),
            'cuotaKi': _('Cuota de capital e intereses:'),
            'comisionCuota': _('Comisión por administración y supervisión:'),
            'mantenimientoCuota': _('Cuota de mantenimiento:'),
            'multaMantenimiento': _('Multa por mantenimiento:'),
            'multaFinanciamiento': _('Multa por financiamiento:'),
        }
        help_texts = {
            'fechaEscrituracion': _('Campo Obligatorio'),
            'montoFinanciamiento': _('Campo Obligatorio. Solo números'),
            'plazo': _('Campo Obligatorio. Solo números enteros'),
            'tasaInteres': _('Campo Obligatorio. En porcentaje sin el simbolo %'),
            'cuotaKi': _('Campo Obligatorio. Solo números'),
            'comisionCuota': _('Campo Obligatorio. Solo números'),
            'mantenimientoCuota': _('Campo Obligatorio. Solo números'),
            'multaMantenimiento': _('Campo Obligatorio. Solo números'),
            'multaFinanciamiento': _('multaFinanciamiento. Solo números'),
        }

        widgets = { 'fechaEscrituracion': DateInput(format=('%Y-%m-%d')), }
