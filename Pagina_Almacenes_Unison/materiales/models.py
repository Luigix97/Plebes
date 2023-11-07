from django.db import models

# Create your models here.

class Material(models.Model):
    
    nombre_articulo = models.CharField(max_length=50)
    precio_unitario = models.DecimalField(max_digits=10,decimal_places=2)
    class Categoria_Material(models.TextChoices):
        ELECTRICO = 'Electrico'
        PLOMERIA = 'Plomeria'
        LIMPIEZA = 'Limpieza'
        OFICINA = 'Oficina'
    categoria = models.CharField(max_length=10, choices=Categoria_Material.choices)
    cantidad = models.IntegerField()
    imagen = models.ImageField(upload_to='material/', blank=True, null=True)
    descripcion = models.CharField(max_length=100,blank=True, null=True)
    cantidad_limite = models.IntegerField()
    class Origen_Producto(models.TextChoices):
        UNISON   = 'Unison'
        EXTERIOR = 'Exterior'
    Origen = models.CharField(max_length=8,choices = Origen_Producto.choices)

    def __str__(self):
        return self.nombre_articulo

