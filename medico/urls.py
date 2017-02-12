"""medico URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from medico.views import *


urlpatterns = [
    url(
        r'^perfil-medico/(?P<id>\w+)$',
        PerfilMedico.as_view(),
        name='perfil_medico'
    ),
    url(
        r'^ver_consultas/(?P<id>\w+)$',
        VerConsultas.as_view(),
        name='ver_consultas'
    ),
    url(
        r'^historias_clinicas$',
        HistoriasClinicas.as_view(),
        name='historias_clinicas'
    ),
    url(
        r'^buscar-paciente$',
        BuscarPaciente.as_view(),
        name='buscar_paciente'
    ),
    url(
        r'^buscar-medico$',
        BuscarMedico.as_view(),
        name='buscar_medico'
    ),
    url(
        r'^ver-citas/(?P<id>\w+)$',
        VerCitas.as_view(),
        name='ver_citas'
    ),
    url(
        r'^mis-pacientes/(?P<id>\w+)$',
        MisPacientes.as_view(),
        name='mis_pacientes'
    ),
]