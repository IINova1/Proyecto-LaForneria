from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

app_name = 'dispositivos'

urlpatterns = [
    # Dashboard e inicio
    path('', views.inicio, name='inicio'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # --- CRUDs para todos los modelos ---
    # Usuario
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/crear/', views.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.usuario_update, name='usuario_update'),
    path('usuarios/<int:pk>/eliminar/', views.usuario_delete, name='usuario_delete'),

    # --- URLs para el Carrito de Compras ---
    path('tienda/', views.ver_productos, name='ver_productos'),
    path('carrito/agregar/<int:pk>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('pedido/realizar/', views.realizar_pedido, name='realizar_pedido'),
    path('pedido/exitoso/', views.pedido_exitoso, name='pedido_exitoso'),
    path('pedidos/', views.pedido_list, name='pedido_list'),
    path('pedidos/<int:pk>/', views.pedido_detail, name='pedido_detail'), # <-- AÑADIR ESTA LÍNEA


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

    # --- URLs de Autenticación ---
    path('login/', auth_views.LoginView.as_view(template_name='dispositivos/login.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='dispositivos:login'), name='logout'),
    path('register/', views.register, name='register'),

    # --- URLs para Restablecimiento de Contraseña (Versión Definitiva) ---
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='dispositivos/password_reset.html',
            # Le indicamos a Django que use nuestras plantillas de correo personalizadas
            email_template_name='dispositivos/password_reset_email.html',
            subject_template_name='dispositivos/password_reset_subject.txt',
            # Definimos la URL de éxito para asegurar la redirección correcta
            success_url=reverse_lazy('dispositivos:password_reset_done')
        ),
        name='password_reset'
    ),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='dispositivos/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='dispositivos/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='dispositivos/password_reset_complete.html'), name='password_reset_complete'),
]