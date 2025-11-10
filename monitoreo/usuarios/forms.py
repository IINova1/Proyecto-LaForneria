from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import Usuario, Direccion, Rol


# --- FORMULARIO DE REGISTRO PERSONALIZADO ---
class CustomRegisterForm(UserCreationForm):
    """
    Formulario para que los usuarios se registren.
    Asigna un rol de 'Cliente' por defecto.
    El campo avatar es opcional.
    """
    avatar = forms.ImageField(
        required=False,
        label="Foto de perfil (opcional)",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('first_name', 'last_name', 'materno', 'email', 'run', 'fono', 'avatar')

    @transaction.atomic
    def save(self, commit=True):
        # Crear el usuario sin guardarlo todavía
        user = super().save(commit=False)

        # Asignar rol 'Cliente' por defecto
        try:
            cliente_rol = Rol.objects.get(nombre='Cliente')
            user.Roles = cliente_rol
        except Rol.DoesNotExist:
            pass

        # Asignar avatar si se subió
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            user.avatar = avatar

        # Guardar en la base de datos
        if commit:
            user.save()

        return user


# --- FORMULARIO DE LOGIN PERSONALIZADO ---
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


# --- FORMULARIO DE PERFIL ---
class UserProfileForm(forms.ModelForm):
    """
    Formulario para que el usuario actualice sus datos personales.
    """
    class Meta:
        model = Usuario
        fields = ('avatar', 'first_name', 'last_name', 'materno', 'fono', 'run')
        widgets = {'run': forms.TextInput(attrs={'readonly': True})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.run:
            self.fields['run'].disabled = True

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError("¡La imagen es demasiado grande! (máximo 2MB)")
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'png', 'jpg']):
                raise forms.ValidationError("Tipo de archivo no válido. (Sube .jpg o .png)")
        return avatar


# --- FORMULARIO DE DIRECCIÓN ---
class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ('calle', 'numero', 'depto', 'comuna', 'region', 'codigo_postal')
