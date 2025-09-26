from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Base model with common attributes
class BaseModel(models.Model):
    STATUS_CHOICES = [
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVO")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

# Modelo Organización (ya no depende de Zona)
class Organization(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Modelo Zona (debe ir antes si Organization depende de ella)
class Zone(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, help_text="Zone description.")
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='zones')

    def __str__(self):
        return self.name

# Modelo de usuario personalizado
class CustomUser(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.organization.name})" if self.organization else self.username

# Modelo Categoría
class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Modelo Dispositivo
class Device(BaseModel):
    name = models.CharField(max_length=100)
    max_consumption = models.IntegerField(help_text="Maximum consumption in watts")
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='dispositivos/', null=True, blank=True)

    def __str__(self):
        return self.name

# Modelo Medición
class Measurement(BaseModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    consumption_w = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"Measurement of {self.device.name} - {self.consumption_w}W"

# Modelo Alerta
class Alert(BaseModel):
    measurement = models.OneToOneField(Measurement, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    reviewed = models.BooleanField(default=False, help_text="Indicates if the alert has been reviewed.")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"Alert for {self.measurement.device.name}"