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

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
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

# --- Admin para Modelos Operacionales ---

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('idclientes',)
    search_fields = ('idclientes',)

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('calle', 'numero', 'comuna', 'region')
    search_fields = ('calle', 'comuna', 'region')
    list_filter = ('region', 'comuna')
    ordering = ('region', 'comuna')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('idventa', 'Usuarios', 'EstadoPedido', 'clientes_idclientes')
    search_fields = ('Usuarios__email', 'EstadoPedido')
    list_filter = ('EstadoPedido',)
    ordering = ('-idventa',)
    list_select_related = ('Usuarios', 'clientes_idclientes')

    # --- CAMBIO CLAVE ---
    # Este método filtra las ventas que se muestran en el admin.
    def get_queryset(self, request):
        # Obtiene el queryset original (todas las ventas)
        qs = super().get_queryset(request)

        # Si el usuario es un superadministrador, puede ver todas las ventas.
        if request.user.is_superuser:
            return qs

        # Si es otro tipo de usuario (vendedor), solo ve sus propias ventas.
        return qs.filter(Usuarios=request.user)

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
        ('Permisos y Rol', {'fields': ('Roles', 'is_active', 'is_staff', 'is_superuser')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

# --- Admin para Pedidos y sus Detalles ---

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

# --- Registros de Modelos Adicionales ---
admin.site.register(Rol)
admin.site.register(Nutricional)
admin.site.register(DetalleVenta)