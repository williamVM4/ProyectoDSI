from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.inventario.models import asignacionLote, detalleVenta
from apps.monitoreo.models import estadoCuenta, cuotaEstadoCuenta
from apps.facturacion.models import pago, pagoMantenimiento
from apps.autenticacion.mixins import *
from django.contrib import messages
from .forms import *

class estadoCuentaView(GroupRequiredMixin,ListView):
    group_required = [u'Configurador del sistema',u'Administrador del sistema']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
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
