from django.urls import path
from django.urls import re_path
from apps.inventario.views import *
from apps.monitoreo.views import *

urlpatterns = [
    path('detallelote/<str:idp>/<str:pk>/',detalleLote.as_view(),name='detalleLote'),
    path('asignacioneslote/<str:idp>/<str:pk>/',asignacionesLote.as_view(),name='asignacionesLote'),
    path('agregarpropietario/<str:idp>/<str:id>/',agregarPropietario.as_view(),name='agregarPropietario'),
    path('seleccionarpropietario/<str:idp>/<str:id>/',seleccionarPropietario.as_view(),name='seleccionarPropietario'),
    path('gestionarlotes/<str:idp>/',gestionarLotes.as_view(),name='gestionarLotes'),
    path('consultarpropietarios/<str:idp>/',consultarPropietarios.as_view(),name='consultarPropietarios'),
    path('agregarlote/<str:idp>/',agregarLote.as_view(),name='agregarLote'),
    path('',proyectoTuristicoView.as_view(),name='home'),
    path('agregarproyecto/',agregarProyectoTuristico.as_view(),name='agregarproyecto'),
    path('historicoVentas/<str:idp>/',historicoVentas.as_view(),name='historicoVentas'),
    path('agregardetalleventa/<str:idp>/<str:idl>/',agregarDetalleVenta.as_view(),name='agregarDetalleVenta'),
    path('agregarcondicionpago/<str:idp>/<str:idv>/',agregarCondicionP.as_view(),name='agregarCondicionP'),
]