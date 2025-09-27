from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Productos
    path('productos/', views.producto_list, name='producto_list'),

    # Categorías
    path('categorias/', views.categoria_list, name='categoria_list'),

    # Usuarios
    path('usuarios/', views.usuario_list, name='usuario_list'),

    # Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),

    # Ventas
    path('ventas/', views.venta_list, name='venta_list'),

    # Alertas
    path('alertas/', views.alert_summary, name='alert_summary'),
]
