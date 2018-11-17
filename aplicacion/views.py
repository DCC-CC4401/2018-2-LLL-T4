from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from aplicacion.models import Curso, AlumnoCurso, Alumno, Coevaluacion


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