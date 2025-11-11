from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# --- MANAGER PERSONALIZADO (para login con email) ---
class CustomUserManager(BaseUserManager):
    """
    Manager personalizado para el modelo Usuario donde el email es el identificador.
    """
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

# --- Modelo de Roles ---
class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    # He quitado 'descripcion' para mantenerlo simple, puedes volver a añadirlo si lo usas.

    def __str__(self):
        return self.nombre

# --- Modelo de Direccion ---
class Direccion(models.Model):
    calle = models.CharField(max_length=100)
    numero = models.CharField(max_length=20)
    depto = models.CharField(max_length=50, blank=True, null=True)
    comuna = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.comuna}"

# --- Modelo de Usuario Personalizado (Principal) ---
class Usuario(AbstractUser):
    username = None  # Eliminamos el username
    email = models.EmailField(_('email address'), unique=True) # El email será el login
    
    # --- Datos Personales ---
    run = models.CharField(max_length=12, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=150) # Aumentado para consistencia
    last_name = models.CharField(max_length=150) # Aumentado para consistencia
    materno = models.CharField(max_length=100, blank=True, null=True)
    
    # Correcto: CharField para aceptar "+569..."
    fono = models.CharField(max_length=20, blank=True, null=True) 
    
    avatar = models.ImageField(upload_to='avatares/', blank=True, null=True)
    
    # --- Relaciones (Versión Corregida) ---
    
    # Usamos SET_NULL para que si se borra un Rol, el usuario no se borre.
    Roles = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True) 
    
    # Usamos OneToOneField: Un usuario solo tiene UNA dirección.
    # Usamos SET_NULL para que si se borra la Dirección, el usuario no se borre.
    Direccion = models.OneToOneField(Direccion, on_delete=models.SET_NULL, null=True, blank=True)

    # --- Configuración de autenticación ---
    objects = CustomUserManager() # Asignamos el manager personalizado
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['run', 'first_name', 'last_name']

    def __str__(self):
        return self.email