from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    # Ruta para la lista de proveedores (CRUD - Read)
    path('', views.proveedor_list, name='proveedor_list'),
    
    # (Aquí añadiremos 'proveedor_create', 'proveedor_update', etc. más adelante)
]