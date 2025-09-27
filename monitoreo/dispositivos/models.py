from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# --- Manejador de Usuario Personalizado (Ajustado y Final) ---

class CustomUserManager(BaseUserManager):
    """
    Manager personalizado para el modelo Usuario donde el email es el identificador único.
    """
    # --- LÍNEA CORREGIDA ---
    # Se cambia el parámetro de 'correo' a 'email' para que coincida con el USERNAME_FIELD
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('El email es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # --- LÍNEA CORREGIDA ---
    # Se cambia el parámetro de 'correo' a 'email' aquí también
    def create_superuser(self, email, password, **extra_fields):
        """
        Crea y guarda un Superusuario con el email y contraseña dados.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser debe tener is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)

# --- Modelos de la Aplicación ---

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

class Usuario(AbstractUser):
    username = None
    
    first_name = models.CharField(max_length=100, db_column='nombres')
    last_name = models.CharField(max_length=100, db_column='paterno')
    email = models.EmailField(_('correo'), unique=True, db_column='correo')

    materno = models.CharField(max_length=100, blank=True, null=True)
    run = models.CharField(unique=True, max_length=10)
    fono = models.IntegerField(blank=True, null=True)
    
    Direccion = models.ForeignKey(Direccion, on_delete=models.DO_NOTHING, null=True, blank=True, db_column='Direccion_id')
    Roles = models.ForeignKey(Rol, on_delete=models.DO_NOTHING, null=True, blank=True, db_column='Roles_id')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'run']

    class Meta:
        managed = False
        db_table = 'Usuarios'
    
    def __str__(self):
        return self.email

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
    class Meta:
        managed = False
        db_table = 'Detalle venta'