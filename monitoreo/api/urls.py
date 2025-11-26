from django.urls import path, include
from rest_framework import routers
from .views import ProductoViewSet, ProveedorViewSet

# Crear el router y registrar nuestros viewsets
router = routers.DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'proveedores', ProveedorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]