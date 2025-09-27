from django.contrib import admin
<<<<<<< Updated upstream
from .models import Category, Zone, Device, Measurement, Alert, Organization, CustomUser

#Registro del modelo Categoria
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'created_at', 'organization')
    search_fields = ('name',)
    list_filter = ('status', 'organization')

#Registro del modelo Zona
@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'created_at', 'organization')
    search_fields = ('name',)
    list_filter = ('status', 'organization')

#Registro del modelo Dispositivo
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_consumption', 'category', 'zone', 'status', 'created_at', 'organization')
    search_fields = ('name',)
    list_filter = ('category', 'zone', 'status', 'organization')

#Registro del modelo Medicion
@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('device', 'consumption_w', 'timestamp', 'status', 'organization')
    list_filter = ('device', 'timestamp', 'organization')
    search_fields = ('device__name',)

#Registro del modelo Alerta
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('measurement', 'message', 'timestamp', 'reviewed', 'status', 'organization')
    list_filter = ('reviewed', 'timestamp', 'organization')
    search_fields = ('message', 'measurement__device__name')

#REgistro del modelo Organizacion
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'created_at')
    search_fields = ('name',)
    list_filter = ('status',)

# Registro del modelo CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'organization', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'organization')
=======
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
>>>>>>> Stashed changes
