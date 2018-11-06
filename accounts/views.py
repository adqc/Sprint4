from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User
from asesorias.models import Asesoria, Curso, Seccion, FactTable, Cita
from django.http import JsonResponse
import json
import cloudinary.api
import cloudinary.uploader
from datetime import date, timedelta



cloudinary.config(
  cloud_name = "dcmdp3lbl",
  api_key = "322921397444291",
  api_secret = "cYxPSGxHfzbGqA3UK6QcBKShChw"
)

def mostrarFechas(year,dia):
    arrFechas=[]
    dt = date(year, 8, 13)
    #dt = date(13, 8, year)
    dt += timedelta(days = dia - dt.weekday())
    while dt.year == year:
      #yield dt
      arrFechas.append(dt)
      dt += timedelta(days = 7)
    return arrFechas

def index(request):
    tipo = 0
    agregar = 0
    return render(request, 'registration/login.html')

def registro(request):
    return render(request, 'registration/registro.html')

def register(request):
    a=request.POST['last_name']
    print(a)
    errors = User.objects.validator(request.POST)
    #print(len(errors))
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/registro')

    #hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    hashed_password = request.POST['password']
    tipoUsuario=request.POST['tipoUsuario']
    print(type(tipoUsuario))
    is_profesor=False
    is_estudiante=False
    is_admin=False
    if tipoUsuario == "profesor":
        is_profesor= True
    elif tipoUsuario == "estudiante":
        is_estudiante= True
    else:
        is_admin=True

    user = User.objects.create(is_profesor=is_profesor,is_estudiante=is_estudiante,is_admin=is_admin,first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=hashed_password, email=request.POST['email'])
    user.save()
    request.session['id'] = user.id
    return redirect('/')

def login(request):
    if (User.objects.filter(email=request.POST['login_email']).exists()):
        user = User.objects.filter(email=request.POST['login_email'])[0]

        #if (bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode())):
        if request.POST['login_password'] == user.password:
            request.session['id'] = user.id
            agregar = 0
            tipo = 0
            if user.is_admin== True:
                return redirect('/listarAsesoria')

            elif user.is_estudiante== True:
                return redirect('/alumnoVista')

            elif user.is_profesor == True:
                return redirect( '/profesorVista')
    return redirect('/')

def vistaProfesor(request):
    arreglo=[]
    nombreProfesor = User.objects.get(id=request.session['id'])
    id_profesor = request.session['id']
    cita= Cita.objects.all().order_by('id')

    for z in cita:
        if (z.estado == True):
            x_info = {}
            x_info['id']= z.id
            alumno= User.objects.get(id=z.alumno_id)
            x_info['alumno']= alumno.first_name
            x_info['comentario']= z.comentario
            x_info['fechaCita'] = z.fechaCita
            result = cloudinary.Search().expression('public_id:'+z.archivo+'').execute()
            print("LEEEN")
            print(result["total_count"])
            cantResult=int(result["total_count"])
            if (cantResult!=1):
                x_info['archivo']=0
            else:
                x_info['archivo']=result['resources'][0]['secure_url']
            factTable = FactTable.objects.filter(asesoria_id= z.asesoria_id)

            for x in factTable:

                if (x.profesor_id == id_profesor):
                    #CURSO
                    curso= Curso.objects.filter(id=x.curso_id)
                    for y in curso:
                        x_info['curso'] = y.nombre

                    #ASESORIA
                    asesoria=Asesoria.objects.filter(id=x.asesoria_id)
                    for y in asesoria:

                        x_info['horario'] = y.horario
                        x_info['dia'] = y.dia
                        x_info['lugar'] = y.lugar

                    #Seccion
                    seccion=Seccion.objects.filter(id=x.seccion_id)
                    for y in seccion:
                        x_info['seccion'] = y.codigo

                    arreglo.append(x_info)
    #print(arreglo)
    return render(request, 'profesorVista.html', locals())

def vistaAlumno(request):
    tipo = 0
    agregar = 0
    factTable = FactTable.objects.all().order_by("id")
    print(factTable)
    arreglo=[]
    nombreAlumno = User.objects.get(id=request.session['id'])
    for x in factTable:
        print (5)
        x_info = {}

        #CURSO
        curso= Curso.objects.filter(id=x.curso_id)
        for y in curso:
            x_info['curso'] = y.nombre

        #PROFESOR
        profesor=User.objects.filter(id=x.profesor_id)
        for y in profesor:
            x_info['profesor'] = y.first_name+" "+y.last_name

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
    #print(arreglo)

    return render(request, 'alumnoVista.html', locals())
