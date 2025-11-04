from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

# --- ¡IMPORTACIONES CORREGIDAS! ---
# Importamos los modelos desde sus NUEVAS apps
# (Estos son necesarios para las estadísticas del dashboard)
from usuarios.models import Usuario
from catalogo.models import Producto
from pedidos.models import Pedido, Cliente

# --------------------
# Vistas Públicas (Para todos)
# --------------------

def inicio(request):
    """
    Vista para la página de inicio pública.
    """
    visitas = request.session.get('visitas', 0)
    request.session['visitas'] = visitas + 1
    context = {
        'visitas': request.session.get('visitas') # Pasamos el valor actualizado
    }
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'core/inicio.html', context)


# ----------------------------------------
# Vistas Protegidas (SOLO PARA ADMINS)
# ----------------------------------------

@login_required
def dashboard(request):
    """
    Vista para el panel de administración.
    """
    if not request.user.is_staff:
        # --- REDIRECCIÓN CORREGIDA ---
        # Si no es admin, lo mandamos a la tienda (en la app 'pedidos')
        return redirect('pedidos:ver_productos')
    
    # Consultamos los modelos de sus apps correspondientes
    total_usuarios = Usuario.objects.count()
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()
    total_pedidos = Pedido.objects.count()
    
    hoy = date.today()
    fecha_limite = hoy + timedelta(days=7)
    
    productos_a_vencer = Producto.objects.filter(
        caducidad__gte=hoy, 
        caducidad__lte=fecha_limite
    ).order_by('caducidad')
    
    context = {
        'total_usuarios': total_usuarios,
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_pedidos': total_pedidos,
        'productos_a_vencer': productos_a_vencer,
    }
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'core/dashboard.html', context)

# --- TODAS LAS OTRAS VISTAS (register, producto_list, ver_carrito, etc.) ---
# --- SE ELIMINAN DE ESTE ARCHIVO ---