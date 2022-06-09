from django.urls import path
from django.urls import re_path
from apps.inventario.views import *

urlpatterns = [
    path('detallelote/<str:idp>/<str:pk>/',detalleLote.as_view(),name='detalleLote'),
    path('asignacioneslote/<str:idp>/<str:pk>/',asignacionesLote.as_view(),name='asignacionesLote'),
    path('agregarpropietario/<str:idp>/<str:id>/',agregarPropietario.as_view(),name='agregarPropietario'),
    path('seleccionarpropietario/<str:idp>/<str:id>/',seleccionarPropietario.as_view(),name='seleccionarPropietario'),
    path('gestionarlotes/<str:idp>/',gestionarLotes.as_view(),name='gestionarLotes'),
    path('agregarlote/<str:idp>/',agregarLote.as_view(),name='agregarLote'),
    path('',proyectoTuristicoView.as_view(),name='home'),
    path('agregarproyecto/',agregarProyectoTuristico.as_view(),name='agregarproyecto'),
]