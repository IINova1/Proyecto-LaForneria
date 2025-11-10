from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# ¡Importamos Q para búsquedas!
from django.db.models import Q 
# ¡IMPORTAMOS EL PAGINADOR!
from django.core.paginator import Paginator

# --- ¡Importaciones Corregidas! ---
from .models import Pedido, DetallePedido, Cliente
from .forms import ClienteForm
# Importamos Producto desde la app 'catalogo'
from catalogo.models import Producto

# --------------------
# Vistas de la Tienda (Públicas)
# --------------------

def ver_productos(request):
    """
    Vista para que los clientes vean los productos disponibles.
    ¡CON FILTROS PERSISTENTES EN SESIÓN!
    """
    
    # 1. Definimos los defaults y las claves de sesión
    DEFAULT_SORT = 'alpha_asc'
    DEFAULT_PER_PAGE = 9 # El valor que tenías
    PER_PAGE_OPTIONS = [5, 9, 15, 30] # Opciones para el selector
    
    SESSION_KEY_Q = 'productos_q'
    SESSION_KEY_SORT = 'productos_sort'
    SESSION_KEY_PER_PAGE = 'productos_per_page'

    # --- Parámetro de Búsqueda 'q' ---
    # Si 'q' viene en la URL, lo usamos y lo guardamos en sesión.
    # Si no, usamos el valor de la sesión (o un string vacío).
    if 'q' in request.GET:
        search_query = request.GET.get('q', '')
        request.session[SESSION_KEY_Q] = search_query
    else:
        search_query = request.session.get(SESSION_KEY_Q, '')
        
    # --- Parámetro de Orden 'sort' ---
    # Si 'sort' viene en la URL, lo usamos y lo guardamos en sesión.
    # Si no, usamos el valor de la sesión (o el default).
    if 'sort' in request.GET:
        sort_by = request.GET.get('sort', DEFAULT_SORT)
        request.session[SESSION_KEY_SORT] = sort_by
    else:
        sort_by = request.session.get(SESSION_KEY_SORT, DEFAULT_SORT)

    # --- Parámetro de 'per_page' (Items por página) ---
    # Si 'per_page' viene en la URL, lo usamos y lo guardamos en sesión.
    # Si no, usamos el valor de la sesión (o el default).
    if 'per_page' in request.GET:
        try:
            per_page = int(request.GET.get('per_page', DEFAULT_PER_PAGE))
            if per_page not in PER_PAGE_OPTIONS:
                per_page = DEFAULT_PER_PAGE
        except ValueError:
            per_page = DEFAULT_PER_PAGE
        request.session[SESSION_KEY_PER_PAGE] = per_page
    else:
        per_page = request.session.get(SESSION_KEY_PER_PAGE, DEFAULT_PER_PAGE)

    # --- Parámetro de 'page' (No es persistente) ---
    # La página actual siempre se toma de la URL, nunca de la sesión.
    page_number = request.GET.get('page', 1)

    # 3. Empezamos con el queryset base
    productos_list = Producto.objects.filter(stock_actual__gt=0)

    # 4. Aplicamos el filtro de BÚSQUEDA si existe
    if search_query:
        productos_list = productos_list.filter(
            Q(nombre__icontains=search_query) |
            Q(descripcion__icontains=search_query)
        )

    # 5. Aplicamos el ORDENAMIENTO
    if sort_by == 'precio_asc':
        productos_list = productos_list.order_by('precio')
    elif sort_by == 'precio_desc':
        productos_list = productos_list.order_by('-precio')
    elif sort_by == 'alpha_desc':
        productos_list = productos_list.order_by('-nombre')
    else: # 'alpha_asc' o por defecto
        productos_list = productos_list.order_by('nombre')

    # 6. Aplicamos la Paginación (usando el valor 'per_page' de la sesión)
    paginator = Paginator(productos_list, per_page)
    
    try:
        # Obtenemos solo los productos para la página actual
        page_obj = paginator.get_page(page_number)
    except Exception: # (Cubre PageNotAnInteger y EmptyPage)
        page_obj = paginator.get_page(1)

    # 7. Pasamos todo al contexto
    context = {
        'page_obj': page_obj,
        'paginator': paginator,
        'current_q': search_query, # Pasa el valor (de URL o sesión)
        'current_sort': sort_by, # Pasa el valor (de URL o sesión)
        'current_per_page': per_page, # Pasa el valor (de URL o sesión)
        'per_page_options': PER_PAGE_OPTIONS, # Pasa las opciones para el <select>
    }
    
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'pedidos/ver_productos.html', context)


