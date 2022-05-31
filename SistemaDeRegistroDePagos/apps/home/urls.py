from django.urls import path
from apps.home.views import *

urlpatterns = [
    path('',home.as_view(),name='home'),
]