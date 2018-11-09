from django.contrib import admin
from .models import *

admin.site.register(Curso)
admin.site.register(CursoNombre)
admin.site.register(Grupo)
admin.site.register(Coevaluacion)
admin.site.register(Pregunta)
admin.site.register(PersonaNatural)
admin.site.register(Alumno)
admin.site.register(Docente)
admin.site.register(DocenteCurso)
admin.site.register(AlumnoCurso)
admin.site.register(AlumnoGrupo)
admin.site.register(AlumnoCoevaluacion)
admin.site.register(Respuesta)
admin.site.register(AlumnoRespuesta)

