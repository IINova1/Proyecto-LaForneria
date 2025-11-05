# Contenido COMPLETO para: Proyecto-LaForneria/monitoreo/usuarios/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    Vista para el registro de nuevos usuarios (Ahora simplificada).
    """
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.first_name}! Tu cuenta ha sido creada.')
            # Redirige al nuevo usuario a la tienda
            return redirect('pedidos:ver_productos')
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
        # --- ¡CAMBIO AQUÍ! Se añade request.FILES ---
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
    # Renderiza la nueva plantilla que crearemos en el siguiente paso
    return render(request, 'usuarios/perfil.html', context)


# ----------------------------------------
# Vistas Protegidas (SOLO PARA ADMINS)
# --- CRUD de Usuarios ---
# (El resto de las vistas de admin (usuario_list, etc.) sigue igual)
# ----------------------------------------

@login_required
def usuario_list(request):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
        
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/usuario_list.html', {'usuarios': usuarios})

@login_required
def usuario_create(request):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
        
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST) # Sigue usando el form de registro
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios:usuario_list')
    else:
        form = CustomRegisterForm()
        
    return render(request, 'usuarios/register.html', {'form': form}) 

@login_required
def usuario_update(request, pk):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
        
    usuario = get_object_or_404(Usuario, pk=pk)
    
    # Los admins ahora usarán el UserProfileForm para editar
    if request.method == 'POST':
        # --- ¡CAMBIO AQUÍ! Se añade request.FILES ---
        form = UserProfileForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuarios:usuario_list')
    else:
        form = UserProfileForm(instance=usuario)
        
    # Renderiza en la plantilla de perfil, pero podría tener una propia
    return render(request, 'usuarios/perfil_admin_edit.html', {'form': form, 'usuario_editado': usuario}) 

@login_required
def usuario_delete(request, pk):
    if not request.user.is_staff:
        return redirect('pedidos:ver_productos')
        
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        email_borrado = usuario.email
        usuario.delete()
        messages.success(request, f'Usuario {email_borrado} eliminado.')
        return redirect('usuarios:usuario_list')
        
    return render(request, 'usuarios/usuario_confirm_delete.html', {'object': usuario})