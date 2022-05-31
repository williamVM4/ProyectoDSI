from django.urls import path
from apps.inventario.views import *

urlpatterns = [
    path('asignarpropietario/',asignarPropietario.as_view(),name='asignarPropietario'),
]