from django.urls import path

from apps.facturacion.views import *

urlpatterns = [
    path('caja/',caja.as_view(),name='caja'),
    path('agregarPagoMantenimiento/',agregarPagoMantenimiento.as_view(),name='agregarPagoMantenimineto'),
    path('agregarPrima/<str:id>/',agregarPrima.as_view(),name='agregarPrima'),
]