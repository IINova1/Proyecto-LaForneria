from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# --- Manejador de Usuario (Sin cambios) ---
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('El email es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser debe tener is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

# --- MODELO USUARIO (CORREGIDO Y SIMPLIFICADO) ---
class Usuario(AbstractUser):
    # Desactivamos el username de Django
    username = None
    
    # Redefinimos los campos para que coincidan 100% con la BD corregida.
    # YA NO es necesario usar db_column.
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(_('email address'), unique=True)

    # Tus campos personalizados
    materno = models.CharField(max_length=100, blank=True, null=True)
    run = models.CharField(unique=True, max_length=10)
    fono = models.IntegerField(blank=True, null=True)
    
    Direccion = models.ForeignKey('Direccion', on_delete=models.DO_NOTHING, null=True, blank=True)
    Roles = models.ForeignKey('Rol', on_delete=models.DO_NOTHING, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'run']

    class Meta:
        # ¡Importante! Mantenemos managed = False
        managed = False
        db_table = 'Usuarios'
    
    def __str__(self):
        return self.email

# --- El resto de los modelos no necesitan cambios ---
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = False
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
        managed = False
        db_table = 'Nutricional'

    def __str__(self):
        return f"ingredientes {self.id}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)
    caducidad = models.DateField()
    elaboracion = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=100)
    Categorias = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, db_column='Categorias_id')
    stock_actual = models.IntegerField(blank=True, null=True)
    stock_minimo = models.IntegerField(blank=True, null=True)
    stock_maximo = models.IntegerField(blank=True, null=True)
    presentacion = models.CharField(max_length=100, blank=True, null=True)
    formato = models.CharField(max_length=100, blank=True, null=True)
    Nutricional = models.ForeignKey(Nutricional, on_delete=models.DO_NOTHING, db_column='Nutricional_id')
    creado = models.DateTimeField(blank=True, null=True)
    modificado = models.DateTimeField(blank=True, null=True)
    eliminado = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
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
        managed = False
        db_table = 'Direccion'

class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Roles'
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    idclientes = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'clientes'

class Venta(models.Model):
    idventa = models.IntegerField(primary_key=True, db_column='idventa')
    Usuarios = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, db_column='Usuarios_id')
    EstadoPedido = models.CharField(max_length=45, blank=True, null=True)
    clientes_idclientes = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, db_column='clientes_idclientes')
    class Meta:
        managed = False
        db_table = 'venta'

class Lote(models.Model):
    idLote = models.IntegerField(primary_key=True)
    Productos = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, db_column='Productos_id')
    class Meta:
        managed = False
        db_table = 'Lote'

class DetalleVenta(models.Model):
    id = models.IntegerField(primary_key=True)
    venta_idventa = models.ForeignKey(Venta, on_delete=models.DO_NOTHING, db_column='venta_idventa')
    Lote_idLote = models.ForeignKey(Lote, on_delete=models.DO_NOTHING, db_column='Lote_idLote')
    Lote_Productos_id = models.IntegerField() # Añadido para consistencia con tu script
    class Meta:
        managed = False
        db_table = 'Detalle venta'

class ReglaAlertaVencimiento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    dias_anticipacion = models.IntegerField(help_text="Días antes del vencimiento para generar la alerta")
    def __str__(self):
        return self.nombre

class ProductoReglaAlerta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    regla = models.ForeignKey(ReglaAlertaVencimiento, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('producto', 'regla')
    def __str__(self):
        return f"{self.producto.nombre} - {self.regla.nombre}"
    # ... (al final del archivo models.py)

class Pedido(models.Model):
    # --- INICIO DEL CÓDIGO ACTUALIZADO ---

    # Definimos los posibles estados de un pedido
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
    
    # Añadimos el nuevo campo 'estado'
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Pendiente' # Estado por defecto para nuevos pedidos
    )

    # --- FIN DEL CÓDIGO ACTUALIZADO ---
    
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
    mensaje = models.CharField(max_length=255)
    leido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.mensaje

    class Meta:
        ordering = ['-fecha_creacion']