from django.urls import path

from apps.facturacion.views import *

urlpatterns = [
    path('agregarPrima/',agregarPrima.as_view(),name='agregarPrima'),
]