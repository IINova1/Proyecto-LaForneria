from django.contrib import admin
from .models import (
    Categoria, Nutricional, Producto, Direccion, Rol, Usuario,
    Cliente, Venta, Lote, DetalleVenta, Organization, CustomUser
)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre",)


@admin.register(Nutricional)
class NutricionalAdmin(admin.ModelAdmin):
    list_display = ("id", "ingredientes", "tiempo_preparacion")
    search_fields = ("ingredientes",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "precio", "categoria", "stock_actual")
    search_fields = ("nombre", "marca")
    list_filter = ("categoria",)
    autocomplete_fields = ["categoria", "nutricional"]


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ("id", "calle", "numero", "comuna", "region")
    search_fields = ("calle", "comuna", "region")


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre",)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombres", "paterno", "run", "correo", "rol")
    search_fields = ("nombres", "paterno", "run", "correo")
    autocomplete_fields = ["direccion", "rol"]


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "cliente", "estado_pedido")
    search_fields = ("id", "cliente__nombre", "usuario__nombres")
    autocomplete_fields = ["usuario", "cliente"]


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ("id", "producto")
    search_fields = ("producto__nombre",)
    autocomplete_fields = ["producto"]


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ("id", "venta", "lote", "producto", "usuario")
    search_fields = ("venta__id", "producto__nombre", "usuario__nombres")
    autocomplete_fields = ["venta", "lote", "producto", "usuario"]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre",)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "organization", "is_staff")
    search_fields = ("username", "email")
    autocomplete_fields = ["organization"]
