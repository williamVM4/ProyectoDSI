from contextlib import redirect_stderr
import decimal
import math
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.facturacion.models import pago, pagoMantenimiento, prima, pagoCuotaMantenimiento
from apps.monitoreo.models import estadoCuenta
from apps.inventario.models import asignacionLote, asignacionProyecto, detalleVenta, lote, proyectoTuristico
from apps.autenticacion.mixins import *
from django.contrib import messages
from django.db.models import Sum
from .forms import *


#----------------------------Views de lote-------------------------------
"""Vista donde se muestra la lista de todos los lotes del proyecto turistico
    Se hereda de GroupRequiredMixin para validar los grupos que tienen acceso a la vista"""
class gestionarLotes(GroupRequiredMixin,ListView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'inventario/Lote/gestionarLotes.html'
    model = lote
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Validacion de que exista proyecto"""
        proyecto = proyectoTuristico.objects.filter(pk=self.kwargs['idp']).exists()
        if proyecto is False:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        "id del proyecto pasado por url"
        id = self.kwargs.get('idp', None)
        "id del proyecto"
        context['idp'] = id
        "Lista de lotes filtrada por proyecto turistico"
        context['lotes'] = lote.objects.filter(proyectoTuristico__id=id)
        "Lista de los detalles de venta activos de cada lote del proyecto turistico"
        context['detalles'] = detalleVenta.objects.filter(lote__proyectoTuristico__id=id, estado=True)
        return context


"""Vista donde se muestra el detalle de las generalidades de la venta del lote"""
class detalleLote(GroupRequiredMixin,DetailView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'inventario/Lote/detalleLote.html'
    model = detalleVenta
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Validacion de que el proyecto turistico de la url exista"
        proyecto = proyectoTuristico.objects.filter(pk=self.kwargs['idp']).exists()
        if proyecto is False:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        "Validacion de que exista el detalle de venta de la url"
        det = detalleVenta.objects.filter(pk=self.kwargs['pk']).exists()
        if det is False:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el detalle de la venta existe')
            return HttpResponseRedirect(reverse_lazy('gestionarLotes', kwargs={'idp': self.kwargs['idp']}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        "id del proyecto turistico"
        idp = self.kwargs.get('idp', None)
        "id del detalle de venta"
        id = self.kwargs.get('pk', None)
        sumPrima=0.00 #Para guardar lo acumulado en primas
        det = detalleVenta.objects.get(pk=id) # se obtiene el detalle de venta
        pagosp = pago.objects.filter(prima__detalleVenta=det.id) # se obtienen las primas para realizar la sumatorias
        "Se verifica si existe condiciones de pago activas para el calculo de cuota por financiamiento"
        condiciones=condicionesPago.objects.filter(detalleVenta_id = det.id).annotate(cuotaFinanciamiento=Sum('cuotaKi')+Sum('comisionCuota')).order_by('-id')
        "Verficar si no da problemas"
        estadosDeCuentaM=estadoCuenta.objects.filter(condicionesPago__detalleVenta__id = det.id).exists()
        if estadosDeCuentaM==True:
            estadosDeCuentaM=estadoCuenta.objects.filter(condicionesPago__detalleVenta__id = det.id).order_by('-id')
        "Sumatoria de primas"
        for pagoObject in pagosp:
            if pagoObject.prima !=None:
                sumPrima=sumPrima+float(pagoObject.monto)
        context['idp'] = idp   
        context['id'] = id
        context['asignaciones'] = asignacionLote.objects.filter(detalleVenta_id = det.id)  
        context['primas'] = prima.objects.filter(detalleVenta_id = det.id)
        context['condiciones'] = condiciones
        context['pagos'] = pago.objects.filter() 
        context['detalleV'] = det
        context['sumPrima'] = round(sumPrima,2)
        context['estadosDeCuentaM'] = estadosDeCuentaM    
        return context 


"""Vista de formulario para agregar lote"""
class agregarLote(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'inventario/Lote/agregarLote.html'
    form_class = LoteForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Validacion de que el proyecto turistico de la url exista"
        proyecto = proyectoTuristico.objects.filter(pk=self.kwargs['idp']).exists()
        if proyecto is False:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_url_redirect(self, **kwargs):
        """ Url de exito de formulario con el parametro id del proyecto"""
        idp = self.kwargs.get('idp', None) 
        return reverse_lazy('gestionarLotes', kwargs={'idp': idp})

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) #id del proyecto
        context['idp'] = idp         
        return context
        
    def get_form(self, form_class = None, **kwargs):
        form = super().get_form(form_class)
        form.fields['areaVCuadrada'].disabled = True #deshabilitar el campo varas cuadradas
        return form

    def form_valid(self, form, **kwargs):
        lote = form.save(commit=False) #objeto del formulario
        lote.identificador = str(lote.poligono) + str(lote.numeroLote) #Concatenar numero y poligono para el identificador
        lote.areaVCuadrada = lote.areaMCuadrado * decimal.Decimal(1.4308) #Calculo de las varas cuadradas
        lote.proyectoTuristico=proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        lote.save()
        messages.success(self.request, 'Lote guardado con éxito')
        return HttpResponseRedirect(self.get_url_redirect())

#----------------------------Fin Views de lote------------------------------------
#--------------------Views de detalle de venta-------------------------------------
"""Vista donde se muestra la tabla de lotes del proyecto y un boton para visualizar el historico de ventas"""
class historicoVentas(GroupRequiredMixin,ListView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'inventario/DetalleVenta/historicoVentas.html'
    model = lote
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Validacion de que el proyecto turistico de la url exista"
        proyecto = proyectoTuristico.objects.filter(pk=self.kwargs['idp']).exists()
        if proyecto is False:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('idp', None) 
        context['idp'] = id #id del proyecto turistico
        context['lotes'] = lote.objects.filter(proyectoTuristico__id=id) #Lista de lotes por proyecto turistico
        return context


"""Vista donde se muestra el historico de ventas de un lote en especifico"""
class historicoVentasLote(GroupRequiredMixin,DetailView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'inventario/Asignaciones/asignacionLote.html'
    model = lote
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Validacion de que el proyecto turistico de la url exista"
        proyecto = proyectoTuristico.objects.filter(pk=self.kwargs['idp']).exists()
        if proyecto is False:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        "Validacion de que el lote de la url exista"
        lot = lote.objects.filter(pk=self.kwargs['pk']).exists()
        if lot is False:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el lote existe')
            return HttpResponseRedirect(reverse_lazy('gestionarLotes', kwargs={'idp': self.kwargs['idp']}))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) #id del proyecto turistico
        id = self.kwargs.get('pk', None)# id del lote
        context['idp'] = idp #id del proyecto turistico
        context['detalles'] = detalleVenta.objects.filter(lote__matriculaLote=id).order_by('-estado') #listado de detalles de venta, primero se muestra el activo
        #context['asignaciones'] = asignacionLote.objects.filter(detalleVenta__lote__matriculaLote = id) #listado de 
        context['condiciones'] = condicionesPago.objects.filter(detalleVenta__lote__matriculaLote = id)
        return context


"""Vista de formulario para agregar un detalle de venta"""
class agregarDetalleVenta(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'inventario/DetalleVenta/agregarDetalleVenta.html'
    form_class = DetalleVentaForm
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Validacion de que el proyecto turistico de la url exista"
        proyecto = proyectoTuristico.objects.filter(pk=self.kwargs['idp']).exists()
        if proyecto is False:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        "Validacion de que el lote de la url exista"
        lot = lote.objects.filter(pk=self.kwargs['idl']).exists()
        if lot is False:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el lote existe')
            return HttpResponseRedirect(reverse_lazy('gestionarLotes', kwargs={'idp': self.kwargs['idp']}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        idl = self.kwargs.get('idl', None)
        context['idp'] = idp #id del proyecto
        context['idl'] = idl #id del lote         
        return context

    def form_valid(self, form, **kwargs):
        """Se recogen los parametros de la url y el formulario"""
        idl = self.kwargs.get('idl', None)
        idp = self.kwargs.get('idp', None)
        detalle = form.save(commit=False)
        """Se desactivan todos los otros detalles de venta"""
        try:
            otrosdeta = detalleVenta.objects.filter(lote__matriculaLote=idl)
            for d in otrosdeta:
                d.estado = False
                d.save()
            """Se asigna el detalle de venta ingresado como activo, se le asigna el lote y se guarda"""
            detalle.estado = True
            detalle.lote = lote.objects.get(pk=idl)
            detalle.save()
            messages.success(self.request, 'Detalle de venta guardado con éxito')
            return HttpResponseRedirect(reverse_lazy('detalleLote', kwargs={'idp': idp,'pk': detalle.id}))
        except Exception:
            messages.error(self.request, 'Ocurrió un error al guardar el detalle de venta, el detalle de venta no es válido')
            return HttpResponseRedirect(reverse_lazy('gestionarlotes', kwargs={'idp': idp}))

#-----------------------------------Views de propietario--------------------------------
"""Vista del listado de propietarios registrados en el proyecto turistico"""
class consultarPropietarios(GroupRequiredMixin,ListView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'inventario/Propietario/consultarPropietarios.html'
    model = propietario
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Validacion de que el proyecto turistico de la url exista"
        proyecto = proyectoTuristico.objects.filter(pk=self.kwargs['idp']).exists()
        if proyecto is False:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('idp', None) 
        context['idp'] = id #id del proyecto turistico
        "Lista de propietarios filtrada por proyecto turistico y ordenados por dui"
        context['propietarios'] = asignacionProyecto.objects.filter(proyectoTuristico__id=id).order_by('-dui')
        return context

class detallePropietario(GroupRequiredMixin,DetailView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'inventario/Propietario/detallePropietario.html'
    model = propietario
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Validacion de que el proyecto turistico de la url exista"
        proyecto = proyectoTuristico.objects.filter(pk=self.kwargs['idp']).exists()
        if proyecto is False:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('idp', None) 
        idPropietario = self.kwargs.get('pk', None)
        context['idp'] = id #id del proyecto turistico
        "Lista de asignaciones de lotes a las que pertenece el propietario"
        context['lotes'] = asignacionLote.objects.filter(propietario__id = idPropietario)
        return context

"""Vista de formulario para registrar un propietario en un lote determinado"""
class agregarPropietario(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'inventario/Propietario/agregarPropietario.html'
    form_class = PropietarioForm
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Validacion de que el proyecto turistico de la url exista"
        proyecto = proyectoTuristico.objects.filter(pk=self.kwargs['idp']).exists()
        if proyecto is False:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        "validacion de que exista el detalle de venta"
        det = detalleVenta.objects.filter(pk=self.kwargs['id']).exists()
        if det is False:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el detalle de la venta existe')
            return HttpResponseRedirect(reverse_lazy('gestionarLotes', kwargs={'idp': self.kwargs['idp']}))
        return super().dispatch(request, *args, **kwargs)
    
    """Metodo para obtener la url de exito del formulario con los parametros necesarios"""
    def get_url_redirect(self, **kwargs):
        idp = self.kwargs.get('idp', None) #id del proyecto turistico 
        id = self.kwargs.get('id', None) #id del detalle de venta
        try:
            detalleVenta.objects.get(pk = id)
            return reverse_lazy('detalleLote', kwargs={'idp': idp, 'pk': id})
        except Exception:
            return reverse_lazy('gestionarLotes', kwargs={'idp': idp})

    """Se obtienen los parametros necesarios y se envian por contexto"""
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('id', None)
        idp = self.kwargs.get('idp', None) 
        context['idp'] = idp  #id del proyecto turistico
        context['id'] = id #id del detalle de venta
        return context
    
    "Enviar parametros a formulario"
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['idp'] = self.kwargs.get('idp', None) #Se envia id del proyecto turistico al form para validacion en el formulario
        return kwargs

    def form_valid(self, form, **kwargs):
        """Se obtienen los parametros de la url y el formulario recibido"""
        id = self.kwargs.get('id', None)
        idp = self.kwargs.get('idp', None)
        propietario = form.save(commit=False)
        try:
            detalle = detalleVenta.objects.get(pk = id)
            proyecto = proyectoTuristico.objects.get(pk = idp)
            propietario.save()
            asigPro = asignacionProyecto(propietario = propietario, dui= propietario.dui ,proyectoTuristico= proyecto)
            asigPro.save()
            """Se crea el objeto de asignación lote después de haber guardado el propietario"""
            detalle.propietarios.add(propietario,through_defaults={'eliminado': False})
            messages.success(self.request, 'Propietario guardado con exito')
        except Exception:
            propietario.delete()
            messages.error(self.request, 'Ocurrió un error al guardar el propietario, los datos ingresados son invalidos')
        return HttpResponseRedirect(self.get_url_redirect())

"""Vista del formulario para seleccionar propietarios ya registrados y asignarlos a un lote"""
class seleccionarPropietario(GroupRequiredMixin,FormView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'inventario/Propietario/seleccionarPropietario.html'
    form_class = detalleVentaPropietarioForm
    model = detalleVenta

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Validacion de que el proyecto turistico de la url exista"
        proyecto = proyectoTuristico.objects.filter(pk=self.kwargs['idp']).exists()
        if proyecto is False:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        "validacion de que exista el detalle de venta"
        det = detalleVenta.objects.filter(pk=self.kwargs['id']).exists()
        if det is False:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el detalle de la venta existe')
            return HttpResponseRedirect(reverse_lazy('gestionarLotes', kwargs={'idp': self.kwargs['idp']}))
        return super().dispatch(request, *args, **kwargs)

    """Metodo para obtener la url de exito del formulario con los parametros necesarios"""
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('id', None)#id del detalle de la venta
        idp = self.kwargs.get('idp', None)#id del proyecto turistico
        try:
            detalleVenta.objects.get(pk = id)
            return reverse_lazy('detalleLote', kwargs={'idp': idp, 'pk': id})
        except Exception:
            return reverse_lazy('gestionarLotes', kwargs={'idp': idp})
        
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('id', None)
        idp = self.kwargs.get('idp', None) 
        context['idp'] = idp #id del proyecto turistico
        context['id'] = id  #id del detalle de la venta
        return context
    
    "Enviar parametros a formulario"
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['idp'] = self.kwargs.get('idp', None) #id del proyecto turistico para validacion en form
        return kwargs

    def form_valid(self, form, **kwargs):
        """Se recoge el id del detalle venta y el formulario enviado"""
        id = self.kwargs.get('id', None) 
        asigprof = form.cleaned_data.get("propietarios")
        try:
            detalle = detalleVenta.objects.get(pk = id)
            """Se crean las tablas asigacion de propietarios segun los propietarios seleccionados"""
            for asig in asigprof:
                detalle.propietarios.add(asig.propietario,through_defaults={'eliminado': False})
            messages.success(self.request, 'Propietarios guardado con exito')
        except Exception:
            messages.error(self.request, 'Ocurrió un error al guardar el propietario, el detalle de venta no es valido')  
        return HttpResponseRedirect(self.get_url_redirect())


        
"""Vista del formulario modificar propietarios"""
class ModificarPropietario(GroupRequiredMixin, UpdateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema',u'Operador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp']) 
            try:
                propietarios = propietario.objects.get(id=self.kwargs['pk'])
            except Exception:
                messages.error(self.request, 'Ocurrió un error, el propietario no existe')
                return HttpResponseRedirect(reverse_lazy('consultarpropietarios', kwargs={'idp': self.kwargs['idp']}))
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    model = propietario
    template_name = 'inventario/Propietario/modificarPropietario.html'
    form_class = PropietarioForm
    
    def get_context_data(self, **kwargs):
        context = super(ModificarPropietario, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', None)    
        if 'form' not in context:
            context['form'] = self.form_class()
        context['pk'] = pk  
        return context

    def get_form(self, form_class = None, **kwargs):
        form = super().get_form(form_class)
        form.fields['dui'].disabled = True        
        return form

    def post(self, request, form_class = None, *args, **kwargs):
        self.object = self.get_object
        id_propietario = kwargs['pk']       
        propie= self.model.objects.get(id = id_propietario)
        form = self.form_class(request.POST, instance = propie)
        form.fields['dui'].disabled = True
        if form.is_valid():
            propietarioF = form.save(commit = False)
            propietarioF.save()
            messages.success(self.request, 'Propietario actualizado exitosamente')
        else: 
            messages.error(self.request, 'Ocurrió un error, el propietario no se actualizo')
        return HttpResponseRedirect(reverse_lazy('consultarPropietarios', kwargs={'idp': self.kwargs['idp']}))

#------------------------------------Views de proyecto---------------------------------------
"Vista de la lista de proyectos turisticos"
class proyectoTuristicoView(ListView):
    template_name = 'home.html'
    model = proyectoTuristico
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) 
        context['idp'] = idp #id del proyecto turistico
        return context


"Vista del formulario para agregar nuevo proyecto turistico"
class agregarProyectoTuristico(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    template_name = 'inventario/Proyecto/agregarProyecto.html'
    form_class = agregarProyectoForm
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    "Metodo para obtener la url de exito"
    def get_url_redirect(self, **kwargs):
        return reverse_lazy('home')

    def form_valid(self, form, **kwargs): 
        proyecto = form.save(commit=False)
        proyecto.save()
        messages.success(self.request, 'Proyecto guardado con exito')
        return HttpResponseRedirect(self.get_url_redirect())


"""Vista de formulario para modificar proyecto turistico"""
class ModificarProyectoTuristico(GroupRequiredMixin, UpdateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['pk'])  
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    model = proyectoTuristico
    template_name = 'inventario/Proyecto/agregarProyecto.html'
    form_class = agregarProyectoForm
    
    def get_context_data(self, **kwargs):
        context = super(ModificarProyectoTuristico, self).get_context_data(**kwargs)
        pk = self.kwargs.get('idp', None)  
        if 'form' not in context:
            context['form'] = self.form_class()
        context['idp'] = pk   
        return context

    def get_form(self, form_class = None, **kwargs):
        form = super().get_form(form_class)        
        return form

    def post(self, request, form_class = None, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, instance=self.object)
        
        if form.is_valid():
            proyectoM = form.save(commit=False)
            proyectoM.save()
            messages.success(self.request, 'EL proyecto fue actualizado exitosamente')
        else: 
            messages.error(self.request, 'Ocurrió un error, no se actualizo el proyecto')
        return HttpResponseRedirect(reverse_lazy('home'))


#-------------------------Views de condicion de pago----------------------------------------
"""Vista de formulario para agregar condiciones de pago"""
class agregarCondicionP(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    model = condicionesPago
    template_name = 'inventario/CondicionesDePago/agregarCondicionPago.html'
    form_class = condicionPagoForm
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        "Validaciones de que exista el proyecto turistico y la venta"
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
            venta = detalleVenta.objects.get(pk=self.kwargs['idv'], estado = True)
        except proyectoTuristico.DoesNotExist:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el proyecto existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        except detalleVenta.DoesNotExist:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el detalle de la venta existe y esté activo')
            return HttpResponseRedirect(reverse_lazy('detalleLote', kwargs={'idp': self.kwargs['idp'], 'pk': self.kwargs['idv']}))

        "Validacion de que no exista condiciones de pago existentes para esa venta"
        condicion = condicionesPago.objects.filter(detalleVenta__id=self.kwargs['idv'], estado=True).exists()
        if condicion is True:
            messages.error(self.request, 'Ocurrió un error, el lote ya tiene condiciones de pago registradas')
            return HttpResponseRedirect(reverse_lazy('detalleLote', kwargs={'idp': self.kwargs['idp'], 'pk': self.kwargs['idv']}))
        "Validaciones de que existan asignaciones y primas existentes"
        asignacion = asignacionLote.objects.filter(detalleVenta__id=self.kwargs['idv']).exists()
        if asignacion is False:
            messages.error(self.request, 'Ocurrió un error, el lote no tiene propietarios asociados')
            return HttpResponseRedirect(reverse_lazy('detalleLote', kwargs={'idp': self.kwargs['idp'], 'pk': self.kwargs['idv']}))
        prim = prima.objects.filter(detalleVenta__id=self.kwargs['idv']).exists()
        if prim is False:
            messages.error(self.request, 'Ocurrió un error, el lote debe tener registrada al menos una prima para poder registrar condiciones de pago')
            return HttpResponseRedirect(reverse_lazy('detalleLote', kwargs={'idp': self.kwargs['idp'], 'pk': self.kwargs['idv']}))    
        return super().dispatch(request, *args, **kwargs)

    "Url de exito del formulario"
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) #id del proyecto
        idv = self.kwargs.get('idv', None) #id del detalle de venta
        return reverse_lazy('detalleLote', kwargs={'idp': idp, 'pk': idv})

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idv = self.kwargs.get('idv', None)
        idp = self.kwargs.get('idp', None) 
        context['idp'] = idp  #id del proyecto
        context['idv'] = idv  #id del detalle de venta
        return context

    def get_form(self, form_class = None, **kwargs):
        form = super().get_form(form_class)
        """Se recoge parametros de la url y los pagos de primas para el calculo del monto de financiamiento
        monto del detalle de venta - sumatoria de todas las primas"""
        idv = self.kwargs.get('idv', None)
        detalle = detalleVenta.objects.get(pk=idv)
        pagosprimas = pago.objects.filter(prima__detalleVenta__id = idv)
        suma = 0
        for pag in pagosprimas:
          suma = suma + pag.monto
        montof = detalle.precioVenta - suma - detalle.descuento
        """Se asigna el monto como valor inicial y se deshabilitan los campos del monto y cuota ki"""
        form.fields['montoFinanciamiento'].initial = montof
        form.fields['montoFinanciamiento'].disabled = True 
        form.fields['cuotaKi'].disabled = True 
        return form

    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
        "Se recoge el parametro por url y el formulario"
        idv = self.kwargs.get('idv', None) 
        condicion = form.save(commit=False)  
        try:
            "se convierte la tasa y se calcula la cuotas"
            tasau = (condicion.tasaInteres / 100) /12
            condicion.cuotaKi = condicion.montoFinanciamiento*((tasau *decimal.Decimal((math.pow((1+tasau),condicion.plazo))))/decimal.Decimal((math.pow((1+tasau),condicion.plazo))-1));
            condicion.cuotaKi = round(condicion.cuotaKi, 2)
            detalle = detalleVenta.objects.get(id = idv)
            condicion.detalleVenta = detalle
            "Se crea las condiciones de pago y el estado de cuenta"
            condicion.save()
            estado = estadoCuenta(condicionesPago_id=condicion.id, nombre="Mantenimiento")
            estado.save()
            messages.success(self.request, 'Condicion de pago guardado con exito, estado de cuenta generado.')
        except Exception:
            messages.error(self.request, 'Ocurrió un error al guardar la condición de pago, la condición de pago no es valida')
        return HttpResponseRedirect(self.get_url_redirect())

#modificar condiciones de pago
class modificarCondicionesP(GroupRequiredMixin, UpdateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])  
            try:
                detallev= detalleVenta.objects.get(id = self.kwargs['idv'])
                if detallev.estado == False:
                    messages.error(self.request, 'Ocurrió un error, el detalle de venta no esta activo')
                    return HttpResponseRedirect(reverse_lazy('home'))
                try:
                    condicion = condicionesPago.objects.get(id=self.kwargs['pk'])
                    if condicion.detalleVenta != detallev:
                            messages.error(self.request, 'Ocurrió un error, la condiciòn de pago no pertenece a el detalle de venta')
                            return HttpResponseRedirect(reverse_lazy('detalleLote', kwargs={'idp': self.kwargs['idp'], 'pk': self.kwargs['idv']}))
                except Exception:
                    messages.error(self.request, 'Ocurrió un error, la condicion de pago no existe')
                    return HttpResponseRedirect(reverse_lazy('detalleLote', kwargs={'idp': self.kwargs['idp'], 'pk': self.kwargs['idv']}))
            except Exception:
                messages.error(self.request, 'Ocurrió un error, el detalle de venta no existe')
                return HttpResponseRedirect(reverse_lazy('home'))
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    model = condicionesPago
    template_name = 'inventario/CondicionesDePago/agregarCondicionPago.html'
    form_class = condicionPagoForm

    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) #id del proyecto
        idv = self.kwargs.get('idv', None) #id del detalle de venta
        return reverse_lazy('detalleLote', kwargs={'idp': idp, 'pk': idv})

    def get_context_data(self, **kwargs):
        context = super(modificarCondicionesP, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', None)
        context['pk'] = pk   
        return context

    def get_form(self, form_class = None, **kwargs):
        form = super().get_form(form_class)
        form.fields['montoFinanciamiento'].disabled = True 
        form.fields['cuotaKi'].disabled = True
        condicion = condicionesPago.objects.get(id=self.kwargs['pk'])
        estado = estadoCuenta.objects.get(condicionesPago=condicion)
        try:
            cuota = pagoMantenimiento.objects.filter(estadoCuenta_id = estado.id)
            for c in cuota:
                if estado.id == c.estadoCuenta_id:
                    form.fields['plazo'].disabled = True
                    form.fields['fechaEscrituracion'].disabled = True
            return form
        except Exception:
            form.fields['fechaEscrituracion'].disabled = False
            form.fields['plazo'].disabled = False
            return form

    def form_valid(self, form, *args, **kwargs):
        """If the form is valid, save the associated model."""
        idp = self.kwargs.get('idp', None) 
        idv = self.kwargs.get('idv', None) 
        if form.is_valid():
            condiciones=condicionesPago.objects.filter(detalleVenta__id = idv)
            for cond in condiciones:
                cond.estado = False
                cond.save()
            condicion = form.save(commit=False)
            ultimo_id = condicionesPago.objects.latest('id')
            condicion.id = (ultimo_id.id + 1)
            tasau = (condicion.tasaInteres / 100) /12
            condicion.cuotaKi = condicion.montoFinanciamiento*((tasau *decimal.Decimal((math.pow((1+tasau),condicion.plazo))))/decimal.Decimal((math.pow((1+tasau),condicion.plazo))-1));
            condicion.cuotaKi = round(condicion.cuotaKi, 2)
            condicion.save()
            estado = estadoCuenta(condicionesPago_id=condicion.id, nombre="Mantenimiento")
            estado.save()
            messages.success(self.request, 'Las condiciones de pago fueron actualizada exitosamente')
        else: 
            messages.error(self.request, 'Ocurrió un error, no se actualizo las condiciones de pago')
        return HttpResponseRedirect(self.get_url_redirect()) 
 
    
#eliminar condiciones de pago
class eliminarCondicionesP(GroupRequiredMixin, DeleteView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    model = condicionesPago
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_url_redirect(self, **kwargs):
        idp = self.kwargs.get('idp', None) 
        id = self.kwargs.get('idv', None) 
        try:
            detalleVenta.objects.get(pk = id)
            return reverse_lazy('detalleLote', kwargs={'idp': idp, 'pk': id})
        except Exception:
            return reverse_lazy('gestionarLotes', kwargs={'idp': idp})

    def post(self,request,*args,**kwargs):
        condicion = self.get_object()
        print(condicion.id)
        estados = estadoCuenta.objects.filter(condicionesPago = condicion)
        pagosM = pagoCuotaMantenimiento.objects.filter(condicionesPago = condicion)
        for pago in pagosM:
            pago.delete()
        for estado in estados:
            estado.delete()
        condicion.delete()
        return HttpResponseRedirect(self.get_url_redirect())



        

    


    