def uploadFiles(idCita,file):

    nomFile=str(file)
    nomFin=str(idCita)+','+nomFile
    u=cloudinary.uploader.upload(file,resource_type="raw", public_id= nomFin )
    url=u['url']
    result = cloudinary.Search().expression('public_id='+nomFin+'').execute()
    return nomFin
def generarCita(request):
    arrFechas=[]
    arrFechas=mostrarFechas(2018,0)
    val=request.POST['fecha_pactada']
    print(val)
    for s in arrFechas:
       print(s)
    file=request.FILES['file'] if 'file' in request.FILES else False
    if (Cita.objects.filter(alumno_id=request.session['id'],fechaCita=request.POST['fecha_pactada'], asesoria_id=request.POST['id_asesoria'], estado=True).exists()):
        #si es que ya existe una cita pactada
        #return redirect('/alumnoVista')
        citaGenerada=True
        #request.session=request.session['id']

        #return render(request,'alumnoVista.html',locals())
        #return redirect('/alumnoVista')
        return redirect('/alumnoCita')
    else:
        cita= Cita.objects.create(alumno_id= request.session['id'], asesoria_id=request.POST['id_asesoria'],comentario=request.POST['comentario'], estado=True,fechaCita=val)
        cita.save()
    if file==False:# si es que no hay archivo
        print("No se grabo")
    else:

        cita.archivo=uploadFiles(cita.id,file)
        cita.save()
    return redirect('/alumnoCita')

def consultarCita(request):
    return redirect('/alumnoCita')

def alumnoCita(request):
    arreglo=[]
    nombreAlumno = User.objects.get(id=request.session['id'])
    id_alumno = request.session['id']
    print(id_alumno)
    cita= Cita.objects.filter(alumno_id= id_alumno)
    print(dir(cita[0]))

    print("AlumnoCita")

    for x in cita:
        if (x.estado == True):
            x_info = {}
            x_info['id'] = x.id
            x_info['comentario'] = x.comentario
            x_info['fechaCita'] = x.fechaCita
            result = cloudinary.Search().expression('public_id:'+x.archivo+'').execute()
            print("LEEEN")
            print(result["total_count"])
            cantResult=int(result["total_count"])
            if (cantResult!=1):
                x_info['archivo']=0
            else:
                x_info['archivo']=result['resources'][0]['secure_url']
            #ASESORIA
            asesoria=Asesoria.objects.filter(id=x.asesoria_id)
            for y in asesoria:
                x_info['horario'] = y.horario
                x_info['dia'] = y.dia
                x_info['lugar'] = y.lugar

                factTable = FactTable.objects.filter(asesoria_id= y.id)

                for fact in factTable:

                    #CURSO
                    curso= Curso.objects.filter(id=fact.curso_id)
                    for q in curso:
                        x_info['curso'] = q.nombre

                    #PROFESOR
                    profesor=User.objects.filter(id=fact.profesor_id)
                    for q in profesor:
                        x_info['profesor'] = q.first_name+" "+q.last_name

                    #Seccion
                    seccion=Seccion.objects.filter(id=fact.seccion_id)
                    for q in seccion:
                        x_info['seccion'] = q.codigo

            arreglo.append(x_info)
    #print(arreglo)
    return render(request, 'alumnoCita.html', locals())

def regresar(request):
    return redirect('/alumnoVista')

def cancelarCita(request):
    id=request.POST.get('id_cita', False)
    Cita.objects.filter(id=id).delete()
    return redirect('/alumnoCita')

def marcarAtencion(request):
    id_cita=request.POST.get('id_cita', False)
    print(id_cita)
    cita= Cita.objects.get(id=id_cita)
    #print(cita)
    cita.estado = False
    cita.save()
    return redirect('/profesorVista')
