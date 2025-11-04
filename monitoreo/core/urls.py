from django.urls import path
from . import views

# --- CORREGIDO ---
# El app_name debe coincidir con el nombre de la app
app_name = 'core'

urlpatterns = [
    # Dashboard e inicio
    path('', views.inicio, name='inicio'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # --- Todas las demás rutas (usuarios, productos, pedidos, etc.) ---
    # --- SE ELIMINAN DE ESTE ARCHIVO ---
]