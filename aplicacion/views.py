from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


from aplicacion.models import Curso, AlumnoCurso, Alumno, Coevaluacion, Grupo, AlumnoGrupo, AlumnoCoevaluacion


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
            coevaluaciones = Coevaluacion.objects.filter(curso__in=cursos).order_by('-fecha_inicio')
            print(coevaluaciones[0].fecha_inicio)
            context = {'cursos': cursos, 'user': user, 'coevaluaciones': coevaluaciones}
            return render(request, 'home-vista-alumno.html', context)
    else:
        return redirect('login')
    # persona = PersonaNatural.objects.get(RUT="19.540.088-1")
    # alumno = Alumno.objects.get(personaNatural=persona)
    # cursos = AlumnoCurso.objects.filter(alumno=alumno)
    # context = {'cursos': cursos}
    # return render(request, 'home-vista-alumno.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def coevaluacionAlumnos_view(request):
    if request.user.is_authenticated and request.method == 'GET':
        user = request.user
        coevaluacion_id = request.GET.get('coevaluacion')
        coevaluacion = Coevaluacion.objects.get(id=coevaluacion_id)
        curso = coevaluacion.curso
        alumno = Alumno.objects.filter(user=user)
        if not alumno:
            return redirect('login')
        else:
            grupo = Grupo.objects.filter(curso=curso)
            alumnoGrupo = AlumnoGrupo.objects.get(alumno=alumno[0], grupo__in=grupo, pertenece=True)
            grupo = alumnoGrupo.grupo
            companeros = AlumnoGrupo.objects.filter(grupo=grupo, pertenece=True).exclude(alumno=alumno[0])
            context = {'user': user, 'coevaluacion': coevaluacion, 'companeros': companeros}
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
            alumnonotas = AlumnoCoevaluacion.objects.filter(alumno=alumno[0])
            n_cursos = cursos.__len__()
            coevaluaciones = Coevaluacion.objects.filter(curso__in=cursos).order_by('-fecha_inicio')
            n_coev = coevaluaciones.__len__()
            context = {'cursos': cursos, 'user': user, 'coevaluaciones': coevaluaciones, 'n_cursos': n_cursos,
                       'notas': alumnonotas, 'n_coev': n_coev}
            return render(request, 'perfil-vista-dueno.html', context)
    else:
        return redirect('login')
