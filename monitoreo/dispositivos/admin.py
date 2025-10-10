import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import (
    Usuario, Categoria, Producto, Cliente, Venta, DetalleVenta,
    Rol, Direccion, Nutricional, ReglaAlertaVencimiento, ProductoReglaAlerta,
    Pedido, DetallePedido, Lote
)

# --- Acción personalizada: exportar productos ---
def exportar_productos_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Marca', 'Precio', 'Stock', 'Caducidad', 'Categoría'])
    for producto in queryset:
        writer.writerow([
            producto.nombre,
            producto.marca,
            producto.precio,
            producto.stock_actual,
            producto.caducidad,
            producto.Categorias.nombre if producto.Categorias else 'Sin categoría'
        ])
    return response
exportar_productos_csv.short_description = "📤 Exportar productos seleccionados a CSV"

# --- Acción personalizada: exportar ventas ---
def exportar_ventas_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ventas.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID Venta', 'Usuario Email', 'Usuario Nombre', 'Estado', 'Cliente ID', 'Num detalles', 'Fecha'])
    
    qs = queryset.select_related('Usuarios', 'clientes_idclientes')
    for venta in qs:
        usuario_email = getattr(venta.Usuarios, 'email', '')
        usuario_nombre = " ".join(filter(None, [getattr(venta.Usuarios, 'first_name',''), getattr(venta.Usuarios, 'last_name','')])).strip()
        cliente_id = getattr(venta.clientes_idclientes, 'idclientes', getattr(venta.clientes_idclientes, 'pk', ''))
        num_detalles = venta.detalleventa_set.count() if hasattr(venta, 'detalleventa_set') else 0
        fecha = getattr(venta, 'fecha_pedido', '')
        writer.writerow([
            venta.idventa,
            usuario_email,
            usuario_nombre,
            venta.EstadoPedido or '',
            cliente_id,
            num_detalles,
            fecha
        ])
exportar_ventas_csv.short_description = "📤 Exportar ventas seleccionadas a CSV"

# --- Admin para Categoría ---
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)
    def has_module_permission(self, request): return request.user.is_superuser

# --- Admin para Producto ---
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'precio', 'stock_actual', 'caducidad', 'Categorias')
    search_fields = ('nombre', 'marca')
    list_filter = ('Categorias',)
    ordering = ('caducidad',)
    list_select_related = ('Categorias', 'Nutricional')
    actions = [exportar_productos_csv]
    def has_module_permission(self, request): return request.user.is_staff

# --- Admin para Regla de Alerta ---
@admin.register(ReglaAlertaVencimiento)
class ReglaAlertaVencimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dias_anticipacion', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('dias_anticipacion',)
    ordering = ('dias_anticipacion',)
    def has_module_permission(self, request): return request.user.is_superuser

@admin.register(ProductoReglaAlerta)
class ProductoReglaAlertaAdmin(admin.ModelAdmin):
    list_display = ('get_producto_nombre', 'get_regla_nombre')
    list_filter = ('regla__nombre',)
    search_fields = ('producto__nombre', 'regla__nombre')
    list_select_related = ('producto', 'regla')
    actions = []

    @admin.display(description='Producto', ordering='producto__nombre')
    def get_producto_nombre(self, obj): return obj.producto.nombre

    @admin.display(description='Regla', ordering='regla__nombre')
    def get_regla_nombre(self, obj): return obj.regla.nombre

    def has_module_permission(self, request): return request.user.is_superuser

# --- Admin Operacionales ---
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('idclientes',)
    search_fields = ('idclientes',)
    def has_module_permission(self, request): return request.user.is_superuser

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('calle', 'numero', 'comuna', 'region')
    search_fields = ('calle', 'comuna', 'region')
    list_filter = ('region', 'comuna')
    ordering = ('region', 'comuna')
    def has_module_permission(self, request): return request.user.is_superuser

# --- Inline para DetalleVenta ---
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0
    readonly_fields = ('mostrar_producto', 'Lote_idLote', 'Lote_Productos_id')

    @admin.display(description="Producto")
    def mostrar_producto(self, obj):
        if obj.Lote_idLote and obj.Lote_idLote.Productos:
            return obj.Lote_idLote.Productos.nombre
        return "—"

# --- Admin para Venta ---
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('idventa', 'Usuarios', 'EstadoPedido', 'clientes_idclientes')
    search_fields = ('Usuarios__email', 'EstadoPedido')
    list_filter = ('EstadoPedido',)
    ordering = ('-idventa',)
    list_select_related = ('Usuarios', 'clientes_idclientes')
    inlines = [DetalleVentaInline]
    actions = [exportar_ventas_csv]
    def has_module_permission(self, request): return request.user.is_superuser

# --- Inline para DetallePedido ---
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio')

# --- Admin para Pedido ---
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_pedido', 'total', 'estado')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('id', 'usuario__email')
    ordering = ('-fecha_pedido',)
    list_editable = ('estado',)
    inlines = [DetallePedidoInline]
    def has_module_permission(self, request): return request.user.is_superuser

# --- Admin para Usuario ---
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
    def has_module_permission(self, request): return request.user.is_superuser

# --- Admin adicionales ---
admin.site.register(Rol)
admin.site.register(Nutricional)
