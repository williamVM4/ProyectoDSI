from django.urls import path

from apps.facturacion.views import *

urlpatterns = [
    path('caja/<str:idp>/',caja.as_view(),name='caja'),
    path('agregarprima/<str:idp>/',agregarPrima.as_view(),name='agregarprima'),

]