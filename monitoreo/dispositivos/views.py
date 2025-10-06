from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Pedido, DetallePedido

# Se eliminaron 'VentaForm' y 'Venta' de las importaciones
from .forms import (
    CustomRegisterForm, ProductoForm, CategoriaForm,
    ClienteForm, CustomLoginForm
)
from .models import Usuario, Categoria, Producto, Cliente
from datetime import date, timedelta
from django.utils import timezone

# --------------------
# Vistas Públicas (Para todos)
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
            # Redirige al nuevo usuario a la tienda, no al dashboard
            return redirect('dispositivos:ver_productos')
    else:
        form = CustomRegisterForm()
    return render(request, 'dispositivos/register.html', {'form': form})

def ver_productos(request):
    """
    Vista para que los clientes vean los productos disponibles.
    """
    productos = Producto.objects.filter(stock_actual__gt=0)
    return render(request, 'dispositivos/ver_productos.html', {'productos': productos})

def agregar_al_carrito(request, pk):
    """
    Añade un producto al carrito de compras, que se guarda en la sesión.
    """
    producto = get_object_or_404(Producto, pk=pk)
    cantidad = int(request.POST.get('cantidad', 1))
    carrito = request.session.get('carrito', {})
    if str(pk) in carrito:
        carrito[str(pk)] += cantidad
    else:
        carrito[str(pk)] = cantidad
    request.session['carrito'] = carrito
    return redirect('dispositivos:ver_carrito')

def ver_carrito(request):
    """
    Muestra el contenido del carrito de compras.
    """
    carrito = request.session.get('carrito', {})
    items_carrito = []
    total_carrito = 0
    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, pk=producto_id)
        subtotal = producto.precio * cantidad
        items_carrito.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
        total_carrito += subtotal
    context = {'items_carrito': items_carrito, 'total_carrito': total_carrito}
    return render(request, 'dispositivos/ver_carrito.html', context)

@login_required
def realizar_pedido(request):
    """
    Crea un pedido en la base de datos a partir del carrito y lo vacía.
    """
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('dispositivos:ver_productos')
    total_pedido = 0
    items_para_pedido = []
    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, pk=producto_id)
        total_pedido += producto.precio * cantidad
        items_para_pedido.append((producto, cantidad))
    pedido = Pedido.objects.create(usuario=request.user, total=total_pedido)
    for producto, cantidad in items_para_pedido:
        DetallePedido.objects.create(pedido=pedido, producto=producto, cantidad=cantidad, precio=producto.precio)
        producto.stock_actual -= cantidad
        producto.save()
    request.session['carrito'] = {}
    return redirect('dispositivos:pedido_exitoso')

def pedido_exitoso(request):
    """
    Muestra una página de confirmación después de un pedido exitoso.
    """
    return render(request, 'dispositivos/pedido_exitoso.html')

# ----------------------------------------
# Vistas Protegidas (SOLO PARA ADMINS)
# ----------------------------------------

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    
    total_usuarios = Usuario.objects.count()
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()
    total_pedidos = Pedido.objects.count()
    hoy = date.today()
    fecha_limite = hoy + timedelta(days=7)
    productos_a_vencer = Producto.objects.filter(caducidad__gte=hoy, caducidad__lte=fecha_limite).order_by('caducidad')
    context = {
        'total_usuarios': total_usuarios,
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_pedidos': total_pedidos,
        'productos_a_vencer': productos_a_vencer,
    }
    return render(request, 'dispositivos/dashboard.html', context)

# --- CRUD de Usuarios ---
@login_required
def usuario_list(request):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    usuarios = Usuario.objects.all()
    return render(request, 'dispositivos/usuario_list.html', {'usuarios': usuarios})

@login_required
def usuario_create(request):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
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
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
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
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('dispositivos:usuario_list')
    return render(request, 'usuario_confirm_delete.html', {'object': usuario})

# --- CRUD de Categorías ---
@login_required
def categoria_list(request):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    categorias = Categoria.objects.all()
    return render(request, 'dispositivos/categoria_list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
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
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
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
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('dispositivos:categoria_list')
    return render(request, 'categoria_confirm_delete.html', {'object': categoria})

# --- CRUD de Productos ---
@login_required
def producto_list(request):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    productos = Producto.objects.all()
    return render(request, 'dispositivos/producto_list.html', {'productos': productos})

@login_required
def producto_detail(request, pk):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'dispositivos/producto_detail.html', {'producto': producto})

@login_required
def producto_create(request):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.creado = timezone.now()
            producto.save()
            return redirect('dispositivos:producto_list')
    else:
        form = ProductoForm()
    return render(request, 'dispositivos/producto_form.html', {'form': form})

@login_required
def producto_update(request, pk):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto_actualizado = form.save(commit=False)
            producto_actualizado.modificado = timezone.now()
            producto_actualizado.save()
            return redirect('dispositivos:producto_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'dispositivos/producto_form.html', {'form': form})

@login_required
def producto_delete(request, pk):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('dispositivos:producto_list')
    return render(request, 'producto_confirm_delete.html', {'object': producto})

# --- CRUD de Clientes ---
@login_required
def cliente_list(request):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    clientes = Cliente.objects.all()
    return render(request, 'dispositivos/cliente_list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
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
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
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
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('dispositivos:cliente_list')
    return render(request, 'cliente_confirm_delete.html', {'object': cliente})

# --- CRUD de Pedidos ---
@login_required
def pedido_list(request):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    return render(request, 'dispositivos/pedido_list.html', {'pedidos': pedidos})

@login_required
def pedido_detail(request, pk):
    if not request.user.is_staff:
        return redirect('dispositivos:ver_productos')
    pedido = get_object_or_404(Pedido, pk=pk)
    for detalle in pedido.detalles.all():
        detalle.subtotal = detalle.cantidad * detalle.precio
    context = {'pedido': pedido}
    return render(request, 'dispositivos/pedido_detail.html', context)