def buscar(request):
    busqueda=request.POST['buscar']
    print(request)
    buscarCurso=Curso.objects.filter(nombre__iexact=busqueda)
    buscarProfesor=User.objects.filter(first_name__iexact=busqueda)
    buscarProfesor2=User.objects.filter(last_name__iexact=busqueda)
    buscarHorario=Asesoria.objects.filter(horario__iexact=busqueda)
    buscarDia=Asesoria.objects.filter(dia__iexact=busqueda)
    buscarLugar=Asesoria.objects.filter(lugar__iexact=busqueda)
    buscarSeccion=Seccion.objects.filter(codigo__iexact=busqueda)

    #Buscar si es curso
    if buscarCurso:
        id= Curso.objects.get(nombre__iexact=busqueda)
        factTable=FactTable.objects.filter(curso_id=id.id)

    #Buscar si es Profesor
    elif buscarProfesor:
        id= User.objects.get(first_name__iexact=busqueda)
        factTable=FactTable.objects.filter(profesor_id=id.id)

    elif buscarProfesor2:
        id= User.objects.get(last_name__iexact=busqueda)
        factTable=FactTable.objects.filter(profesor_id=id.id)

    #Buscar si es Horario
    elif buscarHorario:
        id= Asesoria.objects.get(horario__iexact=busqueda)
        factTable=FactTable.objects.filter(asesoria_id=id.id)

    #Buscar si es Dia
    elif buscarDia:
        id= Asesoria.objects.get(dia__iexact=busqueda)
        factTable=FactTable.objects.filter(asesoria_id=id.id)

    #Buscar si es Lugar
    elif buscarLugar:
        id= Asesoria.objects.get(lugar__iexact=busqueda)
        factTable=FactTable.objects.filter(asesoria_id=id.id)

    #Buscar si es Seccion
    elif buscarSeccion:
        id= Seccion.objects.get(codigo__iexact=busqueda)
        factTable=FactTable.objects.filter(seccion_id=id.id)

    else:
        factTable=FactTable.objects.filter(curso_id=99999)

    arreglo=[]
    nombreAlumno = User.objects.get(id=request.session['id'])
    for x in factTable:
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
    #print(arreglo)||||||

    return render(request, 'alumnoVista.html', locals())
def quitarDup(a):
    dup_items = set()
    uniq_items = []

    for x in a:
        print(x.id)
        if x.id not in dup_items:
            uniq_items.append(x)
            dup_items.add(x.id)
    return uniq_items



def validate_curso(request):
    curso = request.GET.get('curso', None)
    buscarCurso=Curso.objects.filter(nombre__iexact=curso)
    objCurso= Curso.objects.get(nombre__iexact=curso)
    factTable=FactTable.objects.filter(curso_id=objCurso.id)
    print(curso)
    print(buscarCurso)
    print(id)
    print(factTable)
    temp=[]
    profes=[]
    Cursos=[]
    print()
    profesor=[]
    Secciones=[]
    arr=[]
    Secciones=Seccion.objects.filter(curso=objCurso)
    print("LEN SECCIONESs")
    print(len(Secciones))
    for i in Secciones:
        print("Seccion")
        print(i.profesor)
        profesor.append(i.profesor)
        print(profesor)
        for y in profesor:
            temp.append(y)
            arr=quitarDup(temp)
    for i in arr:
        profes.append(i.first_name + " " + i.last_name)
        print(i.first_name)
    #print(len(profes))
    data = {
        'is_taken' : True,
        'profesores' : json.dumps(profes)
    }
    return JsonResponse(data)

def validate_profesor(request):
    first = request.GET.get('first', None)
    last=request.GET.get('last',None)
    id=User.objects.get(first_name__iexact=first)
    id2=User.objects.get(last_name__iexact=last)
    factTable=FactTable.objects.filter(profesor_id=id.id)
    temp=[]
    secciones=[]
    Secciones=Seccion.objects.filter(profesor=id)
    if id.id==id2.id:
        for y in Secciones:
            print(y.codigo)
            temp.append(y)
            arr=quitarDup(temp)
    #if id.id==id2.id:
    #    temp=[]
    #    secciones=[]
    #    for i in factTable:
    #        seccion=Seccion.objects.filter(id=i.seccion_id)
    #        print("sssssss")
    #        for y in seccion:
    #            print(y.codigo)
    #            temp.append(y)
    #            arr=quitarDup(temp)
        for i in arr:
            secciones.append(i.codigo)
            print("finnnn")
            print(i.codigo)
        print(len(secciones))

    data = {
        'is_taken' : True,
        'seccion' : json.dumps(secciones)
    }
    return JsonResponse(data)


