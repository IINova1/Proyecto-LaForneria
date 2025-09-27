from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Categorias'

    def __str__(self):
        return self.nombre


class Nutricional(models.Model):
    ingredientes = models.CharField(max_length=300, blank=True, null=True)
    tiempo_preparacion = models.CharField(max_length=100, blank=True, null=True)
    proteinas = models.CharField(max_length=45, blank=True, null=True)
    azucar = models.CharField(max_length=45, blank=True, null=True)
    gluten = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'Nutricional'

    def __str__(self):
        return f"Nutricional {self.id}"


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)
    caducidad = models.DateField()
    elaboracion = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, db_column="Categorias_id")
    stock_actual = models.IntegerField(blank=True, null=True)
    stock_minimo = models.IntegerField(blank=True, null=True)
    stock_maximo = models.IntegerField(blank=True, null=True)
    presentacion = models.CharField(max_length=100, blank=True, null=True)
    formato = models.CharField(max_length=100, blank=True, null=True)
    nutricional = models.ForeignKey(Nutricional, on_delete=models.PROTECT, db_column="Nutricional_id")
    creado = models.DateTimeField(blank=True, null=True)
    modificado = models.DateTimeField(blank=True, null=True)
    eliminado = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Productos'

    def __str__(self):
        return self.nombre


class Direccion(models.Model):
    calle = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    depto = models.CharField(max_length=10, blank=True, null=True)
    comuna = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'Direccion'

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.comuna}"


class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'Roles'

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    nombres = models.CharField(max_length=100)
    paterno = models.CharField(max_length=100)
    materno = models.CharField(max_length=100, blank=True, null=True)
    run = models.CharField(max_length=10, unique=True)
    correo = models.CharField(max_length=100)
    fono = models.IntegerField(blank=True, null=True)
    clave = models.CharField(max_length=150, blank=True, null=True)
    direccion = models.ForeignKey(Direccion, on_delete=models.PROTECT, db_column="Direccion_id")
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, db_column="Roles_id")

    class Meta:
        db_table = 'Usuarios'

    def __str__(self):
        return f"{self.nombres} {self.paterno}"

class Cliente(models.Model):
    id = models.AutoField(primary_key=True, db_column="idclientes")
    nombre = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'clientes'

    def __str__(self):
        return self.nombre if self.nombre else f"Cliente {self.id}"


class Venta(models.Model):
    id = models.AutoField(primary_key=True, db_column="idventa")
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column="Usuarios_id")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, db_column="clientes_idclientes")
    estado_pedido = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'venta'
        constraints = [
            models.UniqueConstraint(fields=['id', 'usuario', 'cliente'], name='unique_venta')
        ]

    def __str__(self):
        return f"Venta {self.id} - Cliente: {self.cliente}"


class Lote(models.Model):
    id = models.AutoField(primary_key=True, db_column="idLote")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, db_column="Productos_id")

    class Meta:
        db_table = 'Lote'
        constraints = [
            models.UniqueConstraint(fields=['id', 'producto'], name='unique_lote')
        ]

    def __str__(self):
        return f"Lote {self.id} - {self.producto}"


class DetalleVenta(models.Model):
    id = models.AutoField(primary_key=True, db_column="NumeroVenta")
    lote = models.ForeignKey(Lote, on_delete=models.PROTECT, db_column="Lote_idLote", related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, db_column="Lote_Productos_id")
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT, db_column="venta_idventa", related_name="detalles")
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column="venta_Usuarios_id")

    class Meta:
        db_table = 'Detalle venta'
        constraints = [
            models.UniqueConstraint(
                fields=['id', 'lote', 'producto', 'venta', 'usuario'],
                name='unique_detalle_venta'
            )
        ]

    def __str__(self):
        return f"DetalleVenta {self.id} - Venta {self.venta.id}"
    
class Organization(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class CustomUser(AbstractUser):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="usuarios"
    )

    def __str__(self):
        if self.organization:
            return f"{self.username} ({self.organization.nombre})"
        return self.username
