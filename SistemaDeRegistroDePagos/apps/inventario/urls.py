from django.urls import path
from django.urls import re_path
from apps.inventario.views import *

urlpatterns = [
    path('asignarpropietario/<str:id>/',asignarPropietario.as_view(),name='asignarPropietario'),
    path('agregarpropietario/<str:id>/',agregarPropietario.as_view(),name='agregarPropietario'),
    path('seleccionarpropietario/<str:pk>/',seleccionarPropietario.as_view(),name='seleccionarPropietario'),
    path('gestionarlotes/',gestionarLotes.as_view(),name='gestionarLotes'),
]