from unicodedata import name
from django.urls import path
from apps.autenticacion.views import *

urlpatterns = [
    path('login/', loginForm.as_view(), name='login'),
    path('home/',home,name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout' )
]