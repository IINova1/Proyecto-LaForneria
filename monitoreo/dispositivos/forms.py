from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Producto, Categoria, Cliente, Venta, Direccion, Rol
from django.db import transaction

# --- FORMULARIO DE REGISTRO PERSONALIZADO ---
class CustomRegisterForm(UserCreationForm):
    """
    Formulario para que los usuarios se registren.
    Incluye campos para la dirección y asigna un rol de "Cliente" por defecto.
    """
    # 1. Campos para que el usuario ingrese su dirección manualmente.
    calle = forms.CharField(max_length=100, label="Calle", help_text="Nombre de la calle.")
    numero = forms.CharField(max_length=10, label="Número")
    depto = forms.CharField(max_length=10, required=False, label="Departamento (opcional)")
    comuna = forms.CharField(max_length=100, label="Comuna")
    region = forms.CharField(max_length=100, label="Región")
    codigo_postal = forms.CharField(max_length=45, required=False, label="Código Postal (opcional)")

    class Meta(UserCreationForm.Meta):
        model = Usuario
        # 2. Campos del modelo Usuario que se mostrarán en el formulario.
        fields = ('first_name', 'last_name', 'email', 'materno', 'run', 'fono')

    @transaction.atomic
    def save(self, commit=True):
        """
        Sobrescribe el método de guardado para crear la Dirección
        y asignar el Rol por defecto.
        """
        # Guarda la información básica del usuario (sin commit a la BD todavía).
        user = super().save(commit=False)

        # Crea el objeto Direccion con los datos del formulario.
        direccion = Direccion.objects.create(
            calle=self.cleaned_data.get('calle'),
            numero=self.cleaned_data.get('numero'),
            depto=self.cleaned_data.get('depto'),
            comuna=self.cleaned_data.get('comuna'),
            region=self.cleaned_data.get('region'),
            codigo_postal=self.cleaned_data.get('codigo_postal')
        )

        # Asigna la dirección creada al usuario.
        user.Direccion = direccion

        # Asigna un rol por defecto.
        try:
            # ¡IMPORTANTE! Asegúrate de tener un Rol con nombre 'Cliente' en tu BD.
            cliente_rol = Rol.objects.get(nombre='Cliente')
            user.Roles = cliente_rol
        except Rol.DoesNotExist:
            # Si el rol no existe, el usuario se crea sin rol.
            # Puedes crearlo desde el panel de administrador de Django.
            pass

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

# --- OTROS FORMULARIOS DE LA APLICACIÓN ---

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'