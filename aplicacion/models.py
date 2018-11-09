from django.db import models


# Aquí estan los modelos de datos. Falta asociar el usuario a la persona natural. Esto se puede hacer con lo siguiente:
# https://stackoverflow.com/questions/34875146/foreignkey-to-a-model-field .

class CursoNombre(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.nombre + ' ' + self.codigo


class Curso(models.Model):
    codigo = models.ForeignKey(CursoNombre, on_delete=models.CASCADE)
    semestre = models.CharField(max_length=255)
    seccion = models.IntegerField()
    ano = models.IntegerField()

    def __str__(self):
        return self.codigo.codigo + ' ' + self.semestre + ' ' + str(self.seccion) + ' ' + str(self.ano)

    class Meta:
        unique_together = (('codigo', 'semestre', 'seccion', 'ano'),)


class Grupo(models.Model):
    numero = models.IntegerField()
    nombre = models.CharField(max_length=255)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero) + ' ' + self.nombre + ' ' + self.curso.codigo.nombre + ' ' + str(self.curso.ano)

    class Meta:
        unique_together = (('numero', 'curso'), ('nombre', 'curso'))


class Coevaluacion(models.Model):
    nombre = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + ' ' + self.curso.codigo.nombre + ' ' + str(self.curso.ano)

    class Meta:
        unique_together = (('nombre', 'curso'),)


class Pregunta(models.Model):
    descripcion = models.TextField()
    tipo = models.CharField(max_length=255)
    coevaluacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('descripcion', 'coevaluacion'),)


class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    valor = models.TextField()


class PersonaNatural(models.Model):
    RUT = models.CharField(max_length=30, primary_key=True)
    correo = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)


class Alumno(models.Model):
    personaNatural = models.OneToOneField(PersonaNatural, on_delete=models.CASCADE, primary_key=True)


class Docente(models.Model):
    personaNatural = models.OneToOneField(PersonaNatural, on_delete=models.CASCADE, primary_key=True)


class AlumnoCurso(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.DO_NOTHING)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('alumno', 'curso'),)


class DocenteCurso(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.DO_NOTHING)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=255)

    class Meta:
        unique_together = (('docente', 'curso'),)


class AlumnoGrupo(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField()


class AlumnoCoevaluacion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    coevaluacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)
    nota = models.IntegerField()

    class Meta:
        unique_together = (('alumno', 'coevaluacion'),)


class AlumnoRespuesta(models.Model):
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
