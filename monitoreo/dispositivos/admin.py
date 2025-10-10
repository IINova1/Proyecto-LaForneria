from django.contrib import admin
from .models import (
    Usuario, Categoria, Producto, Cliente, Venta, DetalleVenta, 
    Rol, Direccion, Nutricional, ReglaAlertaVencimiento, ProductoReglaAlerta,
    Pedido, DetallePedido
)

# --- Admin para Modelos de Catálogo (Maestros) ---

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)

    def has_module_permission(self, request):
        """Solo los superusuarios pueden ver este módulo."""
        return request.user.is_superuser

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """Este módulo es visible para todo el personal (staff)."""
    list_display = ('nombre', 'marca', 'precio', 'stock_actual', 'caducidad', 'Categorias')
    search_fields = ('nombre', 'marca')
    list_filter = ('Categorias',)
    ordering = ('caducidad',)
    list_select_related = ('Categorias', 'Nutricional')

@admin.register(ReglaAlertaVencimiento)
class ReglaAlertaVencimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dias_anticipacion', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('dias_anticipacion',)
    ordering = ('dias_anticipacion',)
    
    def has_module_permission(self, request):
        """Solo los superusuarios pueden ver este módulo."""
        return request.user.is_superuser

@admin.register(ProductoReglaAlerta)
class ProductoReglaAlertaAdmin(admin.ModelAdmin):
    list_display = ('get_producto_nombre', 'get_regla_nombre')
    list_filter = ('regla__nombre',)
    search_fields = ('producto__nombre', 'regla__nombre')
    list_select_related = ('producto', 'regla')

    @admin.display(description='Producto', ordering='producto__nombre')
    def get_producto_nombre(self, obj):
        return obj.producto.nombre

    @admin.display(description='Regla de Alerta', ordering='regla__nombre')
    def get_regla_nombre(self, obj):
        return obj.regla.nombre

    def has_module_permission(self, request):
        """Solo los superusuarios pueden ver este módulo."""
        return request.user.is_superuser

# --- Admin para Modelos Operacionales ---

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('idclientes',)
    search_fields = ('idclientes',)

    def has_module_permission(self, request):
        """Solo los superusuarios pueden ver este módulo."""
        return request.user.is_superuser

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('calle', 'numero', 'comuna', 'region')
    search_fields = ('calle', 'comuna', 'region')
    list_filter = ('region', 'comuna')
    ordering = ('region', 'comuna')

    def has_module_permission(self, request):
        """Solo los superusuarios pueden ver este módulo."""
        return request.user.is_superuser

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('idventa', 'Usuarios', 'EstadoPedido', 'clientes_idclientes')
    search_fields = ('Usuarios__email', 'EstadoPedido')
    list_filter = ('EstadoPedido',)
    ordering = ('-idventa',)
    list_select_related = ('Usuarios', 'clientes_idclientes')

    def has_module_permission(self, request):
        """Solo los superusuarios pueden ver este módulo."""
        return request.user.is_superuser

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'Roles', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'Roles')
    search_fields = ('email', 'first_name', 'last_name', 'run')
    ordering = ('email',)
    list_select_related = ('Roles', 'Direccion')
    
    # --- BLOQUE CORREGIDO Y FINAL ---
    # Se añaden 'groups' y 'user_permissions' para que la caja de permisos sea visible.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'materno', 'run', 'fono', 'Direccion')}),
        ('Permisos y Rol', {'fields': ('Roles', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    def has_module_permission(self, request):
        """Solo los superusuarios pueden ver este módulo."""
        return request.user.is_superuser

# --- Inline para DetallePedido ---
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_pedido', 'total', 'estado')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('id', 'usuario__email')
    ordering = ('-fecha_pedido',)
    list_editable = ('estado',)
    inlines = [DetallePedidoInline]

    def has_module_permission(self, request):
        """Solo los superusuarios pueden ver este módulo."""
        return request.user.is_superuser

# --- Registros Adicionales ---
# Django registrará estos modelos, pero gracias a has_module_permission,
# solo serán visibles para el superusuario.
admin.site.register(Rol)
admin.site.register(Nutricional)
admin.site.register(DetalleVenta)