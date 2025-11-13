from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, Venta


# --- FORMULARIO DE CLIENTES ---
class ClienteForm(forms.ModelForm):
    """
    Formulario de clientes con validaciones básicas.
    """
    class Meta:
        model = Cliente
        fields = '__all__'

    def clean_idclientes(self):
        """
        Evita IDs duplicados o vacíos.
        """
        idclientes = self.cleaned_data.get('idclientes')
        if not idclientes:
            raise ValidationError("El ID del cliente no puede estar vacío.")
        if Cliente.objects.filter(idclientes=idclientes).exists():
            raise ValidationError(f"Ya existe un cliente con el ID {idclientes}.")
        return idclientes


# --- FORMULARIO DE VENTAS ---
class VentaForm(forms.ModelForm):
    """
    Formulario de ventas con control de consistencia.
    """
    class Meta:
        model = Venta
        fields = '__all__'
        widgets = {
            'EstadoPedido': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('Usuarios')
        cliente = cleaned_data.get('clientes_idclientes')
        estado = cleaned_data.get('EstadoPedido')

        # Validación de relaciones obligatorias
        if not usuario:
            raise ValidationError("Debe asociarse un usuario a la venta.")
        if not cliente:
            raise ValidationError("Debe seleccionarse un cliente.")

        # Validación del estado del pedido
        estados_validos = ['Pendiente', 'En preparación', 'Enviado', 'Completado', 'Cancelado']
        if estado and estado not in estados_validos:
            raise ValidationError(f"Estado '{estado}' no es válido.")

        return cleaned_data
