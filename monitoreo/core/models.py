from django.db import models

#
# La app 'core' se encarga de las vistas principales como el inicio y el dashboard.
# Estas vistas "consultan" modelos de otras apps (como 'usuarios' o 'catalogo'),
# pero la app 'core' NO es "dueña" de ningún modelo.
#
# Por lo tanto, este archivo models.py debe permanecer vacío.
#