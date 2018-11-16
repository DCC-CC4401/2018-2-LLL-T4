from django.shortcuts import render

from aplicacion.models import Curso, AlumnoCurso, PersonaNatural, Alumno


def login(request):
    return render(request, 'login.html')


def landingPageAlumnos(request):
    persona = PersonaNatural.objects.get(RUT="19.540.088-1")
    alumno = Alumno.objects.get(personaNatural=persona)
    cursos = AlumnoCurso.objects.filter(alumno=alumno)

    context = {'cursos': cursos}
    return render(request, 'home-vista-alumno.html', context)
