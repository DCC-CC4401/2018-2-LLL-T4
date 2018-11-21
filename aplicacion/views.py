from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from aplicacion.models import *


def login_view(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landingpagealumnos')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def landingPageAlumnos_view(request):
    if request.user.is_authenticated:
        user = request.user
        alumno = Alumno.objects.filter(user=user)
        if not alumno:
            return redirect('login')
        else:
            alumnocurso = AlumnoCurso.objects.filter(alumno=alumno[0]).values('curso_id')
            cursos = Curso.objects.filter(id__in=alumnocurso)
            alumnoCoevaluaciones = AlumnoCoevaluacion.objects.filter(alumno=alumno[0]).order_by('-coevaluacion__fecha_inicio')[:10]

            context = {'cursos': cursos, 'user': user, 'alumnoCoevaluaciones': alumnoCoevaluaciones}
            for alumnoCoevaluacion in alumnoCoevaluaciones:
                if alumnoCoevaluacion.coevaluacion.fecha_fin <= timezone.now() and (alumnoCoevaluacion.estado == 'Pendiente' or alumnoCoevaluacion.estado == 'Contestada'):
                    alumnoCoevaluacion.coevaluacion.estado = 'Cerrada'
                    alumnoCoevaluacion.coevaluacion.save()
                    alumnoCoevaluacion.estado = 'Cerrada'
                    alumnoCoevaluacion.save()
            return render(request, 'home-vista-alumno.html', context)
    else:
        return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')


def coevaluacionAlumnos_view(request):
    #falta revisar caso coevaluacion cerrada

    #Para poder dejar las notas en un solo lugar hacemos un modelo que se llame "alumno-pregunta-nota"

    if request.user.is_authenticated and request.method == 'POST':
        #Anadir respuestas a la base de dates
        #anadimos todas las respuestas, luego verificamos si alguna es none. Si es none, no se guardan los cambios.
        coevaluacion_id = request.GET.get('coevaluacion')
        coevaluacion = Coevaluacion.objects.get(id=coevaluacion_id)
        preguntas = Pregunta.objects.filter(coevaluacion=coevaluacion)
        evaluado_id = request.GET.get('companero')
        evaluado = Alumno.objects.get(user_id=evaluado_id)
        user = request.user
        autor = Alumno.objects.get(user=user)

        for pregunta in preguntas:
            valor = request.POST.get(str(pregunta.id))
            respuesta = Respuesta(pregunta=pregunta, valor=valor)
            respuesta.save()
            alumnoRespuesta = AutorAlumnoRespuesta(autor=autor, alumno=evaluado, respuesta=respuesta)
            alumnoRespuesta.save()

        #Anadir evaluado a la base de datos
        evaluacion = AutorAlumnoCoevaluacion(autor = autor, alumno = evaluado, coevaluacion=coevaluacion)
        evaluacion.save()

        return HttpResponseRedirect("")
    elif request.user.is_authenticated and request.method == 'GET':
        user = request.user
        coevaluacion_id = request.GET.get('coevaluacion')
        evaluado_id = request.GET.get('companero')


        coevaluacion = Coevaluacion.objects.get(id=coevaluacion_id)
        evaluado = Alumno.objects.filter(user_id=evaluado_id)
        curso = coevaluacion.curso
        alumno = Alumno.objects.filter(user=user)
        if not alumno:
            return redirect('login')
        else:
            alumnoCoevaluacion = AlumnoCoevaluacion.objects.get(alumno=alumno[0], coevaluacion=coevaluacion)

            grupos = Grupo.objects.filter(curso=curso)
            alumnosCoevaluados = AutorAlumnoCoevaluacion.objects.filter(autor=alumno[0], coevaluacion=coevaluacion).values('alumno_id')
            grupo = AlumnoGrupo.objects.get(alumno=alumno[0], grupo__in=grupos, pertenece=True).grupo

            companeros = AlumnoGrupo.objects.filter(grupo=grupo, pertenece=True).exclude(alumno=alumno[0])
            companerosNoContestado = companeros.exclude(alumno_id__in = alumnosCoevaluados)
            companerosContestados = companeros.difference(companerosNoContestado)
            preguntas = Pregunta.objects.filter(coevaluacion = coevaluacion)

            if not companerosNoContestado and alumnoCoevaluacion.estado == 'Pendiente':
                alumnoCoevaluacion.estado = 'Contestada'
                alumnoCoevaluacion.save()
            if not evaluado:
                context = {'user': user, 'alumnoCoevaluacion': alumnoCoevaluacion,
                           'companerosContestados': companerosContestados,
                           'companerosNoContestado': companerosNoContestado}
            else:
                evaluadoIn = companerosNoContestado.filter(alumno=evaluado[0])
                if not evaluadoIn:
                    evaluadoIn = True
                else:
                    evaluadoIn = False
                context = {'user': user, 'alumnoCoevaluacion': alumnoCoevaluacion,
                           'companerosContestados': companerosContestados,
                           'companerosNoContestado': companerosNoContestado,
                           'evaluado' : evaluado[0], 'evaluadoIn' : evaluadoIn,
                           'preguntas' : preguntas}
            return render(request, 'coevaluacion-vista-alumno.html', context)
    else:
        return redirect('login')

def perfil_view(request):
    #arreglar, solo puede verlo alumno
    if request.user.is_authenticated:
        user = request.user
        alumno = Alumno.objects.filter(user=user)
        if not alumno:
            return redirect('login')
        else:
            alumnocurso = AlumnoCurso.objects.filter(alumno=alumno[0]).values('curso_id')
            cursos = Curso.objects.filter(id__in=alumnocurso)
            coevaluaciones = Coevaluacion.objects.filter(curso__in=cursos).order_by('-fecha_inicio')
            #falta preguntar por las notas
            context = {'cursos': cursos, 'user': user, 'coevaluaciones': coevaluaciones}
            return render(request, 'perfil-vista-dueno.html', context)
    else:
        return redirect('login')

def curso_alumno(request):
    if request.user.is_authenticated and request.method == 'GET':
        user = request.user
        curso_id = request.GET.get('curso')
        alumno = Alumno.objects.filter(user=user)
        if not alumno:
            return redirect('login')
        else:
            curso = Curso.objects.get(id=curso_id)
            lista_coevs = Coevaluacion.objects.filter(curso=curso).order_by('-fecha_inicio')
            context = {'user': user, 'lista_coevs': lista_coevs, 'curso': curso}
            return render(request, 'curso-vista-alumno.html', context)
    else:
        return redirect('login')

def curso_docente(request):
    if request.user.is_authenticated and request.method == 'GET':
        user = request.user
        curso_id = request.GET.get('curso')
        docente = Docente.objects.filter(user=user)
        if not docente:
            return redirect('login')
        else:
            curso = Curso.objects.get(id=curso_id)
            lista_coevs = Coevaluacion.objects.filter(curso=curso).order_by('-fecha_inicio')
            grupos_act = Grupo.objects.filter(curso=curso)
            alum_grup_act = AlumnoGrupo.objects.filter(grupo__in=grupos_act)
            context = {'user': user, 'curso': curso, 'coevaluaciones':lista_coevs, 'grupos':grupos_act, 'alumnos':alum_grup_act}
            return render(request, 'curso-vista-docente.html', context)
    else:
        return redirect('login')
