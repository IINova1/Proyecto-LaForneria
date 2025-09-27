from django.shortcuts import render
from django.db import models
from .models import Producto, Categoria, Usuario, Cliente, Venta


# Dashboard
def dashboard(request):
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    total_usuarios = Usuario.objects.count()
    total_clientes = Cliente.objects.count()
    total_ventas = Venta.objects.count()

    return render(request, "dispositivos/dashboard.html", {
        "total_productos": total_productos,
        "total_categorias": total_categorias,
        "total_usuarios": total_usuarios,
        "total_clientes": total_clientes,
        "total_ventas": total_ventas,
    })


# Productos
def producto_list(request):
    productos = Producto.objects.all()
    return render(request, "dispositivos/productos_list.html", {"productos": productos})


# Categorías
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, "dispositivos/categorias_list.html", {"categorias": categorias})


# Usuarios
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, "dispositivos/usuarios_list.html", {"usuarios": usuarios})


# Clientes
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, "dispositivos/clientes_list.html", {"clientes": clientes})


# Ventas
def venta_list(request):
    ventas = Venta.objects.all()
    return render(request, "dispositivos/ventas_list.html", {"ventas": ventas})


# Alertas (productos con stock bajo el mínimo)
def alert_summary(request):
    productos_bajo_stock = Producto.objects.filter(stock_actual__lt=models.F('stock_minimo'))
    return render(request, "dispositivos/alertas.html", {"productos_bajo_stock": productos_bajo_stock})
