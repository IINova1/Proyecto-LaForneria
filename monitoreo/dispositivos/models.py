from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
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

# --- MODELO USUARIO (CORREGIDO Y FINALIZADO) ---
class Usuario(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    materno = models.CharField(max_length=100, blank=True, null=True)
    run = models.CharField(unique=True, max_length=10)
    fono = models.IntegerField(blank=True, null=True)
    
    # Campos renombrados para seguir las convenciones de Django (minúsculas)
    direccion = models.ForeignKey('Direccion', on_delete=models.SET_NULL, null=True, blank=True)
    rol = models.ForeignKey('Rol', on_delete=models.SET_NULL, null=True, blank=True)

    # Corregido para evitar conflictos de related_name cuando Django gestiona la BD
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name="usuario_groups",  # Nombre único
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name="usuario_permissions", # Nombre único
        related_query_name="usuario",
    )

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'run']

    def __str__(self):
        return self.email

# --- MODELOS GESTIONADOS POR DJANGO ---
# Se eliminó `managed = False` y `db_table` de todos los modelos a continuación.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.nombre

class Nutricional(models.Model):
    ingredientes = models.CharField(max_length=300, blank=True, null=True)
    tiempo_preparacion = models.CharField(max_length=100, blank=True, null=True)
    proteinas = models.CharField(max_length=45, blank=True, null=True)
    azucar = models.CharField(max_length=45, blank=True, null=True)
    gluten = models.CharField(max_length=45, blank=True, null=True)
    def __str__(self):
        return f"Nutricional ID: {self.id}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)
    caducidad = models.DateField()
    elaboracion = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    nutricional = models.ForeignKey(Nutricional, on_delete=models.SET_NULL, null=True)
    stock_actual = models.IntegerField(blank=True, null=True)
    stock_minimo = models.IntegerField(blank=True, null=True)
    stock_maximo = models.IntegerField(blank=True, null=True)
    presentacion = models.CharField(max_length=100, blank=True, null=True)
    formato = models.CharField(max_length=100, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True, null=True)
    modificado = models.DateTimeField(auto_now=True, null=True)
    eliminado = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.nombre

class Direccion(models.Model):
    calle = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    depto = models.CharField(max_length=10, blank=True, null=True)
    comuna = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=45, blank=True, null=True)

class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    idclientes = models.IntegerField(primary_key=True)

class Venta(models.Model):
    vendedor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    estado_pedido = models.CharField(max_length=45, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En preparación', 'En preparación'),
        ('Listo para retirar', 'Listo para retirar'),
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