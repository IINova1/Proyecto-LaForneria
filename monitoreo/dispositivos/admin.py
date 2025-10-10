from datetime import date
from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils import timezone
import csv

from .models import (
    Usuario, Categoria, Producto, Cliente, Venta, DetalleVenta,
    Rol, Direccion, Nutricional, ReglaAlertaVencimiento, ProductoReglaAlerta, Lote
)

# --- Inline para ProductoReglaAlerta ---
class ProductoReglaAlertaInline(admin.TabularInline):
    model = ProductoReglaAlerta
    extra = 1
    autocomplete_fields = ['regla']



@admin.action(description="Exportar ventas seleccionadas a CSV")
def exportar_ventas_csv(modeladmin, request, queryset):
    """
    ✅ Exporta las ventas seleccionadas a un archivo CSV.
    Incluye validación para evitar ejecuciones vacías.
    """
    if not queryset.exists():
        modeladmin.message_user(
            request,
            "⚠️ Debes seleccionar al menos una venta para exportar.",
            level=messages.WARNING
        )
        return

    now = timezone.localtime(timezone.now()).strftime("%Y%m%d_%H%M%S")
    filename = f"ventas_{now}.csv"

    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)

    # Cabeceras del CSV
    writer.writerow(['ID Venta', 'Usuario email', 'Usuario nombre', 'Estado', 'Cliente ID', 'Num detalles'])

    qs = queryset.select_related('Usuarios', 'clientes_idclientes')

    for venta in qs.iterator():
        usuario_email = getattr(venta.Usuarios, 'email', '')
        usuario_nombre = " ".join(filter(None, [
            getattr(venta.Usuarios, 'first_name', ''),
            getattr(venta.Usuarios, 'last_name', '')
        ])).strip()
        cliente_id = getattr(venta.clientes_idclientes, 'idclientes', getattr(venta.clientes_idclientes, 'pk', ''))
        num_detalles = venta.detalleventa_set.count()
        writer.writerow([venta.idventa, usuario_email, usuario_nombre, venta.EstadoPedido or '', cliente_id, num_detalles])

    return response


@admin.action(description="Cambiar estado de ventas a 'Entregado'")
def marcar_como_entregado(modeladmin, request, queryset):
    """
    ✅ Cambia el estado de las ventas seleccionadas a 'Entregado'.
    Incluye validación si no hay elementos seleccionados.
    """
    if not queryset.exists():
        modeladmin.message_user(
            request,
            "⚠️ No seleccionaste ninguna venta para actualizar.",
            level=messages.WARNING
        )
        return

    updated = queryset.update(EstadoPedido="Entregado")
    modeladmin.message_user(
        request,
        f"✅ {updated} venta(s) actualizada(s) a 'Entregado'.",
        level=messages.SUCCESS
    )


@admin.action(description="Cambiar estado de ventas a 'En espera'")
def marcar_como_en_espera(modeladmin, request, queryset):
    """
    ✅ Cambia el estado de las ventas seleccionadas a 'En espera'.
    Incluye validación si no hay elementos seleccionados.
    """
    if not queryset.exists():
        modeladmin.message_user(
            request,
            "⚠️ No seleccionaste ninguna venta para actualizar.",
            level=messages.WARNING
        )
        return

    updated = queryset.update(EstadoPedido="En espera")
    modeladmin.message_user(
        request,
        f"✅ {updated} venta(s) actualizada(s) a 'En espera'.",
        level=messages.SUCCESS
    )

# --- Admin de Producto ---
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'precio', 'stock_actual', 'caducidad', 'Categorias')
    search_fields = ('nombre', 'marca')
    list_filter = ('Categorias',)
    ordering = ('caducidad',)
    list_select_related = ('Categorias', 'Nutricional')
    inlines = [ProductoReglaAlertaInline]
    actions = [exportar_ventas_csv,]


# --- Admins secundarios (sin cambios importantes) ---

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)

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


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('idventa', 'Usuarios', 'EstadoPedido', 'clientes_idclientes')
    search_fields = ('Usuarios__email', 'EstadoPedido')
    list_filter = ('EstadoPedido',)
    ordering = ('-idventa',)
    list_select_related = ('Usuarios', 'clientes_idclientes')
    inlines = [DetalleVentaInline]
    actions = [exportar_ventas_csv, marcar_como_entregado, marcar_como_en_espera]


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


admin.site.register(Nutricional)
admin.site.register(Rol)
admin.site.register(Lote)
admin.site.register(Cliente)
admin.site.register(Direccion)
