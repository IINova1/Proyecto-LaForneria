from django.contrib import admin

#
# La app 'core' no es dueña de ningún modelo de base de datos.
# Su propósito es manejar vistas como 'inicio' y 'dashboard'.
#
# Los modelos se registran en las apps a las que pertenecen:
# - Usuario, Rol, Direccion se registran en 'usuarios/admin.py'
# - Producto, Categoria, Nutricional se registran en 'catalogo/admin.py'
# - Pedido, Cliente, Venta se registran en 'pedidos/admin.py'
#
# Por lo tanto, este archivo debe permanecer vacío.
#