# proveedores/models.py
from django.db import models

class Proveedor(models.Model):
    rut = models.CharField(max_length=15, unique=True)
    nombre_empresa = models.CharField(max_length=100)
    nombre_contacto = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    rubro = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_empresa} ({self.rut})"

    class Meta:
        db_table = "proveedores"
        ordering = ["nombre_empresa"]
