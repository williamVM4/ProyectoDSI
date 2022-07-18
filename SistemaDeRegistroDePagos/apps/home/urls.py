from django.urls import path
from apps.home.views import *

urlpatterns = [
    path('proyecto/<str:idp>/',detalleProyecto.as_view(),name='detalleProyecto'),
]