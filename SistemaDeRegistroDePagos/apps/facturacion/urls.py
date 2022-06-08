from django.urls import path

from apps.facturacion.views import *

urlpatterns = [
    path('caja/<str:idp>/',caja.as_view(),name='caja'),
    path('agregarPagoMantenimiento/<str:idp>/',agregarPagoMantenimiento.as_view(),name='agregarPagoMantenimineto'),
    path('agregarPrima/<str:idp>/',agregarPrima.as_view(),name='agregarPrima'),
]