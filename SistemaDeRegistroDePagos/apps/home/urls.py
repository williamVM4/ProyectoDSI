from django.urls import path
from apps.home.views import *

urlpatterns = [
    path('proyecto/<str:idp>/',homeProyecto.as_view(),name='home'),
]