from django.contrib import admin
from .models import (
    Usuario, Categoria, Producto, Cliente, Venta, DetalleVenta, 
    Rol, Direccion, Nutricional, ReglaAlertaVencimiento, ProductoReglaAlerta
)

# --- Admin para Modelos de Catálogo (Maestros) ---

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'precio', 'stock_actual', 'caducidad', 'Categorias')
    search_fields = ('nombre', 'marca')
    list_filter = ('Categorias',)
    ordering = ('caducidad',)
    list_select_related = ('Categorias', 'Nutricional') # Optimiza la carga de la categoría y nutricional

@admin.register(ReglaAlertaVencimiento)
class ReglaAlertaVencimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dias_anticipacion', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('dias_anticipacion',)
    ordering = ('dias_anticipacion',)

@admin.register(ProductoReglaAlerta)
class ProductoReglaAlertaAdmin(admin.ModelAdmin):
    list_display = ('get_producto_nombre', 'get_regla_nombre')
    list_filter = ('regla__nombre',) # Filtro por el nombre de la regla
    search_fields = ('producto__nombre', 'regla__nombre')
    list_select_related = ('producto', 'regla')

    @admin.display(description='Producto', ordering='producto__nombre')
    def get_producto_nombre(self, obj):
        return obj.producto.nombre

    @admin.display(description='Regla de Alerta', ordering='regla__nombre')
    def get_regla_nombre(self, obj):
        return obj.regla.nombre

# --- Admin para Modelos Operacionales (equivalente a Cliente/Área) ---

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # Asumiendo que el modelo Cliente tendrá más campos en el futuro.
    list_display = ('idclientes',)
    search_fields = ('idclientes',)

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('calle', 'numero', 'comuna', 'region')
    search_fields = ('calle', 'comuna', 'region')
    list_filter = ('region', 'comuna')
    ordering = ('region', 'comuna')

# --- Admin para Series de Tiempo (equivalente a Measurement) ---

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    # La tabla 'venta' no tiene un campo de fecha, así que no podemos usar date_hierarchy.
    # Si tuvieras un campo `fecha_venta = models.DateTimeField()`, la línea sería:
    # date_hierarchy = 'fecha_venta'
    list_display = ('idventa', 'Usuarios', 'EstadoPedido', 'clientes_idclientes')
    search_fields = ('Usuarios__email', 'EstadoPedido')
    list_filter = ('EstadoPedido',)
    ordering = ('-idventa',) # Orden descendente por ID
    list_select_related = ('Usuarios', 'clientes_idclientes')


# --- Registros del Modelo de Usuario y otros ---
# Se mantiene el admin personalizado para Usuario que ya tenías
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'Roles', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'Roles')
    search_fields = ('email', 'first_name', 'last_name', 'run')
    ordering = ('email',)
    list_select_related = ('Roles', 'Direccion')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'materno', 'run', 'fono', 'Direccion')}),
        ('Permisos y Rol', {'fields': ('Roles', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

# Registros adicionales para tener un admin completo
admin.site.register(Rol)
admin.site.register(Nutricional)
admin.site.register(DetalleVenta)