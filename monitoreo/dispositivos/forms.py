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
    calle = forms.CharField(max_length=100, label="Calle", help_text="Nombre de la calle.")
    numero = forms.CharField(max_length=10, label="Número")
    depto = forms.CharField(max_length=10, required=False, label="Departamento (opcional)")
    comuna = forms.CharField(max_length=100, label="Comuna")
    region = forms.CharField(max_length=100, label="Región")
    codigo_postal = forms.CharField(max_length=45, required=False, label="Código Postal (opcional)")

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'materno', 'run', 'fono')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        direccion = Direccion.objects.create(
            calle=self.cleaned_data.get('calle'),
            numero=self.cleaned_data.get('numero'),
            depto=self.cleaned_data.get('depto'),
            comuna=self.cleaned_data.get('comuna'),
            region=self.cleaned_data.get('region'),
            codigo_postal=self.cleaned_data.get('codigo_postal')
        )
        user.Direccion = direccion
        try:
            cliente_rol = Rol.objects.get(nombre='Cliente')
            user.Roles = cliente_rol
        except Rol.DoesNotExist:
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

# --- FORMULARIO DE PRODUCTO SIMPLIFICADO ---
class ProductoForm(forms.ModelForm):
    """
    Un formulario de producto más limpio que solo pide los datos necesarios.
    """
    class Meta:
        model = Producto
        # Seleccionamos solo los campos que el usuario debe ingresar manualmente
        fields = [
            'nombre', 'descripcion', 'marca', 'precio', 'caducidad', 
            'elaboracion', 'tipo', 'Categorias', 'stock_actual', 
            'stock_minimo', 'stock_maximo', 'presentacion', 'formato',
            'Nutricional' 
        ]
        # Hacemos que los campos de fecha usen un widget de calendario amigable
        widgets = {
            'caducidad': forms.DateInput(attrs={'type': 'date'}),
            'elaboracion': forms.DateInput(attrs={'type': 'date'}),
        }



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