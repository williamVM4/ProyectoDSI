from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import asignacionLote, detalleVenta, propietario
from apps.autenticacion.mixins import *
from .forms import *

# Views de lote



# Views de asignar propietario
class asignarPropietario(GroupRequiredMixin,TemplateView):
    group_required = [u'Configurador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
         #obtengo el contexto actual
        context=super().get_context_data(**kwargs)
         # recojo el parametro 
        id = self.kwargs.get('id', None) 
         #agrego parametro al diccionario de contexto
        context['id'] = id         
        return context
    template_name = 'inventario/asignarPropietario.html'

class agregarPropietario(GroupRequiredMixin,CreateView):
    group_required = [u'Configurador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    template_name = 'inventario/agregarPropietario.html'
    form_class = PropietarioForm
    success_url = reverse_lazy('home')

    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
         # recojo el parametro 
        id = self.kwargs.get('id', None) 
        propietario = form.save(commit=False)
        #poner try
        detalle = detalleVenta.objects.get(pk = id)
        propietario.save()
        detalle.propietarios.add(propietario,through_defaults={'eliminado': False})
        #asignacion = asignacionLote(propietario = propietario, detalleVenta = detalle)
        #asignacion.save()
        return HttpResponseRedirect(self.success_url)

class seleccionarPropietario(GroupRequiredMixin,UpdateView):
    group_required = [u'Configurador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #para pasar el parametro por contexto
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        id = self.kwargs.get('pk', None) 
        context['id'] = id         
        return context

    template_name = 'inventario/seleccionarPropietario.html'
    form_class = detalleVentaPropietarioForm
    success_url = reverse_lazy('home')
    model = detalleVenta