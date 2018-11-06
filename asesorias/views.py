
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from .models import User
from asesorias.models import Asesoria, Curso, Seccion, FactTable, Cita
from django.http import JsonResponse
import json
# Create your views here.




def mostrarCursos(request):
    agregar = 1
    tipo = 0
    curso = Curso.objects.all().order_by('id')

    return render(request, 'agregarAsesoria.html', locals())



def listarAsesoria(request):
    tipo = 0
    agregar = 0
    factTable = FactTable.objects.all().order_by("id")
    arreglo=[]

    for x in factTable:
        print(5)
        x_info = {}

        #CURSO
        curso= Curso.objects.filter(id=x.curso_id)
        for y in curso:
            x_info['curso'] = y.nombre

        #PROFESOR
        profesor=User.objects.filter(id=x.profesor_id)
        for y in profesor:
            x_info['profesor'] = y.first_name

        #ASESORIA
        asesoria=Asesoria.objects.filter(id=x.asesoria_id)
        for y in asesoria:
            x_info['id'] = y.id
            x_info['horario'] = y.horario
            x_info['dia'] = y.dia
            x_info['lugar'] = y.lugar

        #Seccion
        seccion=Seccion.objects.filter(id=x.seccion_id)
        for y in seccion:
            x_info['seccion'] = y.codigo

        arreglo.append(x_info)
    print(arreglo)

    return render(request, 'listarAsesoria.html', locals())

def eliminarAsesoria(request):
    tipo = 0
    agregar = 0
    id=request.POST.get('id_asesoria', False)
    asesoria=Asesoria.objects.filter(id=id)
    FactTable.objects.filter(asesoria=asesoria)
    asesoria.delete()
    return redirect('/listarAsesoria')

def editarAsesoria(request):
    id = int(request.GET.get('id'))
    tipo= 1
    agregar= 0
    listado = Asesoria.objects.all().order_by("id")
    return render(request, 'listarAsesoria.html', locals())

def guardarCambios(request):
    tipo = 0
    agregar = 0
    id=request.POST.get('id_asesoria', False)
    curso=request.POST['curso']
    profesor=request.POST['profesor']
    horario=request.POST['horario']
    lugar=request.POST['lugar']
    dia=request.POST['dia']
    asesoria= Asesoria.objects.get(id=id)
    asesoria.curso = curso
    asesoria.profesor = profesor
    asesoria.horario = horario
    asesoria.lugar = lugar
    asesoria.dia=dia
    asesoria.save()
    return redirect('/listarAsesoria')

def guardarAsesoria(request):
    tipo = 0
    agregar = 0
    curso=request.POST['curso']
    sv=request.POST['seccion']
    profesor=request.POST['profesor']
    horario=request.POST['horario']
    seccion=request.POST['seccion']
    dia=request.POST['dia']
    lugar=request.POST['lugar']
    #buscarProfesor=User.objects.filter(first_name__iexact=busqueda)
    #buscarSeccion=Seccion.objects.filter(codigo__iexact=busqueda)
        #codigo = models.AutoField()
        #dia
        #horario
        #lugar
        #seccion
        
    objCurso= Curso.objects.get(nombre=curso)
    arrProf=profesor.split(" ")
    objProf= User.objects.get(first_name=arrProf[0])
    objProf2= User.objects.get(last_name=arrProf[1])
    if objProf.id==objProf2.id:
        objSeccion=Seccion.objects.get(profesor=objProf.id,curso=objCurso.id,codigo=int(seccion))
    print(objCurso.id)
    print(profesor)
    print(objProf.id)
    print(objSeccion.id)
    print(lugar)

    asesoria = Asesoria.objects.create(dia=dia, horario=horario, lugar=lugar, seccion=objSeccion)

    asesoria.save()
    newAsesoria=asesoria
    print(newAsesoria)
    fact=FactTable.objects.create(curso=objCurso,profesor=objProf,asesoria=newAsesoria,seccion=objSeccion)
    fact.save()
    return redirect('/listarAsesoria')

def cancelar(request):
    tipo = 0
    agregar = 0
    return redirect('/listarAsesoria')

def salir(request):
    tipo = 0
    agregar = 0
    return render(request, 'registration/login.html')

def logout(request):
    request.session['id'] = ''
    return render(request, 'registration/login.html')
