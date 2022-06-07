from django.urls import path

from apps.facturacion.views import *

urlpatterns = [
    path('caja/',caja.as_view(),name='caja'),
    path('agregarPrima/',agregarPrima.as_view(),name='agregarPrima'),
    path('agregarPagoMantenimiento/',agregarPagoMantenimiento.as_view(),name='agregarPagoMantenimineto'),
]