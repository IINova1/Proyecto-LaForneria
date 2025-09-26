"""
URL configuration for monitoreo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

# Importamos todas las vistas de la aplicación 'dispositivos'
from dispositivos.views import (
    dashboard, inicio, register, device_list, device_detail, measurement_list, 
    alert_summary, api_dispositivos, device_add, device_edit, device_delete
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='dispositivos/login.html'), name='login'),
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='dispositivos/logout.html'), name='logout'), 
    
    # Flujo de Restablecimiento de Contraseña
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='dispositivos/password_reset.html'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='dispositivos/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='dispositivos/password_reset_confirm.html'
        ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='dispositivos/password_reset_complete.html'
        ), name='password_reset_complete'),


    path('', inicio, name='inicio'),
    path('panel/', dashboard, name='dashboard'),
    
    path('devices/', device_list, name='device_list'),
    path('devices/add/', device_add, name='device_add'),  # Agregar (Create)
    path('devices/<int:device_id>/', device_detail, name='device_detail'), # Detalle (Read)
    path('devices/<int:device_id>/edit/', device_edit, name='device_edit'), # Editar (Update)
    path('devices/<int:device_id>/delete/', device_delete, name='device_delete'), # Eliminar (Delete)
    
    path('measurements/', measurement_list, name='measurement_list'),
    path('alerts/summary/', alert_summary, name='alert_summary'),
    path('api/dispositivos/', api_dispositivos, name='api_dispositivos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)