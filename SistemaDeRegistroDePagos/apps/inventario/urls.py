from django.urls import path
from django.urls import re_path
from apps.inventario.views import *

urlpatterns = [
    path('detallelote/<str:pk>/',detalleLote.as_view(),name='detalleLote'),
    path('asignacioneslote/<str:pk>/',asignacionesLote.as_view(),name='asignacionesLote'),
    path('agregarpropietario/<str:id>/',agregarPropietario.as_view(),name='agregarPropietario'),
    path('seleccionarpropietario/<str:id>/',seleccionarPropietario.as_view(),name='seleccionarPropietario'),
    path('gestionarlotes/',gestionarLotes.as_view(),name='gestionarLotes'),
]