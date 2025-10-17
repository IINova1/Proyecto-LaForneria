"""
URL configuration for monitoreo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # --- LÍNEA CORREGIDA ---
    # Se añade un namespace 'dispositivos' para evitar conflictos al
    # buscar las rutas de la aplicación.
    path('', include(('dispositivos.urls', 'dispositivos'), namespace='dispositivos')),
]

# Configuración para servir archivos multimedia (imágenes) en modo de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)