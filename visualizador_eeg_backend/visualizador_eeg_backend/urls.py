"""
URL configuration for visualizador_eeg_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

# Crear un enrutador para gestionar las rutas automáticamente
router = DefaultRouter()
router.register(r'pacientes', views.PacienteViewSet)
router.register(r'sesiones', views.SesionViewSet)
router.register(r'canales', views.CanalViewSet)
router.register(r'frecuencias', views.FrecuenciaViewSet)
router.register(r'enfermedades', views.EnfermedadViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Incluir las rutas del enrutador
    path('api/subir-edf/', views.subir_edf, name='subir_edf'),
    path('api/obtener-frecuencias/<int:sesion_id>/', views.obtener_frecuencias, name='obtener_frecuencias'),
    path('api/obtener-sesiones', views.obtener_sesiones, name='obtener_sesiones'),
    path('api/obtener-sesion_id', views.obtener_sesion_id, name='obtener_sesion_id'),
]


