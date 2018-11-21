from django.conf import settings
from django.db import models


# Aqui estan los modelos de datos. Falta asociar el usuario a la persona natural. Esto se puede hacer con lo siguiente:
# https://stackoverflow.com/questions/34875146/foreignkey-to-a-model-field .

class CursoDatos(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.nombre + ' ' + self.codigo


class Curso(models.Model):
    datos = models.ForeignKey(CursoDatos, on_delete=models.CASCADE)
    semestre = models.IntegerField()
    seccion = models.IntegerField()
    ano = models.IntegerField()

    def __str__(self):
        return self.datos.codigo + ' ' + str(self.semestre) + ' ' + str(self.seccion) + ' ' + str(self.ano)

    class Meta:
        unique_together = (('datos', 'semestre', 'seccion', 'ano'),)


class Grupo(models.Model):
    numero = models.IntegerField()
    nombre = models.CharField(max_length=255)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero) + ' ' + self.nombre + ' ' + self.curso.datos.nombre + ' ' + str(self.curso.ano)

    class Meta:
        unique_together = (('numero', 'curso'), ('nombre', 'curso'))


class Coevaluacion(models.Model):
    ESTADO_CHOICES = (
        ('Abierta', 'Abierta'),
        ('Cerrada', 'Cerrada'),
        ('Publicada', 'Publicada'),
    )
    nombre = models.CharField(max_length=255)
    estado = models.CharField(max_length=255, choices=ESTADO_CHOICES)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + ' ' + self.curso.datos.nombre + ' ' + str(self.curso.ano)

    class Meta:
        unique_together = (('nombre', 'curso'),)


class Pregunta(models.Model):

    TIPO_CHOICES = (
        ('Multiple', 'Multiple'),
        ('Desarrollo', 'Desarrollo'),
    )
    descripcion = models.TextField()
    tipo = models.CharField(max_length=255, choices=TIPO_CHOICES)
    coevaluacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)
    ponderacion = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = (('descripcion', 'coevaluacion'),)


class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    valor = models.TextField()


class Alumno(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)


class Docente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)


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
    pertenece = models.BooleanField()
    fecha_ingreso = models.DateField()

    def __str__(self):
        return self.alumno.user.first_name + " " + self.grupo.nombre + " "



class AlumnoCoevaluacion(models.Model):
    ESTADO_CHOICES = (
        ('Contestada', 'Contestada'),
        ('Pendiente', 'Pendiente'),
        ('Cerrada', 'Cerrada'),
        ('Publicada', 'Publicada'),
    )
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    coevaluacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)
    estado = models.CharField(max_length=255, choices=ESTADO_CHOICES)

    class Meta:
        unique_together = (('alumno', 'coevaluacion'),)



#AutorAlumnoCoevaluacion: Une quien corrige al alumno en la respectiva coevaluacion.
#Si contesto la coevaluacion se encuentra la tabla, si es que no, no.

class AutorAlumnoCoevaluacion(models.Model):
    autor = models.ForeignKey(Alumno, related_name='autor', on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, related_name='alumno',on_delete=models.CASCADE)
    coevaluacion = models.ForeignKey(Coevaluacion, on_delete=models.CASCADE)

    class Meta:
       unique_together = (('autor','alumno', 'coevaluacion'),)


class AutorAlumnoRespuesta(models.Model):
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, related_name='alumno_respuesta',on_delete=models.CASCADE)
    autor = models.ForeignKey(Alumno, related_name='autor_respuesta', on_delete=models.CASCADE)
#agregar pregunta y coevaluacion


#Colocar AlumnoCoevaluacion para dar estado a las coevaluaciones