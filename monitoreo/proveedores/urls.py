from django.urls import path
from . import views

app_name = 'proveedores'  # <--- MUY IMPORTANTE por el namespace

urlpatterns = [
    path('', views.listar_proveedores, name='listar_proveedores'),
    path('nuevo/', views.crear_proveedor, name='crear_proveedor'),
    path('editar/<int:pk>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
]
