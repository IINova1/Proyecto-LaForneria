"""
URL configuration for monitoreo project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- LÍNEAS CORREGIDAS ---
    # Se añaden las rutas a las 4 nuevas apps
    
    # La app 'core' maneja la raíz ('') y el dashboard
    path('', include(('core.urls', 'core'), namespace='core')),
    
    # La app 'usuarios' maneja la autenticación (ej. /auth/login)
    path('auth/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
    
    # La app 'catalogo' maneja los productos (ej. /catalogo/productos)
    path('catalogo/', include(('catalogo.urls', 'catalogo'), namespace='catalogo')),
    
    # La app 'pedidos' maneja la tienda (ej. /tienda, /carrito)
    path('', include(('pedidos.urls', 'pedidos'), namespace='pedidos')),
]

# Configuración para servir archivos multimedia (imágenes) en modo de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)