
from django.contrib import admin
#from django.conf.urls import url
from django.urls import path, include
from asesorias import views
from accounts import views as accounts_views

urlpatterns = [


    path('administrador/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),




    #path(r'^register', views.register),
    #path('index', views.index),
    path('', accounts_views.index),
    path('login', accounts_views.login),
    path('buscar', accounts_views.buscar),
    path('profesorVista', accounts_views.vistaProfesor),
    path('alumnoVista', accounts_views.vistaAlumno),
    path('registro', accounts_views.registro),
    path('register', accounts_views.register),
    path('agregarAsesoria', views.mostrarCursos),
    path('guardarAsesoria', views.guardarAsesoria),
    path('listarAsesoria', views.listarAsesoria),
    path('eliminarAsesoria', views.eliminarAsesoria),
    path('editarAsesoria', views.editarAsesoria),
    path('guardarCambios', views.guardarCambios),
    path('cancelar', views.cancelar),
    path('salir', views.salir),
    path('logout', views.logout),
    path('generarCita', accounts_views.generarCita),
    path('consultarCita', accounts_views.consultarCita),
    path('alumnoCita', accounts_views.alumnoCita),
    path('regresar', accounts_views.regresar),
    path('cancelarCita', accounts_views.cancelarCita),
    path('marcarAtencion', accounts_views.marcarAtencion),

    path('validate_curso', accounts_views.validate_curso),
    path('validate_profesor', accounts_views.validate_profesor),


    path('citaAtendida', accounts_views.citaAtendida),
    path('feedback', accounts_views.feedback),
    path('citaFin', accounts_views.citaFin),
    path('regresarVistaProfe', accounts_views.regresarVistaProfe),

]
