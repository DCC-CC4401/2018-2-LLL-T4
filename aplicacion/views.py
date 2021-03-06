from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
import datetime

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
            cursos = Curso.objects.filter(id__in=alumnocurso).order_by('-ano', '-semestre')
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
            alumnoCurso = AlumnoCurso.objects.filter(alumno=alumno[0], curso=curso)
            if not alumnoCurso:
                return redirect('landingpagealumnos')

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

def curso_alumno(request):
    if request.user.is_authenticated and request.method == 'GET':
        user = request.user
        curso_id = request.GET.get('curso')
        alumno = Alumno.objects.filter(user=user)
        if not alumno:
            return redirect('login')
        else:
            curso = Curso.objects.get(id=curso_id)
            alumnoCurso = AlumnoCurso.objects.filter(alumno=alumno[0], curso =curso)
            if not alumnoCurso:
                return redirect('landingpagealumnos')
            coevaluaciones = Coevaluacion.objects.filter(curso=curso)
            alumnoCoevaluaciones = AlumnoCoevaluacion.objects.filter(alumno=alumno[0], coevaluacion__in=coevaluaciones).order_by('-coevaluacion__fecha_inicio')
            print(alumnoCoevaluaciones)
            context = {'user': user, 'alumnoCoevaluaciones': alumnoCoevaluaciones, 'curso': curso}
            return render(request, 'curso-vista-alumno.html', context)
    else:
        return redirect('login')

def curso_docente(request):
    if request.user.is_authenticated and request.method == 'POST':
        user = request.user
        docente = Docente.objects.filter(user=user)
        curso_id = request.GET.get('curso')
        curso = Curso.objects.get(id=curso_id)
        nombreCoevaluacion = request.POST.get('nombreCoevaluacion')
        fecha = request.POST.get('fechaEntrega')
        hora = request.POST.get('horaEntrega')

        fecha_objeto = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        hora_objeto = datetime.datetime.strptime(hora,'%H:%M').time()
        fecha_fin = datetime.datetime.combine(fecha_objeto,hora_objeto)

        coevaluacion = Coevaluacion(nombre=nombreCoevaluacion, fecha_inicio=timezone.now(),
                                    fecha_fin=fecha_fin, curso=curso, estado='Abierta')
        coevaluacion.save()
        alumnoCursos = AlumnoCurso.objects.filter(curso=curso)
        for alumnoCurso in alumnoCursos:
            alumno = alumnoCurso.alumno
            alumnoCoevaluacion =AlumnoCoevaluacion(alumno=alumno, coevaluacion=coevaluacion, estado='Pendiente')
            alumnoCoevaluacion.save()
        createPreguntas(coevaluacion)
        return HttpResponseRedirect("")
    elif request.user.is_authenticated and request.method == 'GET':
        user = request.user
        curso_id = request.GET.get('curso')
        docente = Docente.objects.filter(user=user)
        if not docente:
            return redirect('login')
        else:
            curso = Curso.objects.get(id=curso_id)
            docenteCurso = DocenteCurso.objects.filter(docente=docente[0], curso=curso)
            if not docenteCurso:
                return redirect('landingpagealumnos')
            lista_coevs = Coevaluacion.objects.filter(curso=curso).order_by('-fecha_inicio')
            for coevs in lista_coevs:
                if coevs.fecha_fin <= timezone.now() and coevs.estado == 'Abierta':
                    coevs.estado = 'Cerrada'
            grupos_act = Grupo.objects.filter(curso=curso)
            alum_grup_act = AlumnoGrupo.objects.filter(grupo__in=grupos_act)
            lista_coevs_pubicadas = lista_coevs.filter(estado='Publicada')
            alum_coev = AlumnoCoevaluacion.objects.filter(coevaluacion__in=lista_coevs_pubicadas)
            context = {'user': user, 'curso': curso, 'coevaluaciones':lista_coevs, 'grupos':grupos_act, 'alumnos':alum_grup_act, 'alum_coev':alum_coev, 'docenteCurso':docenteCurso[0], 'coevPublicadas':lista_coevs_pubicadas}
            return render(request, 'curso-vista-docente.html', context)
    else:
        return redirect('login')

