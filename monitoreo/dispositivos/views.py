<<<<<<< Updated upstream
from django.shortcuts import render, redirect, get_object_or_404
from .models import Device, Measurement, Alert, Category, Zone
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomRegisterForm, DispositivoForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# ----------------------------------------------------------------------
# VISTAS DE AUTENTICACIÓN
# ----------------------------------------------------------------------

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirige al panel después del registro exitoso
            return redirect('dashboard')
    else:
        form = CustomRegisterForm()
    return render(request, 'dispositivos/register.html', {'form': form})

def inicio(request):
    """Página de inicio pública."""
    return render(request, 'dispositivos/inicio.html')


# ----------------------------------------------------------------------
# VISTAS PROTEGIDAS (REQUIEREN @login_required)
# ----------------------------------------------------------------------

@login_required
def dashboard(request):
    org = request.user.organization

    # Filtros GET
    category_id = request.GET.get('category')
    zone_id = request.GET.get('zone')
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    # Base queryset de dispositivos
    devices = Device.objects.filter(organization=org)

    # Aplicar filtros de organización/usuario
    if category_id and category_id.isdigit():
        if Category.objects.filter(id=category_id, organization=org).exists():
            devices = devices.filter(category_id=int(category_id))

    if zone_id and zone_id.isdigit():
        if Zone.objects.filter(id=zone_id, organization=org).exists():
            devices = devices.filter(zone_id=int(zone_id))

    # Mediciones filtradas por dispositivos y fechas
    measurements = Measurement.objects.filter(
        organization=org,
        device__in=devices
    )
    if from_date:
        measurements = measurements.filter(timestamp__gte=from_date)
    if to_date:
        measurements = measurements.filter(timestamp__lte=to_date)
    recent_measurements = measurements.order_by('-timestamp')[:10]

    # Alertas filtradas por dispositivos y fechas
    alerts = Alert.objects.filter(
        organization=org,
        measurement__device__in=devices
    )
    if from_date:
        alerts = alerts.filter(timestamp__gte=from_date)
    if to_date:
        alerts = alerts.filter(timestamp__lte=to_date)
    recent_alerts = alerts.order_by('-timestamp')[:10]

    # Alertas de la semana
    one_week_ago = timezone.now() - timedelta(days=7)
    weekly_alerts = alerts.filter(timestamp__gte=one_week_ago).values('status').annotate(count=Count('id'))

    # Conteo por categoría y zona
    category_counts = devices.values('category__name').annotate(count=Count('id'))
    zone_counts = devices.values('zone__name').annotate(count=Count('id'))

    # Listado de categorías y zonas para los filtros
    categories = Category.objects.filter(organization=org)
    zones = Zone.objects.filter(organization=org)

    context = {
        'recent_measurements': recent_measurements,
        'category_counts': category_counts,
        'zone_counts': zone_counts,
        'weekly_alerts': weekly_alerts,
        'recent_alerts': recent_alerts,
        'devices': devices,
        'categories': categories,
        'zones': zones,
    }
    return render(request, 'dispositivos/dashboard.html', context)


@login_required
def device_list(request):
    org = request.user.organization
    category_id = request.GET.get('category')
    categories = Category.objects.filter(organization=org)

    devices = Device.objects.filter(organization=org)

    # Aplicar filtro de categoría si es válido
    if category_id and category_id.isdigit():
        if Category.objects.filter(id=category_id, organization=org).exists():
            devices = devices.filter(category_id=int(category_id))

    return render(request, 'dispositivos/device_list.html', {
        'devices': devices,
        'categories': categories
    })


@login_required    
def device_detail(request, device_id):
    org = request.user.organization
    # Asegura que el dispositivo pertenece a la organización del usuario
    device = get_object_or_404(Device, id=device_id, organization=org)
    measurements = Measurement.objects.filter(device=device).order_by('-timestamp')
    alerts = Alert.objects.filter(measurement__device=device).order_by('-timestamp')

    return render(request, 'dispositivos/device_detail.html', {
        'device': device,
        'measurements': measurements,
        'alerts': alerts
    })


@login_required
def measurement_list(request):
    org = request.user.organization
=======
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
>>>>>>> Stashed changes

    # Filtros
    device_id = request.GET.get('device')
    zone_id = request.GET.get('zone')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

<<<<<<< Updated upstream
    measurements = Measurement.objects.filter(organization=org).order_by('-timestamp')
=======
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
>>>>>>> Stashed changes

    if device_id:
        measurements = measurements.filter(device_id=device_id)

<<<<<<< Updated upstream
    if zone_id:
        measurements = measurements.filter(device__zone_id=zone_id)
=======
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
>>>>>>> Stashed changes

    if start_date:
        measurements = measurements.filter(timestamp__gte=start_date)

<<<<<<< Updated upstream
    if end_date:
        measurements = measurements.filter(timestamp__lte=end_date)

    paginator = Paginator(measurements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    devices = Device.objects.filter(organization=org)
    zones = Zone.objects.filter(organization=org)

    return render(request, 'dispositivos/measurement_list.html', {
        'page_obj': page_obj,
        'devices': devices,
        'zones': zones,
        'filters': {
            'device': device_id,
            'zone': zone_id,
            'start_date': start_date,
            'end_date': end_date
        }
    })

@login_required
def alert_summary(request):
    org = request.user.organization
    one_week_ago = timezone.now() - timedelta(days=7)

    alerts = Alert.objects.filter(organization=org)


    reviewed_count = alerts.filter(reviewed=True).count()
    pending_count = alerts.filter(reviewed=False).count()

    severity_counts = alerts.values('status').annotate(count=Count('id'))

    recent_alerts = alerts.order_by('-timestamp')[:10]

    return render(request, 'dispositivos/alerts_summary.html', {
        'reviewed_count': reviewed_count,
        'pending_count': pending_count,
        'severity_counts': severity_counts,
        'recent_alerts': recent_alerts
    })



@login_required
def device_add(request):
    org = request.user.organization
    
    if request.method == 'POST':
        form = DispositivoForm(request.POST, request.FILES) 
        if form.is_valid():
            new_device = form.save(commit=False)
            new_device.organization = org
            new_device.save()
            return redirect('device_list')
    else:
        form = DispositivoForm(initial={'organization': org.id})
    
    form.fields['category'].queryset = Category.objects.filter(organization=org)
    form.fields['zone'].queryset = Zone.objects.filter(organization=org)
    form.fields['organization'].initial = org

    return render(request, 'dispositivos/device_form.html', {'form': form})

@login_required
def device_edit(request, device_id):
    org = request.user.organization
    device = get_object_or_404(Device, id=device_id, organization=org)
    
    if request.method == 'POST':
        form = DispositivoForm(request.POST, request.FILES, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_list')
    else:
        form = DispositivoForm(instance=device)
    form.fields['category'].queryset = Category.objects.filter(organization=org)
    form.fields['zone'].queryset = Zone.objects.filter(organization=org)
    
    return render(request, 'dispositivos/device_form.html', {'form': form})

@login_required
def device_delete(request, device_id):
    org = request.user.organization
    device = get_object_or_404(Device, id=device_id, organization=org)
    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    return render(request, 'dispositivos/device_confirm_delete.html', {'device': device})

def api_dispositivos(request):
    """Endpoint que devuelve un listado de dispositivos en formato JSON."""

    data = list(Device.objects.values('id', 'name', 'max_consumption', 'status', 'category__name', 'zone__name'))
    return JsonResponse({'devices': data})
=======
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
>>>>>>> Stashed changes
