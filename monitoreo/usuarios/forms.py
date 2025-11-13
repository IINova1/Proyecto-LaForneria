from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Usuario, Direccion, Rol

# ----------------------------------------------------------
# --- FORMULARIO DE REGISTRO PERSONALIZADO ---
# ----------------------------------------------------------
class CustomRegisterForm(UserCreationForm):
    """
    Formulario para registrar nuevos usuarios con validaciones personalizadas.
    - Verifica duplicados de email y RUN.
    - Valida formato de RUN chileno y teléfono.
    - Asigna rol 'Cliente' por defecto.
    - Controla tamaño y tipo de avatar.
    """

    avatar = forms.ImageField(
        required=False,
        label="Foto de perfil (opcional)",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    run = forms.CharField(
        label="RUN",
        max_length=12,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12.345.678-9'})
    )

    fono = forms.CharField(
        label="Teléfono",
        required=False,
        validators=[RegexValidator(r'^\+?\d[\d\s\-]{7,14}$', 'Formato de teléfono inválido.')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'})
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('first_name', 'last_name', 'materno', 'email', 'run', 'fono', 'avatar')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido paterno'}),
            'materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido materno'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está registrado.")
        return email

    def clean_run(self):
        run = self.cleaned_data.get('run').strip()
        run_regex = r'^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$'
        import re
        if not re.match(run_regex, run):
            raise ValidationError("Formato de RUN inválido. Ejemplo: 12.345.678-9")
        if Usuario.objects.filter(run=run).exists():
            raise ValidationError("Este RUN ya está registrado.")
        return run

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise ValidationError("La imagen supera los 2MB permitidos.")
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'png', 'jpg']):
                raise ValidationError("Solo se permiten imágenes JPG o PNG.")
        return avatar

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        try:
            rol_cliente = Rol.objects.get(nombre='Cliente')
            user.Roles = rol_cliente
        except Rol.DoesNotExist:
            pass

        if commit:
            user.save()
        return user


# ----------------------------------------------------------
# --- FORMULARIO DE LOGIN PERSONALIZADO ---
# ----------------------------------------------------------
class CustomLoginForm(AuthenticationForm):
    """
    Formulario de login usando email.
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

    def clean_username(self):
        email = self.cleaned_data.get('username').lower()
        if not Usuario.objects.filter(email=email).exists():
            raise ValidationError("No existe una cuenta registrada con este correo.")
        return email


# ----------------------------------------------------------
# --- FORMULARIO DE PERFIL ---
# ----------------------------------------------------------
class UserProfileForm(forms.ModelForm):
    """
    Permite actualizar los datos personales del usuario actual.
    """

    fono = forms.CharField(
        label="Teléfono",
        required=False,
        validators=[RegexValidator(r'^\+?\d[\d\s\-]{7,14}$', 'Formato de teléfono inválido.')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'})
    )

    class Meta:
        model = Usuario
        fields = ('avatar', 'first_name', 'last_name', 'materno', 'fono', 'run')
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'materno': forms.TextInput(attrs={'class': 'form-control'}),
            'fono': forms.TextInput(attrs={'class': 'form-control'}),
            'run': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise ValidationError("El archivo de imagen no debe superar los 2MB.")
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'png', 'jpg']):
                raise ValidationError("Solo se permiten archivos .jpg o .png.")
        return avatar


# ----------------------------------------------------------
# --- FORMULARIO DE DIRECCIÓN ---
# ----------------------------------------------------------
class DireccionForm(forms.ModelForm):
    """
    Controla la validación de campos de dirección.
    Evita campos vacíos o con caracteres inválidos.
    """
    class Meta:
        model = Direccion
        fields = ('calle', 'numero', 'depto', 'comuna', 'region', 'codigo_postal')
        widgets = {
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'depto': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if numero and not numero.isdigit():
            raise ValidationError("El número debe contener solo dígitos.")
        return numero

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('calle') or not cleaned.get('comuna') or not cleaned.get('region'):
            raise ValidationError("Los campos Calle, Comuna y Región son obligatorios.")
        return cleaned
