from django.urls import path
from .views import *

urlpatterns = [
    path('estadocuentaM/<str:idp>/<str:idv>/<str:pk>/',estadoCuentaViewM.as_view(),name='estadoCuentaM'),
    path('estadocuentaF/<str:idp>/<str:idv>/<str:pk>/',estadoCuentaViewF.as_view(),name='estadoCuentaF'),
    path('estadocuentareporte/',EstadoCuentaReporte.as_view(),name='estadoCuentaReporte'),
    path('data/', ItemListView.as_view()),
]