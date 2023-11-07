from django.db import models
from usuarios.models import Usuario
from materiales.models import Material

# Create your models here.

class Reporte(models.Model):
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return f"Reporte de {self.producto.nombre_articulo} por {self.solicitante.username}"