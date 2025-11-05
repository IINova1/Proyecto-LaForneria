from django.contrib import admin
from .models import Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre_empresa', 'email', 'telefono', 'rubro')
    search_fields = ('rut', 'nombre_empresa', 'email', 'rubro')
    list_filter = ('rubro',)
    
    # Solo los superusuarios pueden ver esto en el admin
    def has_module_permission(self, request):
        return request.user.is_superuser