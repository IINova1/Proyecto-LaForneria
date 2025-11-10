import csv
from django.http import HttpResponse
from django.contrib import admin

# --- ¡Importaciones Corregidas! ---
from .models import (
    Cliente, Venta, DetalleVenta, Pedido, DetallePedido, Lote
)

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

# --- Admin Operacionales ---
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('idclientes',)
    search_fields = ('idclientes',)
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