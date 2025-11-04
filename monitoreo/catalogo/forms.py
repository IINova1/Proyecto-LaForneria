from django import forms

# --- ¡Importaciones Corregidas! ---
# Importa los modelos desde la app local 'catalogo'
from .models import Producto, Categoria

# --- FORMULARIO DE PRODUCTO CON VALIDACIÓN ---
class ProductoForm(forms.ModelForm):
    """
    Un formulario de producto que ahora incluye validaciones de negocio para el stock.
    """
    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'marca', 'precio', 'caducidad', 
            'elaboracion', 'tipo', 'Categorias', 'stock_actual', 
            'stock_minimo', 'stock_maximo', 'presentacion', 'formato',
            'Nutricional' 
        ]
        widgets = {
            'caducidad': forms.DateInput(attrs={'type': 'date'}),
            'elaboracion': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        stock_minimo = cleaned_data.get("stock_minimo")
        stock_maximo = cleaned_data.get("stock_maximo")
        stock_actual = cleaned_data.get("stock_actual")

        if stock_minimo is not None and stock_maximo is not None:
            if stock_minimo >= stock_maximo:
                raise forms.ValidationError(
                    "Error de lógica: El stock mínimo no puede ser mayor o igual al stock máximo."
                )
        
        if stock_actual is not None and stock_minimo is not None and stock_maximo is not None:
            if not (stock_minimo <= stock_actual <= stock_maximo):
                 raise forms.ValidationError(
                    "Error de consistencia: El stock actual debe estar entre los valores de stock mínimo y máximo."
                )
                
        return cleaned_data

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'