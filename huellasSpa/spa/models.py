# spa/models.py
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=300)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    categoria = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre
