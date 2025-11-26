from rest_framework import viewsets
from catalogo.models import Producto
from proveedores.models import Proveedor
from .serializers import ProductoSerializer, ProveedorSerializer
from rest_framework.permissions import IsAuthenticated


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]
