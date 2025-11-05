from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Proveedor

@login_required
def proveedor_list(request):
    # Solo el staff puede ver la lista
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
        
    proveedores = Proveedor.objects.all()
    context = {
        'proveedores': proveedores
    }
    return render(request, 'proveedores/proveedor_list.html', context)

# (Aquí añadiremos 'proveedor_create', 'proveedor_update', etc. más adelante)