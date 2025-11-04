# Contenido COMPLETO para: Proyecto-LaForneria/monitoreo/usuarios/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction

# --- ¡Importaciones Corregidas! ---
from .models import Usuario, Direccion, Rol 

# --- FORMULARIO DE REGISTRO PERSONALIZADO (SIMPLIFICADO) ---
class CustomRegisterForm(UserCreationForm):
    """
    Formulario para que los usuarios se registren.
    Asigna un rol de "Cliente" por defecto.
    LOS CAMPOS DE DIRECCIÓN HAN SIDO ELIMINADOS.
    """
    
    # --- LOS CAMPOS DE DIRECCIÓN SE ELIMINARON DE AQUÍ ---
    # calle = forms.CharField(...)
    # numero = forms.CharField(...)
    # ...etc...

    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Fono y materno siguen siendo opcionales en el registro
        fields = ('first_name', 'last_name', 'email', 'materno', 'run', 'fono')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # --- LÓGICA DE DIRECCIÓN ELIMINADA DE AQUÍ ---
        # El campo user.Direccion permanecerá null por ahora.
        
        # Asigna el Rol
        try:
            cliente_rol = Rol.objects.get(nombre='Cliente')
            user.Roles = cliente_rol
        except Rol.DoesNotExist:
            pass
            
        if commit:
            user.save()
        return user

# --- FORMULARIO DE LOGIN PERSONALIZADO (Sin cambios) ---
class CustomLoginForm(AuthenticationForm):
    """
    Formulario de login personalizado que usa email en lugar de username.
    """
    username = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autofocus': True})
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}),
    )

# --- ¡NUEVOS FORMULARIOS PARA LA PÁGINA DE PERFIL! ---

class UserProfileForm(forms.ModelForm):
    """
    Formulario para que el usuario actualice sus datos personales opcionales.
    """
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'materno', 'fono', 'run')
        # Hacemos que 'run' sea de solo lectura si ya está establecido,
        # pero editable si no lo está.
        widgets = {
            'run': forms.TextInput(attrs={'readonly': True})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.run:
            self.fields['run'].disabled = True
        else:
            self.fields['run'].disabled = False
            
        # El email no se debe cambiar desde aquí
        if 'email' in self.fields:
             self.fields['email'].disabled = True


class DireccionForm(forms.ModelForm):
    """
    Formulario para crear o actualizar la dirección del usuario.
    """
    class Meta:
        model = Direccion
        fields = ('calle', 'numero', 'depto', 'comuna', 'region', 'codigo_postal')