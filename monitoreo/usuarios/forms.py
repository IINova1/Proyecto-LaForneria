from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import Usuario, Direccion, Rol
import re # <-- Importado para Expresiones Regulares
from django.core.exceptions import ValidationError # <-- Importado para validaciones


# --- Función Auxiliar para Validar RUT Chileno ---
# --- Función Auxiliar para Validar RUT Chileno ---
# --- Función Auxiliar para Validar RUT Chileno ---
def validar_rut(rut):
    """
    Valida un RUT chileno.
    """
    rut = str(rut).upper().replace(".", "").replace("-", "")
    if not re.match(r'^\d{7,8}[0-9K]$', rut):
        return False
    
    cuerpo = rut[:-1]
    dv = rut[-1]
    
    try:
        suma = sum(int(cuerpo[-(i + 1)]) * (i % 6 + 2) for i in range(len(cuerpo)))
        
        # --- LÓGICA CORREGIDA ---
        resultado = 11 - (suma % 11)
        
        if resultado == 11:
            dv_calculado = '0'
        elif resultado == 10:
            dv_calculado = 'K'
        else:
            dv_calculado = str(resultado)
        # --- FIN DE LA CORRECCIÓN ---
            
        return dv == dv_calculado
    except ValueError:
        return False


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
        # Crear el usuario sin guardarlo todavía.
        # super().save() ya asigna todos los campos del Meta:
        # (first_name, last_name, materno, email, run, fono, avatar)
        user = super().save(commit=False)

        # Asignar rol 'Cliente' por defecto
        try:
            cliente_rol = Rol.objects.get(nombre='Cliente')
            user.Roles = cliente_rol
        except Rol.DoesNotExist:
            # ¡IMPORTANTE! Esto fallará si el Rol 'Cliente' no existe en la BD.
            # Asegúrate de crearlo después de migrar.
            print("ADVERTENCIA: El Rol 'Cliente' no existe en la BD. El usuario se creó sin rol.")
            pass
        
        # --- Las asignaciones redundantes de run, fono y avatar se eliminaron ---
        # super().save() ya se encargó de ellas.

        # Guardar en la base de datos
        if commit:
            user.save()

        return user

    # --- VALIDACIONES AÑADIDAS ---
    def clean_run(self):
        run_raw = self.cleaned_data.get('run')
        if not run_raw:
            raise ValidationError("Este campo es obligatorio.")
        
        # 1. LIMPIAMOS PRIMERO: Quitamos espacios, puntos, guiones
        run_limpio = str(run_raw).strip().upper().replace(".", "").replace("-", "")
        
        # 2. VALIDAMOS el RUT limpio
        if not validar_rut(run_limpio):
            # Mensaje más claro
            raise ValidationError("RUT inválido o dígito verificador incorrecto.")
        
        # 3. DEVOLVEMOS el RUT limpio para la BD
        return run_limpio

    def clean_fono(self):
        fono = self.cleaned_data.get('fono')
        if fono: # Solo valida si no está vacío
            # Regex para formato +569XXXXXXXX (9 dígitos después del +56)
            if not re.match(r'^\+569\d{8}$', fono):
                raise ValidationError("Formato de teléfono inválido. Debe ser +569XXXXXXXX")
        return fono
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # 2 MB Límite
            if avatar.size > 2 * 1024 * 1024: 
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
        widgets = {'run': forms.TextInput(attrs={'readonly': True})} # Hacemos 'run' solo lectura

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitamos el campo 'run' si el usuario ya tiene uno
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

    # --- VALIDACIÓN DE FONO AÑADIDA ---
    def clean_fono(self):
        fono = self.cleaned_data.get('fono')
        if fono: # Solo valida si no está vacío
            if not re.match(r'^\+569\d{8}$', fono):
                raise ValidationError("Formato de teléfono inválido. Debe ser +569XXXXXXXX")
        return fono
    
    # Nota: No necesitamos clean_run aquí porque el campo está deshabilitado
    # por __init__ y no se enviará para validación si ya existe.


# --- FORMULARIO DE DIRECCIÓN ---
class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ('calle', 'numero', 'depto', 'comuna', 'region', 'codigo_postal')