from django.db import models

class Proveedor(models.Model):
    rut = models.CharField(max_length=12, unique=True, verbose_name='RUT')
    nombre_empresa = models.CharField(max_length=200, verbose_name='Nombre Empresa')
    nombre_contacto = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nombre Contacto')
    email = models.EmailField(unique=True, verbose_name='Email')
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name='Dirección')
    rubro = models.CharField(max_length=100, blank=True, null=True, verbose_name='Rubro')
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre_empresa']

    def __str__(self):
        return self.nombre_empresa