from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# --- Manejador de Usuario Personalizado ---

class CustomUserManager(BaseUserManager):
    """
    Manejador de modelo de usuario personalizado donde el email es el identificador
    único para la autenticación en lugar de los nombres de usuario.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Crea y guarda un usuario con el email y la contraseña dados.
        """
        if not email:
            raise ValueError(_('El Email es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Crea y guarda un superusuario con el email y la contraseña dados.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser debe tener is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


# --- Modelo de Usuario Personalizado ---

class CustomUser(AbstractUser):
    username = None  # Eliminamos el campo username
    email = models.EmailField(_('dirección de email'), unique=True)
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('USER', 'Usuario'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='USER')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# --- Otros Modelos de la Aplicación ---

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='dispositivos/', blank=True, null=True)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombres = models.CharField(max_length=100)
    paterno = models.CharField(max_length=50)
    materno = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.paterno} {self.materno or ''}".strip()


class Venta(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    estado_pedido = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta a {self.cliente.nombres} ({self.fecha.strftime('%d-%m-%Y')})"
    
    @property
    def precio_total(self):
        return sum(item.total for item in self.detalleventa_set.all())


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    @property
    def total(self):
        return self.cantidad * self.producto.precio
