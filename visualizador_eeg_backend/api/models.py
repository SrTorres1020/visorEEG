from django.db import models

class Paciente(models.Model):
    nombre_paciente = models.CharField(max_length=30)
    enfermedad = models.ForeignKey('Enfermedad', on_delete=models.CASCADE)

class Enfermedad(models.Model):
    descripcion = models.CharField(max_length=30)

class Sesion(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    fecha_sesion = models.DateTimeField()
    intervalo = models.DecimalField(max_digits=8, decimal_places=6)


class Canal(models.Model):
    nombre_canal = models.CharField(max_length=10)
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)

class Frecuencia(models.Model):
    frecuencia = models.FloatField()
    canal = models.ForeignKey(Canal, on_delete=models.CASCADE)
