from django.db import models

class UserActivity(models.Model):
    username = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')])
    activity_data = models.TextField()

    def __str__(self):
        return f"{self.username} - {self.activity_data}"
  
# actividades/models.py

from django.db import models

# actividades/models.py
from django.db import models


class Resultado(models.Model):
    usuario = models.CharField(max_length=100)
    actividad = models.CharField(max_length=100)
    respuesta = models.TextField(default='')  # Valor por defecto definido
    puntaje = models.FloatField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    estado_correccion = models.CharField(max_length=50, default='pendiente')
    ventana_perdida = models.IntegerField(default=0)
    detalles = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.usuario} - {self.actividad}"


class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    grado = models.CharField(max_length=10)
    # otros campos...

    def __str__(self):
        return self.nombre



class Actividad(models.Model):
    ACTIVIDAD_CHOICES = [
        ('Sistema de numeración', 'Sistema de numeración'),
    ]
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    actividad = models.CharField(max_length=100, choices=ACTIVIDAD_CHOICES)
    estado_correccion = models.CharField(max_length=20, default='pendiente')
    puntaje = models.IntegerField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    corregido_por = models.CharField(max_length=100, null=True, blank=True)
    ventana_perdida = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.estudiante.nombre} - {self.actividad}'
