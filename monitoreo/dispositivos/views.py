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

    # Filtros
    device_id = request.GET.get('device')
    zone_id = request.GET.get('zone')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    measurements = Measurement.objects.filter(organization=org).order_by('-timestamp')

    if device_id:
        measurements = measurements.filter(device_id=device_id)

    if zone_id:
        measurements = measurements.filter(device__zone_id=zone_id)

    if start_date:
        measurements = measurements.filter(timestamp__gte=start_date)

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