from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomRegisterForm, ProductoForm, CategoriaForm,
    ClienteForm, VentaForm
)
# --- LÍNEA CORREGIDA ---
# Se importa el modelo 'Usuario' con su nombre correcto.
from .models import Usuario, Categoria, Producto, Cliente, Venta

# --------------------
# Vistas Públicas
# --------------------

def inicio(request):
    """
    Vista para la página de inicio pública.
    """
    return render(request, 'dispositivos/inicio.html')

def register(request):
    """
    Vista para el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dispositivos:dashboard')
    else:
        form = CustomRegisterForm()
    return render(request, 'dispositivos/register.html', {'form': form})

# --------------------
# Vistas Protegidas (Requieren Login)
# --------------------

@login_required
def dashboard(request):
    """
    Vista para el panel de control principal. Muestra estadísticas generales.
    """
    # Se utiliza el modelo 'Usuario' corregido
    total_usuarios = Usuario.objects.count()
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()
    total_ventas = Venta.objects.count()
    
    context = {
        'total_usuarios': total_usuarios,
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
    }
    return render(request, 'dispositivos/dashboard.html', context)


# --- CRUD de Usuarios ---
@login_required
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'dispositivos/usuario_list.html', {'usuarios': usuarios})

@login_required
def usuario_create(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:usuario_list')
    else:
        form = CustomRegisterForm()
    return render(request, 'dispositivos/register.html', {'form': form})

@login_required
def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:usuario_list')
    else:
        form = CustomRegisterForm(instance=usuario)
    return render(request, 'dispositivos/register.html', {'form': form})

@login_required
def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('dispositivos:usuario_list')
    return render(request, 'usuario_confirm_delete.html', {'object': usuario})


# --- CRUD de Categorías ---
@login_required
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'dispositivos/categoria_list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'categoria_form.html', {'form': form})

@login_required
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria_form.html', {'form': form})

@login_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('dispositivos:categoria_list')
    return render(request, 'categoria_confirm_delete.html', {'object': categoria})


# --- CRUD de Productos ---
@login_required
def producto_list(request):
    productos = Producto.objects.all()
    return render(request, 'dispositivos/producto_list.html', {'productos': productos})

@login_required
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'dispositivos/producto_detail.html', {'producto': producto})

@login_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:producto_list')
    else:
        form = ProductoForm()
    return render(request, 'dispositivos/producto_form.html', {'form': form})

@login_required
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:producto_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'dispositivos/producto_form.html', {'form': form})

@login_required
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('dispositivos:producto_list')
    return render(request, 'producto_confirm_delete.html', {'object': producto})


# --- CRUD de Clientes ---
@login_required
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'dispositivos/cliente_list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'cliente_form.html', {'form': form})

@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente_form.html', {'form': form})

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('dispositivos:cliente_list')
    return render(request, 'cliente_confirm_delete.html', {'object': cliente})


# --- CRUD de Ventas ---
@login_required
def venta_list(request):
    ventas = Venta.objects.all()
    return render(request, 'dispositivos/venta_list.html', {'ventas': ventas})

@login_required
def venta_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:venta_list')
    else:
        form = VentaForm()
    return render(request, 'venta_form.html', {'form': form})

@login_required
def venta_update(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:venta_list')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'venta_form.html', {'form': form})

@login_required
def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('dispositivos:venta_list')
    return render(request, 'venta_confirm_delete.html', {'object': venta})