from django.urls import path
from .views import *

urlpatterns = [
    path('estadocuenta/<str:idp>/<str:pk>/',estadoCuentaView.as_view(),name='estadoCuenta'),
]