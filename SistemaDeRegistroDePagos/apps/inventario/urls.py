from django.urls import path
from django.urls import re_path
from apps.inventario.views import *

urlpatterns = [
    path('asignarpropietario/',asignarPropietario.as_view(),name='asignarPropietario'),
    path('agregarpropietario/',agregarPropietario.as_view(),name='agregarPropietario'),
    path('seleccionarpropietario/<str:id>/',seleccionarPropietario.as_view(),name='seleccionarPropietario'),
]