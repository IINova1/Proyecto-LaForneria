from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

# --- ¡Importaciones Corregidas! ---
from .models import Categoria, Producto
from .forms import ProductoForm, CategoriaForm

# ----------------------------------------
# Vistas Protegidas (SOLO PARA ADMINS)
# ----------------------------------------

# --- CRUD de Categorías ---
@login_required
def categoria_list(request):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    categorias = Categoria.objects.all()
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'catalogo/categoria_list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            # --- REDIRECCIÓN CORREGIDA ---
            return redirect('catalogo:categoria_list')
    else:
        form = CategoriaForm()
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'catalogo/categoria_form.html', {'form': form})

@login_required
def categoria_update(request, pk):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            # --- REDIRECCIÓN CORREGIDA ---
            return redirect('catalogo:categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'catalogo/categoria_form.html', {'form': form})

@login_required
def categoria_delete(request, pk):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nombre_cat = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría {nombre_cat} eliminada.')
        # --- REDIRECCIÓN CORREGIDA ---
        return redirect('catalogo:categoria_list')
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'catalogo/categoria_confirm_delete.html', {'object': categoria})

# --- CRUD de Productos ---
@login_required
def producto_list(request):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    productos = Producto.objects.all()
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'catalogo/producto_list.html', {'productos': productos})

@login_required
def producto_detail(request, pk):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    producto = get_object_or_404(Producto, pk=pk)
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'catalogo/producto_detail.html', {'producto': producto})

@login_required
def producto_create(request):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.creado = timezone.now()
            producto.save()
            messages.success(request, 'Producto creado exitosamente.')
            # --- REDIRECCIÓN CORREGIDA ---
            return redirect('catalogo:producto_list')
    else:
        form = ProductoForm()
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'catalogo/producto_form.html', {'form': form})

@login_required
def producto_update(request, pk):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto_actualizado = form.save(commit=False)
            producto_actualizado.modificado = timezone.now()
            producto_actualizado.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            # --- REDIRECCIÓN CORREGIDA ---
            return redirect('catalogo:producto_list')
    else:
        form = ProductoForm(instance=producto)
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'catalogo/producto_form.html', {'form': form})

@login_required
def producto_delete(request, pk):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre_prod = producto.nombre
        producto.delete()
        messages.success(request, f'Producto {nombre_prod} eliminado.')
        # --- REDIRECCIÓN CORREGIDA ---
        return redirect('catalogo:producto_list')
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'catalogo/producto_confirm_delete.html', {'object': producto})