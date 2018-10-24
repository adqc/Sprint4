from django.db import models
#from django.contrib.auth.models import User
from accounts.models import User
# Create your models here.



class Curso(models.Model):
    #codigo = models.AutoField()
    nombre= models.CharField(max_length=255)
    creditos= models.IntegerField()
    nivel=models.IntegerField()


class Seccion(models.Model):
    codigo=models.IntegerField()
    curso=models.ForeignKey(Curso,on_delete=models.CASCADE)
    profesor=models.ForeignKey(User, on_delete=models.CASCADE)

class Asesoria(models.Model):
    #codigo = models.AutoField()
    dia= models.CharField(max_length=255)
    horario= models.CharField(max_length=255)
    lugar=models.CharField(max_length=255)
    seccion=models.ForeignKey(Seccion,on_delete=models.CASCADE,default='000')

class Cita(models.Model):
    asesoria=models.ForeignKey(Asesoria, on_delete=models.CASCADE)
    alumno=models.ForeignKey(User,on_delete=models.CASCADE)
    comentario=models.CharField(max_length=255, default='null')
    estado=models.BooleanField(default=True)
    archivo=models.CharField(max_length=255, default='null')
    feedback= models.CharField(max_length=255, default='null')

class FactTable(models.Model):
    curso=models.ForeignKey(Curso,on_delete=models.CASCADE, related_name = 'cursoFact')
    profesor=models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'profesorFact')
    asesoria=models.ForeignKey(Asesoria, on_delete=models.CASCADE, related_name = 'asesoriaFact')
    seccion=models.ForeignKey(Seccion,on_delete=models.CASCADE,default='000', related_name = 'seccionFact')
