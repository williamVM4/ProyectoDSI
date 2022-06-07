from django.urls import path

from apps.facturacion.views import *

urlpatterns = [
    path('agregarPrima/<str:id>/',agregarPrima.as_view(),name='agregarPrima'),
]