from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

# --- ¡IMPORTACIONES CORREGIDAS! ---
from usuarios.models import Usuario
from catalogo.models import Producto
# ¡Pedido y Cliente ya estaban importados!
from pedidos.models import Pedido, Cliente 
from proveedores.models import Proveedor

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
        return redirect('pedidos:ver_productos')
    
    # Consultamos los modelos de sus apps correspondientes
    total_usuarios = Usuario.objects.count()
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()
    total_pedidos = Pedido.objects.count()
    
    # Esta línea fallará si la tabla 'proveedores_proveedor' no existe
    total_proveedores = Proveedor.objects.count()

    # --- ¡LÓGICA MEJORADA! ---
    # Esto es más intuitivo que el total de pedidos.
    total_pedidos_pendientes = Pedido.objects.filter(estado='Pendiente').count()
    
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
        'total_pedidos': total_pedidos, # Aún lo pasamos por si lo quieres usar
        'total_proveedores': total_proveedores,
        'productos_a_vencer': productos_a_vencer,

        # --- ¡NUEVO CONTEXTO AÑADIDO! ---
        'total_pedidos_pendientes': total_pedidos_pendientes,
    }
    return render(request, 'core/dashboard.html', context)
