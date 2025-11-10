from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

# --- Importamos el formulario de login personalizado ---
from .forms import CustomLoginForm 

app_name = 'usuarios'

urlpatterns = [
    # --- CRUD de Usuarios (para el Admin) ---
    path('listado/', views.usuario_list, name='usuario_list'),
    path('crear/', views.usuario_create, name='usuario_create'),
    path('<int:pk>/editar/', views.usuario_update, name='usuario_update'),
    path('<int:pk>/eliminar/', views.usuario_delete, name='usuario_delete'),

    # --- Autenticación de Usuarios ---
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html',  # Nueva ruta de plantilla
        authentication_form=CustomLoginForm
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(
        next_page='core:inicio'  # Redirige al inicio público
    ), name='logout'),
    
    path('register/', views.register, name='register'),

    # --- ¡NUEVA RUTA DE PERFIL! ---
    path('perfil/', views.perfil, name='perfil'),

    # --- Restablecimiento de Contraseña ---
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='usuarios/password_reset.html',
            email_template_name='usuarios/password_reset_email.html',
            subject_template_name='usuarios/password_reset_subject.txt',
            success_url=reverse_lazy('usuarios:password_reset_done')
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='usuarios/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='usuarios/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='usuarios/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]