# proveedores/urls.py
from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    # --- CRUD de Proveedores ---
    path('', views.proveedor_list, name='listar_proveedores'),
    path('nuevo/', views.crear_proveedor, name='crear_proveedor'),
    path('<int:pk>/editar/', views.editar_proveedor, name='editar_proveedor'),
    path('<int:pk>/eliminar/', views.eliminar_proveedor, name='eliminar_proveedor'),

    # --- Exportación Excel ---
    path('exportar/', views.exportar_proveedores_excel, name='exportar_proveedores_excel'),
]
