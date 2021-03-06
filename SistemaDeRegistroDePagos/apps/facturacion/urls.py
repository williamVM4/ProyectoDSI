from django.urls import path

from apps.facturacion.views import *

urlpatterns = [
    path('caja/<str:idp>/',caja.as_view(),name='caja'),
    path('agregarprima/<str:idp>/',agregarPrima.as_view(),name='agregarprima'),
    path('pagomantenimiento/<str:idp>/',agregarPagoMantenimiento.as_view(),name='agregarPagoMantenimiento'),
    path('pagofinanciamiento/<str:idp>/',agregarPagoFinanciamiento.as_view(),name='agregarPagoFinanciamiento'),
    path('detallepago/<str:idp>/<str:pk>/',detallePago.as_view(),name='detallePago'),
    path('gestionarcuentas/<str:idp>/',gestionarCuentasBancarias.as_view(),name='cuentas'),
    path('agregarcuenta/<str:idp>/',agregarCuentaBancaria.as_view(),name='agregarCuentaB'),
    path('recibo/<str:idp>/<str:pk>/',Recibo.as_view(),name='recibo'),
    path('eliminarPrima/<str:idp>/<str:idv>/<str:id>/',EliminarPrima.as_view(),name='eliminarPrima'),
    path('modificarPrima/<str:idp>/<str:idv>/<str:pk>/',ModificarPrima.as_view(), name='modificarPrima')
]