def perfil_view(request):
    #arreglar, solo puede verlo alumno
    context = {}

    if request.method == 'POST':
        user = request.user
        username = user.username
        passOld = request.POST.get('passOld')
        valid = authenticate(request, username=username, password=passOld)
        if valid is not None:
            passNew = request.POST.get('passNew')
            passNewConfirm = request.POST.get('passNewConfirm')
            if passNew == passNewConfirm:
                user.set_password(passNew)
                user.save()
                update_session_auth_hash(request, user)
                context.update({'correcto': 'correcto'})
            else:
                context.update({'error': 'error'})
        else:
            context.update({'error': 'error'})

    if request.user.is_authenticated:
        user = request.user
        alumno = Alumno.objects.filter(user=user)
        if not alumno:
            return redirect('login')
        else:

            alumnocurso = AlumnoCurso.objects.filter(alumno=alumno[0]).values('curso_id')
            cursos = Curso.objects.filter(id__in=alumnocurso)
            coevaluaciones = Coevaluacion.objects.filter(curso__in=cursos)
            alumnoCoevaluaciones = AlumnoCoevaluacion.objects.filter(alumno=alumno[0], coevaluacion__in = coevaluaciones, estado='Publicada').order_by('-coevaluacion__fecha_inicio')
            print(alumnoCoevaluaciones)
            n_cursos = cursos.__len__()
            n_coev = alumnoCoevaluaciones.__len__()
            context.update ({'cursos': cursos, 'user': user, 'alumnoCoevaluaciones': alumnoCoevaluaciones, 'n_cursos': n_cursos,
                        'n_coev': n_coev})
            return render(request, 'perfil-vista-dueno.html', context)
    else:
        return redirect('login')

def createPreguntas(coevaluacion):
    pregunta1 = Pregunta(descripcion="Demuestra compromiso con el proyecto",
                         tipo='Multiple',
                         coevaluacion=coevaluacion,
                         ponderacion=0.8)
    pregunta1.save()
    pregunta2 = Pregunta(descripcion="Cumple de manera adecuada con las tareas que le son asignadas",
                         tipo='Multiple',
                         coevaluacion=coevaluacion,
                         ponderacion=0.8)
    pregunta2.save()
    pregunta3 = Pregunta(descripcion="Demuestra iniciativa para lograr el éxito del proyecto",
                         tipo='Multiple',
                         coevaluacion=coevaluacion,
                         ponderacion=0.8)
    pregunta3.save()
    pregunta4 = Pregunta(descripcion="Mantiene buena comunicación con el resto del equipo",
                         tipo='Multiple',
                         coevaluacion=coevaluacion,
                         ponderacion=0.8)
    pregunta4.save()
    pregunta5 = Pregunta(descripcion="Mantiene buena coordinación entre sus tareas y las de sus pares",
                         tipo='Multiple',
                         coevaluacion=coevaluacion,
                         ponderacion=0.8)
    pregunta5.save()
    pregunta6 = Pregunta(descripcion="La calidad de su trabajo es la apropiada para lograr el éxito del proyecto. ",
                         tipo='Multiple',
                         coevaluacion=coevaluacion,
                         ponderacion=0.8)
    pregunta6.save()
    pregunta7 = Pregunta(descripcion="Ofrece apoyo en las tareas que van más allá del rol asignado",
                         tipo='Multiple',
                         coevaluacion=coevaluacion,
                         ponderacion=0.8)
    pregunta7.save()
    pregunta8 = Pregunta(descripcion="Es capaz de admitir sus equivocaciones y recibir críticas",
                         tipo='Multiple',
                         coevaluacion=coevaluacion,
                         ponderacion=0.8)
    pregunta8.save()
    pregunta9 = Pregunta(descripcion="Fortalezas",
                         tipo='Desarrollo',
                         coevaluacion=coevaluacion,
                         ponderacion=0)
    pregunta9.save()
    pregunta10 = Pregunta(descripcion="Debilidades",
                          tipo='Desarrollo',
                          coevaluacion=coevaluacion,
                          ponderacion=0)
    pregunta10.save()