def agregar_al_carrito(request, pk):
    """
    Añade un producto al carrito de compras, que se guarda en la sesión.
    (Esta vista no necesita cambios)
    """
    # Usamos el modelo 'Producto' de la app 'catalogo'
    producto = get_object_or_404(Producto, pk=pk)
    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except (TypeError, ValueError):
        cantidad = 1
    carrito = request.session.get('carrito', {})
    
    if str(pk) in carrito:
        carrito[str(pk)] += cantidad
    else:
        carrito[str(pk)] = cantidad
    
    request.session['carrito'] = carrito
    
    messages.success(request, f'¡Producto "{producto.nombre}" agregado al carrito!')
    
    # --- REDIRECCIÓN CORREGIDA ---
    return redirect('pedidos:ver_carrito')

def ver_carrito(request):
    """
    Muestra el contenido del carrito de compras.
    (Esta vista no necesita cambios)
    """
    carrito = request.session.get('carrito', {})
    items_carrito = []
    total_carrito = 0
    for producto_id, cantidad in carrito.items():
        # Usamos el modelo 'Producto' de la app 'catalogo'
        producto = get_object_or_404(Producto, pk=producto_id)
        subtotal = producto.precio * cantidad
        items_carrito.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
        total_carrito += subtotal
    context = {'items_carrito': items_carrito, 'total_carrito': total_carrito}
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'pedidos/ver_carrito.html', context)

@login_required
def realizar_pedido(request):
    """
    Crea un pedido en la base de datos a partir del carrito y lo vacía.
    (Esta vista no necesita cambios)
    """
    carrito = request.session.get('carrito', {})
    if not carrito:
        # --- REDIRECCIÓN CORREGIDA ---
        return redirect('pedidos:ver_productos')
    total_pedido = 0
    items_para_pedido = []
    for producto_id, cantidad in carrito.items():
        # Usamos el modelo 'Producto' de la app 'catalogo'
        producto = get_object_or_404(Producto, pk=producto_id)
        total_pedido += producto.precio * cantidad
        items_para_pedido.append((producto, cantidad))
    
    # Usamos los modelos 'Pedido' y 'DetallePedido' de esta app
    pedido = Pedido.objects.create(usuario=request.user, total=total_pedido)
    for producto, cantidad in items_para_pedido:
        DetallePedido.objects.create(pedido=pedido, producto=producto, cantidad=cantidad, precio=producto.precio)
        producto.stock_actual -= cantidad
        producto.save() # Actualiza el stock en la app 'catalogo'
        
    request.session['carrito'] = {}
    # --- REDIRECCIÓN CORREGIDA ---
    return redirect('pedidos:pedido_exitoso')

def pedido_exitoso(request):
    """
    Muestra una página de confirmación después de un pedido exitoso.
    (Esta vista no necesita cambios)
    """
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'pedidos/pedido_exitoso.html')

# ----------------------------------------
# Vistas Protegidas (SOLO PARA ADMINS)
# (El resto de las vistas de admin (cliente_list, etc.) sigue igual)
# ----------------------------------------

# --- CRUD de Clientes ---
@login_required
def cliente_list(request):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    clientes = Cliente.objects.all()
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'pedidos/cliente_list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            # --- REDIRECCIÓN CORREGIDA ---
            return redirect('pedidos:cliente_list')
    else:
        form = ClienteForm()
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'pedidos/cliente_form.html', {'form': form})

@login_required
def cliente_update(request, pk):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            # --- REDIRECCIÓN CORREGIDA ---
            return redirect('pedidos:cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'pedidos/cliente_form.html', {'form': form})

@login_required
def cliente_delete(request, pk):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        # --- REDIRECCIÓN CORREGIDA ---
        return redirect('pedidos:cliente_list')
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'pedidos/cliente_confirm_delete.html', {'object': cliente})

# --- CRUD de Pedidos ---
@login_required
def pedido_list(request):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'pedidos/pedido_list.html', {'pedidos': pedidos})

@login_required
def pedido_detail(request, pk):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
    pedido = get_object_or_404(Pedido, pk=pk)
    for detalle in pedido.detalles.all():
        detalle.subtotal = detalle.cantidad * detalle.precio
    context = {'pedido': pedido}
    # --- RUTA DE PLANTILLA CORREGIDA ---
    return render(request, 'pedidos/pedido_detail.html', context)