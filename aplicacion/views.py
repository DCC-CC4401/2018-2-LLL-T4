from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from aplicacion.models import Curso, AlumnoCurso, Alumno


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print(form.get_user())

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('landingpagealumnos')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def landingPageAlumnos_view(request):
    # persona = PersonaNatural.objects.get(RUT="19.540.088-1")
    # alumno = Alumno.objects.get(personaNatural=persona)
    # cursos = AlumnoCurso.objects.filter(alumno=alumno)
    # context = {'cursos': cursos}
    # return render(request, 'home-vista-alumno.html', context)
    return render(request, 'home-vista-alumno.html')
