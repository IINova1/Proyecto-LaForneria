from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Categoria, Producto, Cliente, Venta, DetalleVenta

# Configuración personalizada para el usuario
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'rol')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'rol', 'password', 'password2', 'is_staff', 'is_active')}
        ),
    )

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'stock')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'categoria__nombre')

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombres', 'paterno', 'materno', 'email', 'telefono')
    search_fields = ('nombres', 'paterno', 'materno', 'email', 'telefono')

class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'usuario', 'estado_pedido', 'fecha')
    list_filter = ('estado_pedido', 'fecha')
    search_fields = ('cliente__nombres', 'usuario__email')
    inlines = [DetalleVentaInline]


# Registro de modelos en el admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Categoria)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Venta, VentaAdmin)
