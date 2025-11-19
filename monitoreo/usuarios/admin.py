from django.contrib import admin
from .models import Usuario, Rol, Direccion

# --- Admin para Usuario ---
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'Roles', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'Roles')
    search_fields = ('email', 'first_name', 'last_name', 'run')
    
    # --- ¡ESTA ES LA LÍNEA QUE AÑADIMOS! ---
    # Esto habilita la interfaz de "dos cajas" con flechas
    filter_horizontal = ('groups', 'user_permissions')
    
    ordering = ('email',)
    list_select_related = ('Roles', 'Direccion')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'materno', 'run', 'fono', 'Direccion')}),
        # Modificamos este fieldset para que 'groups' y 'user_permissions' se muestren correctamente
        ('Permisos y Rol', {'fields': ('Roles', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    def has_module_permission(self, request): return request.user.is_superuser

# --- Admin para Direccion ---
@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('calle', 'numero', 'comuna', 'region')
    search_fields = ('calle', 'comuna', 'region')
    list_filter = ('region', 'comuna')
    ordering = ('region', 'comuna')
    def has_module_permission(self, request): return request.user.is_superuser

# --- Admin adicionales ---
admin.site.register(Rol)
