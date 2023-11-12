from django.db import models

# Create your models here.

class Material(models.Model):
    nombre_articulo = models.CharField('Nombre de artículo',max_length=50)
    precio_unitario = models.DecimalField('Precio unitario',max_digits=10,decimal_places=2)
    class Categoria_Material(models.TextChoices):
        ELECTRICO = 'Electrico'
        PLOMERIA = 'Plomeria'
        LIMPIEZA = 'Limpieza'
        OFICINA = 'Oficina'
    categoria = models.CharField('Categoría',max_length=10, choices=Categoria_Material.choices)
    cantidad = models.IntegerField('Cantidad')
    imagen = models.ImageField('Imagen')
    descripcion = models.CharField('Descripción',max_length=100,blank=True, null=True)
    umbral = models.IntegerField('Umbral mínimo')
    class Origen_Producto(models.TextChoices):
        UNISON   = 'Unison'
        EXTERIOR = 'Exterior'
    Origen = models.CharField('Origen', max_length=8,choices = Origen_Producto.choices)

    def __str__(self):
        return self.nombre_articulo

class Gasto(models.Model):
    producto = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="Material", ) 
    cantidad = models.IntegerField('Cantidad')
    gasto = models.DecimalField('Gasto',decimal_places=2, max_digits=5)
    fecha = models.DateField('Fecha de gasto',auto_now=True)
