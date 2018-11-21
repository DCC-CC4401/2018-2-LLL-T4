from django.contrib import admin
from .models import *

admin.site.register(Curso)
admin.site.register(CursoDatos)
admin.site.register(Grupo)
admin.site.register(Coevaluacion)
admin.site.register(Pregunta)
admin.site.register(Alumno)
admin.site.register(Docente)
admin.site.register(DocenteCurso)
admin.site.register(AlumnoCurso)
admin.site.register(AlumnoGrupo)
admin.site.register(AlumnoCoevaluacion)
admin.site.register(Respuesta)
admin.site.register(AutorAlumnoRespuesta)
admin.site.register(AutorAlumnoCoevaluacion)

