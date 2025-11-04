import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction

# --- IMPORTACIÓN CORREGIDA ---
# Importa directamente desde la app 'catalogo'
from catalogo.models import Nutricional, Categoria, Producto, ReglaAlertaVencimiento, ProductoReglaAlerta

class Command(BaseCommand):
    help = 'Carga los datos iniciales de catálogos de productos y alertas.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Iniciando la siembra de datos..."))
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Sube 3 niveles (commands -> management -> catalogo) y luego baja a 'fixtures'
        fixtures_dir = os.path.join(base_dir, '..', '..', 'fixtures')
        
        files = [
            '00_nutricional.json',
            '01_categorias_productos.json',
            '02_reglas_alerta.json',
            '03_productos_reglas.json',
        ]

        with transaction.atomic():
            for filename in files:
                file_path = os.path.join(fixtures_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.process_fixture_data(data)
                        self.stdout.write(self.style.SUCCESS(f"✔ Datos de {filename} cargados correctamente."))
                except FileNotFoundError:
                    self.stdout.write(self.style.ERROR(f"✖ Archivo {filename} no encontrado en {file_path}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"✖ Error al procesar {filename}: {e}"))

        self.stdout.write(self.style.SUCCESS("\n¡Siembra de datos completada!"))

    def process_fixture_data(self, data):
        # --- LÓGICA SIMPLIFICADA Y CORREGIDA ---
        for item in data:
            model_name = item['model'].split('.')[-1].lower()
            fields = item['fields']
            pk = item.get('pk')

            if model_name == 'nutricional':
                Nutricional.objects.create(pk=pk, **fields)
            elif model_name == 'categoria':
                Categoria.objects.create(pk=pk, **fields)
            elif model_name == 'producto':
                fields['Categorias_id'] = fields.pop('Categorias')
                fields['Nutricional_id'] = fields.pop('Nutricional')
                Producto.objects.create(pk=pk, **fields)
            elif model_name == 'reglaalertavencimiento':
                ReglaAlertaVencimiento.objects.create(pk=pk, **fields)
            elif model_name == 'productoreglaalerta':
                producto = Producto.objects.get(pk=fields['producto'])
                regla = ReglaAlertaVencimiento.objects.get(pk=fields['regla'])
                ProductoReglaAlerta.objects.create(producto=producto, regla=regla)