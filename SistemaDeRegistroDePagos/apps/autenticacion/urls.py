from unicodedata import name
from django.urls import path
from apps.autenticacion.views import *

urlpatterns = [
    path('login/', loginForm.as_view(), name='login'),
    path('home/',home.as_view(),name='home'),
    path('otro/',otro.as_view(),name='otro'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout' )
]