from django.contrib import admin
from .models import (
    Usuario, Categoria, Producto, Cliente, Venta, DetalleVenta, 
    Rol, Direccion, Nutricional, ReglaAlertaVencimiento, ProductoReglaAlerta, Lote
)
import csv
from django.http import HttpResponse
from django.utils import timezone


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



# --- Inline para DetalleVenta ---

class DetalleVentaInline(admin.TabularInline):  
    model = DetalleVenta
    extra = 1  

#---Funciones Venta Admin ---
@admin.action(description="Exportar ventas seleccionadas a CSV")
def exportar_ventas_csv(modeladmin, request, queryset):
    """
    Exporta las ventas seleccionadas a un CSV descargable.
    Incluye: ID venta, email usuario, nombre usuario, estado, id cliente y número de detalles.
    """
    now = timezone.localtime(timezone.now()).strftime("%Y%m%d_%H%M%S")
    filename = f"ventas_{now}.csv"
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    # Cabecera (ajusta columnas según necesites)
    writer.writerow(['ID Venta', 'Usuario email', 'Usuario nombre', 'Estado', 'Cliente ID', 'Num detalles'])

    # select_related para optimizar (trae Usuarios y Cliente en la misma consulta)
    qs = queryset.select_related('Usuarios', 'clientes_idclientes')

    for venta in qs.iterator():
        # Campos FK seguros (evitar fallos si son None)
        usuario_email = getattr(venta.Usuarios, 'email', '')
        usuario_nombre = " ".join(filter(None, [
            getattr(venta.Usuarios, 'first_name', '') or '',
            getattr(venta.Usuarios, 'last_name', '') or ''
        ])).strip()
        cliente_id = getattr(venta.clientes_idclientes, 'idclientes', getattr(venta.clientes_idclientes, 'pk', ''))
        # Contar detalles (si la relación existe)
        try:
            num_detalles = venta.detalleventa_set.count()
        except Exception:
            num_detalles = ''

        writer.writerow([
            venta.idventa,
            usuario_email,
            usuario_nombre,
            venta.EstadoPedido or '',
            cliente_id,
            num_detalles
        ])

    return response

# --- Admin para Venta con Inline ---
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('idventa', 'Usuarios', 'EstadoPedido', 'clientes_idclientes')
    search_fields = ('Usuarios__email', 'EstadoPedido')
    list_filter = ('EstadoPedido',)
    ordering = ('-idventa',)
    list_select_related = ('Usuarios', 'clientes_idclientes')
    inlines = [DetalleVentaInline]
    actions = [exportar_ventas_csv] 




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

# --- Registros simples sin admin personalizado ---
admin.site.register(Nutricional)
admin.site.register(Rol)
admin.site.register(Lote)
