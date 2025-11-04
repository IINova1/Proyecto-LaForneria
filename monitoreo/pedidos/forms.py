from django import forms

# --- ¡Importaciones Corregidas! ---
from .models import Cliente, Venta 

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'