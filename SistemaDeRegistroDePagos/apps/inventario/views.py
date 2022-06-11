from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.monitoreo.models import estadoCuenta
from apps.inventario.models import asignacionLote, detalleVenta, lote, proyectoTuristico
from apps.autenticacion.mixins import *
from django.contrib import messages
from .forms import *

# Views de lote
class gestionarLotes(GroupRequiredMixin,ListView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)
    template_name = 'inventario/gestionarLotes.html'
    model = lote

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('idp', None) 
        context['idp'] = id
        context['lotes'] = lote.objects.filter(proyectoTuristico__id=id)
        return context
    
class detalleLote(GroupRequiredMixin,DetailView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el proyecto existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        try:
            lot = detalleVenta.objects.get(pk=self.kwargs['pk'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el detalle de la venta existe')
            return HttpResponseRedirect(reverse_lazy('gestionarLotes', kwargs={'idp': self.kwargs['idp']}))
        return super().dispatch(request, *args, **kwargs)
    template_name = 'inventario/detalleLote.html'
    model = detalleVenta

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        id = self.kwargs.get('pk', None) 
        context['idp'] = idp   
        context['id'] = id      
        return context

class asignacionesLote(GroupRequiredMixin,ListView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el proyecto existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        try:
            lot = lote.objects.get(pk=self.kwargs['pk'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el lote existe')
            return HttpResponseRedirect(reverse_lazy('gestionarLotes', kwargs={'idp': self.kwargs['idp']}))
        return super().dispatch(request, *args, **kwargs)
    template_name = 'inventario/asignacionLote.html'
    model = detalleVenta

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        id = self.kwargs.get('pk', None)
        context['idp'] = idp
        context['id'] = id
        context['detalles'] = detalleVenta.objects.filter(lote__matriculaLote=id)
        context['asignaciones'] = asignacionLote.objects.filter()   
        return context

# Views de lote
class agregarLote(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, el proyecto no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)
    template_name = 'inventario/agregarLote.html'
    form_class = LoteForm
    #success_url = reverse_lazy('asignacionLote')
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) 
        return reverse_lazy('gestionarLotes', kwargs={'idp': idp})
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        context['idp'] = idp         
        return context
    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
         # recojo el parametro 
        idp = self.kwargs.get('idp', None) 
        lote = form.save(commit=False)
        #poner try
        try:
            lote.proyectoTuristico = proyectoTuristico.objects.get(id=idp)
            lote.identificador = str(lote.poligono) + str(lote.numeroLote)
            lote.save()
            messages.success(self.request, 'Lote guardado con éxito')
        except Exception:
            lote.delete()
            messages.error(self.request, 'Ocurrió un error al guardar el lote, el lote no es válido')
        return HttpResponseRedirect(self.get_url_redirect())

# Views de detalle de venta
class agregarDetalleVenta(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el proyecto existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        try:
            lot = lote.objects.get(pk=self.kwargs['idl'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el lote existe')
            return HttpResponseRedirect(reverse_lazy('gestionarLotes', kwargs={'idp': self.kwargs['idp']}))
        return super().dispatch(request, *args, **kwargs)
    template_name = 'inventario/agregarDetalleVenta.html'
    form_class = DetalleVentaForm
    #success_url = reverse_lazy('asignacionLote')
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        idl = self.kwargs.get('idl', None)  
        return reverse_lazy('asignacionesLote', kwargs={'idp': idp,'pk': idl})

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        idl = self.kwargs.get('idl', None)
        context['idp'] = idp
        context['idl'] = idl           
        return context
    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
         # recojo el parametro 
        idl = self.kwargs.get('idl', None) 
        detalle = form.save(commit=False)
        #poner try
        try:
            detalle.lote = lote.objects.get(pk=idl)
            detalle.save()
            messages.success(self.request, 'Detalle de venta guardado con éxito')
        except Exception:
            detalle.delete()
            messages.error(self.request, 'Ocurrió un error al guardar el detalle de venta, el detalle de venta no es válido')
        return HttpResponseRedirect(self.get_url_redirect())

# Views de propietario
class agregarPropietario(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el proyecto existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        try:
            lot = detalleVenta.objects.get(pk=self.kwargs['id'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el detalle de la venta existe')
            return HttpResponseRedirect(reverse_lazy('gestionarLotes', kwargs={'idp': self.kwargs['idp']}))
        return super().dispatch(request, *args, **kwargs)
    
    template_name = 'inventario/agregarPropietario.html'
    form_class = PropietarioForm
    #success_url = reverse_lazy('detalleLote')
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) 
        id = self.kwargs.get('id', None) 
        try:
            detalleVenta.objects.get(pk = id)
            return reverse_lazy('detalleLote', kwargs={'idp': idp, 'pk': id})
        except Exception:
            return reverse_lazy('gestionarLotes', kwargs={'idp': idp})

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('id', None)
        idp = self.kwargs.get('idp', None) 
        context['idp'] = idp  
        context['id'] = id  
        return context

    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
         # recojo el parametro 
        id = self.kwargs.get('id', None) 
        propietario = form.save(commit=False)
        #poner try
        try:
            detalle = detalleVenta.objects.get(pk = id)
            propietario.save()
            detalle.propietarios.add(propietario,through_defaults={'eliminado': False})
            messages.success(self.request, 'Propietario guardado con exito')
        except Exception:
            propietario.delete()
            messages.error(self.request, 'Ocurrió un error al guardar el propietario, el detalle de venta no es valido')
        return HttpResponseRedirect(self.get_url_redirect())

class seleccionarPropietario(GroupRequiredMixin,FormView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el proyecto existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        try:
            lot = detalleVenta.objects.get(pk=self.kwargs['id'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el detalle de la venta existe')
            return HttpResponseRedirect(reverse_lazy('gestionarLotes', kwargs={'idp': self.kwargs['idp']}))
        return super().dispatch(request, *args, **kwargs)

    template_name = 'inventario/seleccionarPropietario.html'
    form_class = detalleVentaPropietarioForm
    #success_url = reverse_lazy('detalleLote')
    model = detalleVenta
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('id', None)
        idp = self.kwargs.get('idp', None)
        try:
            detalleVenta.objects.get(pk = id)
            return reverse_lazy('detalleLote', kwargs={'idp': idp, 'pk': id})
        except Exception:
            return reverse_lazy('gestionarLotes', kwargs={'idp': idp})
        
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('id', None)
        idp = self.kwargs.get('idp', None) 
        context['idp'] = idp  
        context['id'] = id         
        return context

    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
         # recojo el parametro 
        id = self.kwargs.get('id', None) 
        propietariosf = form.cleaned_data.get("propietarios")
        #poner try
        try:
            detalle = detalleVenta.objects.get(pk = id)
            for propietario in propietariosf:
                detalle.propietarios.add(propietario,through_defaults={'eliminado': False})
            messages.success(self.request, 'Propietarios guardado con exito')
        except Exception:
            messages.error(self.request, 'Ocurrió un error al guardar el propietario, el detalle de venta no es valido')  
        return HttpResponseRedirect(self.get_url_redirect())

# Views de proyecto

class proyectoTuristicoView(ListView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    template_name = 'home.html'
    model = proyectoTuristico

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) 
        context['idp'] = idp
        return context

class agregarProyectoTuristico(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    template_name = 'inventario/agregarProyecto.html'
    form_class = agregarProyectoForm
    #success_url = reverse_lazy('')
    def get_url_redirect(self, **kwargs):
        return reverse_lazy('home')


    def form_valid(self, form, **kwargs): 
        proyecto = form.save(commit=False)
        #poner try
        try:
            proyecto.save()
            messages.success(self.request, 'Proyecto guardado con exito')
        except Exception:
            messages.error(self.request, 'Ocurrió un error al guardar el proyecto')
        return HttpResponseRedirect(self.get_url_redirect())

# Views de condicion de pago
class agregarCondicionP(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            proyecto = proyectoTuristico.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el proyecto existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        try:
            venta = detalleVenta.objects.get(pk=self.kwargs['idv'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, asegurese de que el detalle de la venta existe')
            return HttpResponseRedirect(reverse_lazy('gestionarLotes', kwargs={'idp': self.kwargs['idp']}))
        return super().dispatch(request, *args, **kwargs)
    
    model = condicionesPago
    template_name = 'inventario/CondicionesDePago/agregarCondicionPago.html'
    form_class = condicionPagoForm

    #success_url = reverse_lazy('detalleLote')
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) 
        idv = self.kwargs.get('idv', None)         
        return reverse_lazy('detalleLote', kwargs={'idp': idp, 'pk': idv})

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idv = self.kwargs.get('idv', None)
        idp = self.kwargs.get('idp', None) 
        context['idp'] = idp  
        context['idv'] = idv  
        return context

    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
         # recojo el parametro 
        idv = self.kwargs.get('idv', None) 
        condicion = form.save(commit=False)
        
        #poner try
        try:
            detalle = detalleVenta.objects.get(pk = idv)
            condicion.detalleVenta = detalle
            condicion.save()

            #estado = estadoCuenta(detalleVenta=detalle)
            #estado.save()

            messages.success(self.request, 'Condicion de pago guardado con exito')
        except Exception:
            condicion.delete()
            messages.error(self.request, 'Ocurrió un error al guardar la condición de pago, la condición de pago no es valida')
        return HttpResponseRedirect(self.get_url_redirect())

