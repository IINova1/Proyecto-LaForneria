from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import Usuario, Direccion, Rol
import re # <-- Importado para Expresiones Regulares
from django.core.exceptions import ValidationError # <-- Importado para validaciones


# --- Función Auxiliar para Validar RUT Chileno ---
def validar_rut(rut_limpio):
    """
    Valida un RUT chileno (asume que ya viene limpio, ej: "12345678K").
    """
    if not re.match(r'^\d{7,8}[0-9K]$', rut_limpio):
        return False
    
    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1]
    
    try:
        suma = sum(int(cuerpo[-(i + 1)]) * (i % 6 + 2) for i in range(len(cuerpo)))
        resultado = 11 - (suma % 11)
        
        if resultado == 11:
            dv_calculado = '0'
        elif resultado == 10:
            dv_calculado = 'K'
        else:
            dv_calculado = str(resultado)
            
        return dv == dv_calculado
    except ValueError:
        return False


# --- FORMULARIO DE REGISTRO PERSONALIZADO ---
class CustomRegisterForm(UserCreationForm):
    """
    Formulario para que los usuarios se registren.
    Asigna un rol de 'Cliente' por defecto.
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
        user = super().save(commit=False)

        # Asignar rol 'Cliente' por defecto (con captura de errores robusta)
        try:
            cliente_rol = Rol.objects.get(nombre='Cliente')
            user.Roles = cliente_rol
        except Rol.DoesNotExist:
            # Si 'Cliente' no existe en la BD, se mostrará este error 
            # en la alerta roja {% if form.non_field_errors %}
            raise ValidationError("Error de configuración: El Rol 'Cliente' no existe en la base de datos.")
        except Exception as e:
            # Captura cualquier otro error (ej. tabla no existe)
            raise ValidationError(f"Error inesperado al asignar rol: {e}")

        if commit:
            user.save()
        return user

    # --- VALIDACIONES (Versión final) ---
    
    def clean_run(self):
        run_raw = self.cleaned_data.get('run')
        if not run_raw:
            raise ValidationError("Este campo es obligatorio.")
        
        # 1. LIMPIAMOS PRIMERO: Quitamos espacios, puntos, guiones
        run_limpio = str(run_raw).strip().upper().replace(".", "").replace("-", "")
        
        # 2. VALIDAMOS el RUT limpio
        if not validar_rut(run_limpio):
            raise ValidationError("RUT inválido o dígito verificador incorrecto.")
        
        # 3. DEVOLVEMOS el RUT limpio para la BD
        return run_limpio

    def clean_fono(self):
        fono = self.cleaned_data.get('fono')
        if fono:
            # Limpiamos espacios (ej. "+569 12345678")
            fono_limpio = fono.strip()
            if not re.match(r'^\+569\d{8}$', fono_limpio):
                raise ValidationError("Formato de teléfono inválido. Debe ser +569XXXXXXXX")
            return fono_limpio # Devolvemos el fono limpio
        return fono # Devuelve None o "" si está vacío
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024: # 2 MB Límite
                raise forms.ValidationError("¡La imagen es demasiado grande! (máximo 2MB)")
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'png', 'jpg']):
                raise forms.ValidationError("Tipo de archivo no válido. (Sube .jpg o .png)")
        return avatar


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

    def clean_fono(self):
        fono = self.cleaned_data.get('fono')
        if fono:
            # Limpiamos espacios también en el perfil
            fono_limpio = fono.strip()
            if not re.match(r'^\+569\d{8}$', fono_limpio):
                raise ValidationError("Formato de teléfono inválido. Debe ser +569XXXXXXXX")
            return fono_limpio
        return fono


# --- FORMULARIO DE DIRECCIÓN ---
class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ('calle', 'numero', 'depto', 'comuna', 'region', 'codigo_postal')