from django import forms

#
# La app 'core' no es dueña de ningún formulario.
#
# Los formularios se han movido a las apps correspondientes:
# - CustomRegisterForm y CustomLoginForm están en 'usuarios/forms.py'
# - ProductoForm y CategoriaForm están en 'catalogo/forms.py'
# - ClienteForm y VentaForm están en 'pedidos/forms.py'
#
# Por lo tanto, este archivo debe permanecer vacío.
#