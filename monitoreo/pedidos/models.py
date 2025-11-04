from django.db import models
from usuarios.models import Usuario
from catalogo.models import Producto

class Cliente(models.Model):
    idclientes = models.IntegerField(primary_key=True)
    class Meta:
        managed = True # <-- ¡CORREGIDO!
        db_table = 'clientes'

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En preparación', 'En preparación'),
        ('Enviado', 'Enviado'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    def __str__(self):
        return f"Pedido {self.id} de {self.usuario.email}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    mensaje = models.CharField(max_length=255)
    leido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.mensaje
    class Meta:
        ordering = ['-fecha_creacion']

class Venta(models.Model):
    idventa = models.IntegerField(primary_key=True, db_column='idventa')
    Usuarios = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, db_column='Usuarios_id')
    EstadoPedido = models.CharField(max_length=45, blank=True, null=True)
    clientes_idclientes = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, db_column='clientes_idclientes')
    class Meta:
        managed = True # <-- ¡CORREGIDO!
        db_table = 'venta'

class Lote(models.Model):
    idLote = models.IntegerField(primary_key=True)
    Productos = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, db_column='Productos_id')
    class Meta:
        managed = True # <-- ¡CORREGIDO!
        db_table = 'Lote'

class DetalleVenta(models.Model):
    id = models.IntegerField(primary_key=True)
    venta_idventa = models.ForeignKey(Venta, on_delete=models.DO_NOTHING, db_column='venta_idventa')
    Lote_idLote = models.ForeignKey(Lote, on_delete=models.DO_NOTHING, db_column='Lote_idLote')
    Lote_Productos_id = models.IntegerField()
    class Meta:
        managed = True # <-- ¡CORREGIDO!
        db_table = 'Detalle venta'