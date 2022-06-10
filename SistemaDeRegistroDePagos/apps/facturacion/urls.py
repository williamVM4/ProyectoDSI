from django.urls import path

from apps.facturacion.views import *

urlpatterns = [
    path('caja/<str:idp>/',caja.as_view(),name='caja'),
    path('agregarprima/<str:idp>/',agregarPrima.as_view(),name='agregarprima'),
    path('pagomantenimiento/<str:idp>/',agregarPagoMantenimiento.as_view(),name='agregarPagoMantenimiento'),

    
]