from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# --- ¡Importaciones Añadidas! ---
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError # <-- ¡IMPORTANTE!

# --- ¡Importaciones Corregidas! ---
# Importamos los formularios y modelos desde la app local 'usuarios'
from .forms import (
    CustomRegisterForm, UserProfileForm, DireccionForm
)
from .models import Usuario, Direccion

# --------------------
# Vistas de Autenticación
# --------------------

def register(request):
    """
    Vista para el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        # --- ¡Corrección! Se añade request.FILES para el avatar ---
        form = CustomRegisterForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # --- ¡CORRECCIÓN! Ponemos el .save() dentro de un try ---
                # para atrapar el error del Rol si no existe.
                user = form.save()
                
                # Si .save() funciona, continuamos
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.first_name}! Tu cuenta ha sido creada.')
                # Redirige al nuevo usuario a la tienda
                return redirect('pedidos:ver_productos')

            except ValidationError as e:
                # --- ¡CORRECCIÓN! Si form.save() lanza el error,
                # lo atrapamos y lo añadimos a los non_field_errors
                # para que la plantilla lo muestre.
                form.add_error(None, e)
        
        # Si form.is_valid() fue Falso, o si form.save() falló,
        # la función continúa aquí, renderizando el 'form' con los errores.
        
    else:
        form = CustomRegisterForm()
    
    return render(request, 'usuarios/register.html', {'form': form})

# --- ¡NUEVA VISTA DE PERFIL! ---
@login_required
def perfil(request):
    """
    Vista para que el usuario vea y actualice sus datos personales y dirección.
    """
    usuario = request.user
    # Busca la dirección existente o usa None si no existe
    try:
        direccion = usuario.Direccion
    except Direccion.DoesNotExist:
        direccion = None

    if request.method == 'POST':
        # --- ¡Correcto! Se incluye request.FILES ---
        user_form = UserProfileForm(request.POST, request.FILES, instance=usuario)
        direccion_form = DireccionForm(request.POST, instance=direccion)
        
        if user_form.is_valid() and direccion_form.is_valid():
            user_form.save() # Guarda los cambios en el Usuario (ej. fono, materno)
            
            # Guarda la dirección
            nueva_direccion = direccion_form.save(commit=False)
            if direccion is None:
                # Si no había dirección, la crea y la asigna al usuario
                nueva_direccion.save()
                usuario.Direccion = nueva_direccion
                usuario.save()
            else:
                # Si ya existía, solo la guarda (actualiza)
                nueva_direccion.save()
            
            messages.success(request, '¡Tu perfil ha sido actualizado con éxito!')
            return redirect('usuarios:perfil')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')

    else:
        # En un GET, muestra los formularios con la data existente
        user_form = UserProfileForm(instance=usuario)
        direccion_form = DireccionForm(instance=direccion)

    context = {
        'user_form': user_form,
        'direccion_form': direccion_form
    }
    # Renderiza la plantilla de perfil
    return render(request, 'usuarios/perfil.html', context)


# ----------------------------------------
# Vistas Protegidas (SOLO PARA ADMINS)
# --- CRUD de Usuarios ---
# ----------------------------------------

@login_required
def usuario_list(request):
    """
    Vista para listar, buscar y paginar usuarios (SOLO STAFF).
    (Versión actualizada con filtro y paginación)
    """
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('pedidos:ver_productos')
    
    # Lógica de Búsqueda
    query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page', 1)

    # Queryset base
    usuarios_qs = Usuario.objects.all().order_by('first_name')

    if query:
        usuarios_qs = usuarios_qs.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(run__icontains=query)
        )

    # Lógica de Paginación
    paginator = Paginator(usuarios_qs, 10) # 10 usuarios por página
    page_obj = paginator.get_page(page_number)

    context = {
        'usuarios': page_obj, # Pasamos el objeto de página
        'query': query,
    }
    return render(request, 'usuarios/usuario_list.html', context)


@login_required
def usuario_create(request):
    """
    Vista para que un Admin cree un nuevo usuario (SOLO STAFF).
    """
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
        
    if request.method == 'POST':
        # --- ¡Corrección! Se añade request.FILES para el avatar ---
        form = CustomRegisterForm(request.POST, request.FILES) # Sigue usando el form de registro
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios:usuario_list')
    else:
        form = CustomRegisterForm()
        
    # 'es_admin' puede usarse en la plantilla para cambiar el título
    return render(request, 'usuarios/register.html', {'form': form, 'es_admin': True})

@login_required
def usuario_update(request, pk):
    """
    Vista para que un Admin edite un usuario (SOLO STAFF).
    """
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
        
    usuario = get_object_or_404(Usuario, pk=pk)
    
    # Los admins ahora usarán el UserProfileForm para editar
    if request.method == 'POST':
        # --- ¡Correcto! Se incluye request.FILES ---
        form = UserProfileForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuarios:usuario_list')
    else:
        form = UserProfileForm(instance=usuario)
        
    # Renderiza en una plantilla separada para no confundir con el perfil del admin
    return render(request, 'usuarios/perfil_admin_edit.html', {'form': form, 'usuario_editado': usuario})

@login_required
def usuario_delete(request, pk):
    """
    Vista para que un Admin elimine un usuario (SOLO STAFF).
    """
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
        
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        email_borrado = usuario.email
        usuario.delete()
        messages.success(request, f'Usuario {email_borrado} eliminado.')
        return redirect('usuarios:usuario_list')
        
    # Esta plantilla ya no se usará si SweetAlert está activo,
    # pero es buena práctica mantenerla.
    return render(request, 'usuarios/usuario_confirm_delete.html', {'object': usuario})