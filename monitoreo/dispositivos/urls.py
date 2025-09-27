from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'dispositivos'

urlpatterns = [
    # Dashboard e inicio
    path('', views.inicio, name='inicio'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Usuario
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/crear/', views.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.usuario_update, name='usuario_update'),
    path('usuarios/<int:pk>/eliminar/', views.usuario_delete, name='usuario_delete'),

    # Categoría
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/crear/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),

    # Producto
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/crear/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('productos/<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),

    # Cliente
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/crear/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', views.cliente_delete, name='cliente_delete'),

    # Venta
    path('ventas/', views.venta_list, name='venta_list'),
    path('ventas/crear/', views.venta_create, name='venta_create'),
    path('ventas/<int:pk>/editar/', views.venta_update, name='venta_update'),
    path('ventas/<int:pk>/eliminar/', views.venta_delete, name='venta_delete'),

    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='dispositivos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='dispositivos:login'), name='logout'),
    path('register/', views.register, name='register'),

    # Restablecimiento de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='dispositivos/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='dispositivos/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='dispositivos/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='dispositivos/password_reset_complete.html'), name='password_reset_complete'),
]