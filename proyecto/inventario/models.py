from django.db import models

# Create your models here.
class inventario_objetos(models.Model):
    codigo_pddh = models.CharField(max_length=100)
    descripcion = models.TextField()
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    serie = models.CharField(max_length=100)
    fecha_adquisición = models.DateField()
    valor_unitario = models.DecimalField(max_digits=20, decimal_places=2)
    observaciones = models.TextField()

    def __str__(self):
        return self.codigo_pddh