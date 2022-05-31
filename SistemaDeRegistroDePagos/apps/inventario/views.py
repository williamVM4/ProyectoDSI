from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.autenticacion.mixins import *

# View de asignar propietario
class asignarPropietario(ValidatePermissionRequiredMixin,TemplateView):
    permission_required = 'autenticacion.view_group'
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    template_name = 'inventario/asignarPropietario.html'