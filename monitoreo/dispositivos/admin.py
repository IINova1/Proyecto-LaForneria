from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Importamos los modelos de nuestra aplicación
from .models import Usuario, Categoria, Producto, Cliente, Venta, DetalleVenta, Rol, Direccion, Nutricional

# --- CÓDIGO CORREGIDO ---
# Adaptamos la vista de administrador para el modelo 'Usuario' con los campos corregidos.
class UsuarioAdmin(UserAdmin):
    model = Usuario
    # Usamos los nombres de campo correctos ('email', 'first_name', 'last_name')
    list_display = ('email', 'first_name', 'last_name', 'Roles', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'Roles')
    search_fields = ('email', 'first_name', 'last_name', 'run')
    ordering = ('email',)
    
    # Organizamos los campos para la vista de edición del usuario
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'materno', 'run', 'fono', 'Direccion')}),
        ('Permisos y Rol', {'fields': ('Roles', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos que aparecerán al crear un nuevo usuario desde el admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 'run', 'Roles', 'Direccion')}
        ),
    )

# Registramos todos los modelos para que aparezcan en el panel de administración
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Rol)
admin.site.register(Direccion)
admin.site.register(Nutricional)