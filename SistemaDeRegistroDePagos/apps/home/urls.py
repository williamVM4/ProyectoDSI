from django.urls import path
from SistemaDeRegistroDePagos.apps.home.views import *

urlpatterns = [
    path('proyecto/<str:idp>/',homeProyecto.as_view(),name='homeProyecto'),
]