from rest_framework import serializers
from catalogo.models import Producto
from proveedores.models import Proveedor

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__' # Expone todos los campos del producto

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__' # Expone todos los campos del proveedor