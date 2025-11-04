from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = True # <-- ¡CORREGIDO!
        db_table = 'Categorias'
    def __str__(self):
        return self.nombre

class Nutricional(models.Model):
    ingredientes = models.CharField(max_length=300, blank=True, null=True)
    tiempo_preparacion = models.CharField(max_length=100, blank=True, null=True)
    proteinas = models.CharField(max_length=45, blank=True, null=True)
    azucar = models.CharField(max_length=45, blank=True, null=True)
    gluten = models.CharField(max_length=45, blank=True, null=True)
    class Meta:
        managed = True # <-- ¡CORREGIDO!
        db_table = 'Nutricional'
    def __str__(self):
        return f"ingredientes {self.id}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)
    caducidad = models.DateField()
    elaboracion = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=100)
    Categorias = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, db_column='Categorias_id')
    Nutricional = models.ForeignKey(Nutricional, on_delete=models.DO_NOTHING, db_column='Nutricional_id')
    stock_actual = models.IntegerField(blank=True, null=True)
    stock_minimo = models.IntegerField(blank=True, null=True)
    stock_maximo = models.IntegerField(blank=True, null=True)
    presentacion = models.CharField(max_length=100, blank=True, null=True)
    formato = models.CharField(max_length=100, blank=True, null=True)
    creado = models.DateTimeField(blank=True, null=True)
    modificado = models.DateTimeField(blank=True, null=True)
    eliminado = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True # <-- ¡CORREGIDO!
        db_table = 'Productos'
    def __str__(self):
        return self.nombre

class ReglaAlertaVencimiento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    dias_anticipacion = models.IntegerField()
    def __str__(self):
        return self.nombre

class ProductoReglaAlerta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    regla = models.ForeignKey(ReglaAlertaVencimiento, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('producto', 'regla')
    def __str__(self):
        return f"{self.producto.nombre} - {self.regla.nombre}"