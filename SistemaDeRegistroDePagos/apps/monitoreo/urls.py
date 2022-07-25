from django.urls import path
from .views import *

urlpatterns = [
    path('estadocuenta/<str:idp>/<str:idv>/<str:pk>/',estadoCuentaView.as_view(),name='estadoCuenta'),
    path('estadocuentareporte/',EstadoCuentaReporte.as_view(),name='estadoCuentaReporte'),
]