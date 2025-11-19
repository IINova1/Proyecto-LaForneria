from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import IntegrityError
from .models import Proveedor
from .forms import ProveedorForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('proveedores.view_proveedor', raise_exception=True)
def listar_proveedores(request):

    # --- Búsqueda y filtro ---
    query = request.GET.get('q', '').strip()
    rubro_filtro = request.GET.get('rubro', '').strip()

    proveedores_list = Proveedor.objects.all()

    if query:
        proveedores_list = proveedores_list.filter(
            Q(nombre_empresa__icontains=query) | Q(rut__icontains=query)
        )

    if rubro_filtro:
        proveedores_list = proveedores_list.filter(rubro__iexact=rubro_filtro)

    # --- Paginación ---
    paginator = Paginator(proveedores_list, 10)
    page_number = request.GET.get('page')
    proveedores = paginator.get_page(page_number)

    # --- Rubros disponibles ---
    rubros = (
        Proveedor.objects.values_list('rubro', flat=True)
        .exclude(rubro__isnull=True)
        .exclude(rubro__exact='')
        .distinct()
        .order_by('rubro')
    )

    context = {
        'proveedores': proveedores,
        'query': query,
        'rubros': rubros,
        'rubro_filtro': rubro_filtro,
    }
    return render(request, 'proveedores/proveedor_list.html', context)


@login_required
@permission_required('proveedores.add_proveedor', raise_exception=True) # <-- Revisa si el usuario está en el grupo "Editor" o "Administrador"
def crear_proveedor(request):
    # --- Detectar rubro preseleccionado desde el filtro ---
    rubro_inicial = request.GET.get('rubro', '').strip()

    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, '✅ Proveedor creado exitosamente.')
                return redirect('proveedores:listar_proveedores')
            except IntegrityError:
                messages.error(request, '❌ Error al guardar. Verifica que los datos no estén duplicados.')
        else:
            messages.error(request, '⚠️ Hay errores en el formulario. Revisa los campos.')
    else:
        # Preasigna el rubro si existe
        form = ProveedorForm(initial={'rubro': rubro_inicial} if rubro_inicial else None)

    return render(request, 'proveedores/proveedor_form.html', {'form': form, 'accion': 'Nuevo'})


@login_required
@permission_required('proveedores.change_proveedor', raise_exception=True)
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, '✅ Proveedor actualizado correctamente.')
                return redirect('proveedores:listar_proveedores')
            except IntegrityError:
                messages.error(request, '❌ Error al actualizar. Datos duplicados o inválidos.')
        else:
            messages.error(request, '⚠️ Hay errores en el formulario. Revisa los campos.')
    else:
        form = ProveedorForm(instance=proveedor)

    return render(request, 'proveedores/proveedor_form.html', {'form': form, 'accion': 'Editar'})


@login_required
@permission_required('proveedores.delete_proveedor', raise_exception=True)
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    try:
        proveedor.delete()
        messages.success(request, '✅ Proveedor eliminado exitosamente.')
    except IntegrityError:
        messages.error(request, '❌ No se puede eliminar el proveedor porque está vinculado a otros registros.')

    return redirect('proveedores:listar_proveedores')
