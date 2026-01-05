from django.urls import path
from . import views

urlpatterns = [
    path('subir/', views.subir_documento, name='subir_documento'),
    path('lista/', views.lista_pacientes, name='lista_pacientes'),
]