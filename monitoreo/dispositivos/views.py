from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from .forms import (
    CustomRegisterForm, ProductoForm, CategoriaForm,
    ClienteForm, VentaForm
)
from .models import CustomUser, Categoria, Producto, Cliente, Venta

# --------------------
# Inicio y Dashboard
# --------------------
def inicio(request):
    total_usuarios = CustomUser.objects.count()
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()
    total_ventas = Venta.objects.count()
    ultimas_ventas = Venta.objects.order_by('-fecha')[:5]

    context = {
        'total_usuarios': total_usuarios,
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
        'ultimas_ventas': ultimas_ventas,
    }
    return render(request, 'dispositivos/inicio.html', context)

def dashboard(request):
    total_usuarios = CustomUser.objects.count()
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()
    total_ventas = Venta.objects.count()
    ultimas_ventas = Venta.objects.order_by('-fecha')[:5]
    ultimos_clientes = Cliente.objects.order_by('-id')[:5]

    context = {
        'total_usuarios': total_usuarios,
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
        'ultimas_ventas': ultimas_ventas,
        'ultimos_clientes': ultimos_clientes,
    }
    return render(request, 'dispositivos/dashboard.html', context)


# --------------------
# Registro de usuario
# --------------------
def register(request):
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
# Usuarios
# --------------------
def usuario_list(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'dispositivos/usuario_list.html', {'usuarios': usuarios})

def usuario_create(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:usuario_list')
    else:
        form = CustomRegisterForm()
    return render(request, 'dispositivos/register.html', {'form': form})

def usuario_update(request, pk):
    usuario = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:usuario_list')
    else:
        form = CustomRegisterForm(instance=usuario)
    return render(request, 'dispositivos/register.html', {'form': form})

def usuario_delete(request, pk):
    usuario = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('dispositivos:usuario_list')
    return render(request, 'dispositivos/usuario_confirm_delete.html', {'usuario': usuario})


# --------------------
# Categorías
# --------------------
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'dispositivos/categoria_list.html', {'categorias': categorias})

def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'dispositivos/categoria_form.html', {'form': form})

def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'dispositivos/categoria_form.html', {'form': form})

def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('dispositivos:categoria_list')
    return render(request, 'dispositivos/categoria_confirm_delete.html', {'categoria': categoria})


# --------------------
# Productos
# --------------------
def producto_list(request):
    productos = Producto.objects.all()
    return render(request, 'dispositivos/producto_list.html', {'productos': productos})

def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'dispositivos/producto_detail.html', {'producto': producto})

def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:producto_list')
    else:
        form = ProductoForm()
    return render(request, 'dispositivos/producto_form.html', {'form': form})

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

def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('dispositivos:producto_list')
    return render(request, 'dispositivos/producto_confirm_delete.html', {'producto': producto})


# --------------------
# Clientes
# --------------------
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'dispositivos/cliente_list.html', {'clientes': clientes})

def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'dispositivos/cliente_form.html', {'form': form})

def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'dispositivos/cliente_form.html', {'form': form})

def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('dispositivos:cliente_list')
    return render(request, 'dispositivos/cliente_confirm_delete.html', {'cliente': cliente})


# --------------------
# Ventas
# --------------------
def venta_list(request):
    ventas = Venta.objects.all()
    return render(request, 'dispositivos/venta_list.html', {'ventas': ventas})

def venta_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:venta_list')
    else:
        form = VentaForm()
    return render(request, 'dispositivos/venta_form.html', {'form': form})

def venta_update(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('dispositivos:venta_list')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'dispositivos/venta_form.html', {'form': form})

def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('dispositivos:venta_list')
    return render(request, 'dispositivos/venta_confirm_delete.html', {'venta': venta})