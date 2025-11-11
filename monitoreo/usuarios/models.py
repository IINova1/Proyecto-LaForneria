from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

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

class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        managed = True # <-- ¡CORREGIDO!
        db_table = 'Roles'
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
        managed = True # <-- ¡CORREGIDO!
        db_table = 'Direccion'

class Usuario(AbstractUser):
    username = None
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    materno = models.CharField(max_length=100, blank=True, null=True)
    run = models.CharField(unique=True, max_length=10)
    fono = models.IntegerField(blank=True, null=True)
    
    # --- ¡CAMPO AÑADIDO AQUÍ! ---
    avatar = models.ImageField(upload_to='avatares/', null=True, blank=True, verbose_name='Avatar')
    
    Direccion = models.ForeignKey('Direccion', on_delete=models.DO_NOTHING, null=True, blank=True)
    Roles = models.ForeignKey('Rol', on_delete=models.DO_NOTHING, null=True, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'run']
    class Meta:
        managed = True # <-- ¡CORREGIDO!
        db_table = 'Usuarios'
    def __str__(self):
        return self.email