def citaAtendida(request):
    arreglo=[]
    nombreAlumno = User.objects.get(id=request.session['id'])
    id_alumno = request.session['id']
    cita= Cita.objects.filter(alumno_id= id_alumno)
    expresion= "null"
    for x in cita:
        if (x.estado == False):
            x_info = {}
            x_info['id'] = x.id
            x_info['comentario'] = x.comentario
            x_info['feedback'] = x.feedback
            #ASESORIA
            asesoria=Asesoria.objects.filter(id=x.asesoria_id)
            for y in asesoria:
                x_info['horario'] = y.horario
                x_info['dia'] = y.dia
                x_info['lugar'] = y.lugar

                factTable = FactTable.objects.filter(asesoria_id= y.id)

                for fact in factTable:

                    #CURSO
                    curso= Curso.objects.filter(id=fact.curso_id)
                    for q in curso:
                        x_info['curso'] = q.nombre

                    #PROFESOR
                    profesor=User.objects.filter(id=fact.profesor_id)
                    for q in profesor:
                        x_info['profesor'] = q.first_name+" "+q.last_name

                    #Seccion
                    seccion=Seccion.objects.filter(id=fact.seccion_id)
                    for q in seccion:
                        x_info['seccion'] = q.codigo

            arreglo.append(x_info)
    #print(arreglo)
    return render(request, 'citaAtendida.html', locals())

def feedback(request):
    feedback = request.POST['feedback']
    id_cita=request.POST.get('id_cita', False)
    cita= Cita.objects.get(id=id_cita)
    cita.feedback= feedback
    cita.estado = False
    cita.save()
    return redirect('/profesorVista')

def citaFin(request):
    arreglo=[]
    nombreProfesor = User.objects.get(id=request.session['id'])
    id_profesor = request.session['id']
    cita= Cita.objects.all().order_by('id')
    expresion= "null"
    for z in cita:
        if (z.estado == False):
            x_info = {}
            x_info['id']= z.id
            alumno= User.objects.get(id=z.alumno_id)
            x_info['alumno']= alumno.first_name
            x_info['comentario']= z.comentario
            x_info['feedback']= z.feedback
            factTable = FactTable.objects.filter(asesoria_id= z.asesoria_id)

            for x in factTable:

                if (x.profesor_id == id_profesor):
                    #CURSO
                    curso= Curso.objects.filter(id=x.curso_id)
                    for y in curso:
                        x_info['curso'] = y.nombre

                    #ASESORIA
                    asesoria=Asesoria.objects.filter(id=x.asesoria_id)
                    for y in asesoria:

                        x_info['horario'] = y.horario
                        x_info['dia'] = y.dia
                        x_info['lugar'] = y.lugar

                    #Seccion
                    seccion=Seccion.objects.filter(id=x.seccion_id)
                    for y in seccion:
                        x_info['seccion'] = y.codigo

                    arreglo.append(x_info)
    #print(arreglo)
    return render(request, 'citaFin.html', locals())


def obtenerFechaCita(request):
    numSemana = request.GET.get('numSemana', None)
    idSemana = request.GET.get('idSemana', None)
    diaSemana = request.GET.get('diaSemana', None)
    switcher = {
        "lunes": 0,
        "Martes": 1,
        "Miercoles": 2,
        "jueves": 3,
        "Viernes": 4,
        "sabado": 5,
        "Domingo": 6,
    }
    numDia=switcher[diaSemana]
    print("numDIAAA")
    print(numDia)
    arrSepId=[]
    arrSepNum=[]
    arrSepId=idSemana.split("/")
    arrSepNum=numSemana.split("/")
    arrFechas=[]
    arrFechas=mostrarFechas(2018,numDia)
    print(len(arrFechas))
    print(numSemana)
    print("split")
    print(arrSepNum[1])
    semanaElegida=arrSepNum[1]
    fecha=arrFechas[int(semanaElegida)-1]
    print("FECHAAA")
    print(fecha)
    data = {
        'is_taken' : True,
        'fecha' : fecha
    }
    return JsonResponse(data)

def regresarVistaProfe(request):
    return redirect('/profesorVista')
