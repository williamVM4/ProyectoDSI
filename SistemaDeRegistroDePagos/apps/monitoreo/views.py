from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.inventario.models import asignacionLote, detalleVenta, proyectoTuristico
from apps.monitoreo.models import estadoCuenta, cuotaEstadoCuenta
from apps.facturacion.models import pago, pagoMantenimiento
from apps.autenticacion.mixins import *
from django.contrib import messages
from .forms import *

class estadoCuentaView(GroupRequiredMixin,ListView):
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
        try:
            estado = estadoCuenta.objects.get(detalleVenta=self.kwargs['pk'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error el lote no tiene estado de cuenta generado. Verifique que ingreso las condiciones de pago')
            return HttpResponseRedirect(reverse_lazy('detalleLote', kwargs={'idp': self.kwargs['idp'], 'pk': self.kwargs['pk']}))    
        return super().dispatch(request, *args, **kwargs)
    template_name = 'monitoreo/estadoCuenta.html'
    model = detalleVenta

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        id = self.kwargs.get('pk', None)
        estado = estadoCuenta.objects.get(detalleVenta=id)
        cuotas = cuotaEstadoCuenta.objects.filter(estadoCuenta=estado)
        pagosm = pago.objects.filter(pagoMantenimiento__numeroCuotaEstadoCuenta__estadoCuenta=estado)
        context['idp'] = idp
        context['id'] = id  
        context['pagosm'] = pagosm
        return context
