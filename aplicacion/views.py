from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from aplicacion.models import Curso, AlumnoCurso, Alumno


def login_view(request):
    if request.method == 'POST':
        print("if")
        username = request.POST['user']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landingpagealumnos')
        else:
            return render(request, 'login.html')
    else:
        print("else")
        return render(request, 'login.html')


def landingPageAlumnos_view(request):
    # persona = PersonaNatural.objects.get(RUT="19.540.088-1")
    # alumno = Alumno.objects.get(personaNatural=persona)
    # cursos = AlumnoCurso.objects.filter(alumno=alumno)
    # context = {'cursos': cursos}
    # return render(request, 'home-vista-alumno.html', context)
    return render(request, 'home-vista-alumno.html')
