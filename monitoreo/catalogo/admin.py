import csv
from django.http import HttpResponse
from django.contrib import admin

# --- ¡Importaciones Corregidas! ---
from .forms import ProductoForm
from .models import (
    Categoria, Producto, Nutricional, 
    ReglaAlertaVencimiento, ProductoReglaAlerta
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
    form = ProductoForm # Activa la validación de stock
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

# --- Admin adicional ---
admin.site.register(Nutricional)