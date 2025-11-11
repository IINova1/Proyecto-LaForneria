from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Proveedor
from .forms import ProveedorForm

@login_required
def listar_proveedores(request):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/proveedor_list.html', {'proveedores': proveedores})

@login_required
def crear_proveedor(request):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')

    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado exitosamente.')
            return redirect('proveedores:listar_proveedores')
        else:
            messages.error(request, 'Hay errores en el formulario. Revisa los campos.')
    else:
        form = ProveedorForm()

    return render(request, 'proveedores/proveedor_form.html', {'form': form, 'accion': 'Nuevo'})

@login_required
def editar_proveedor(request, pk):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')

    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado correctamente.')
            return redirect('proveedores:listar_proveedores')
        else:
            messages.error(request, 'Hay errores en el formulario. Revisa los campos.')
    else:
        form = ProveedorForm(instance=proveedor)

    return render(request, 'proveedores/proveedor_form.html', {'form': form, 'accion': 'Editar'})

@login_required
def eliminar_proveedor(request, pk):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')

    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.delete()
    messages.success(request, 'Proveedor eliminado exitosamente.')
    return redirect('proveedores:listar_proveedores')
