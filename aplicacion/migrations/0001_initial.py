# Generated by Django 2.1 on 2018-11-16 04:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AlumnoCoevaluacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField()),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='AlumnoCurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='aplicacion.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='AlumnoGrupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ingreso', models.DateField()),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='AlumnoRespuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='Coevaluacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('estado', models.CharField(max_length=255)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semestre', models.IntegerField()),
                ('seccion', models.IntegerField()),
                ('ano', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CursoDatos',
            fields=[
                ('nombre', models.CharField(max_length=255)),
                ('codigo', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocenteCurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=255)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.Curso')),
                ('docente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='aplicacion.Docente')),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('nombre', models.CharField(max_length=255)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.Curso')),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('tipo', models.CharField(max_length=255)),
                ('coevaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.Coevaluacion')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.TextField()),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.Pregunta')),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='datos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.CursoDatos'),
        ),
        migrations.AddField(
            model_name='coevaluacion',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.Curso'),
        ),
        migrations.AddField(
            model_name='alumnorespuesta',
            name='respuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.Respuesta'),
        ),
        migrations.AddField(
            model_name='alumnogrupo',
            name='grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.Grupo'),
        ),
        migrations.AddField(
            model_name='alumnocurso',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.Curso'),
        ),
        migrations.AddField(
            model_name='alumnocoevaluacion',
            name='coevaluacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.Coevaluacion'),
        ),
        migrations.AlterUniqueTogether(
            name='pregunta',
            unique_together={('descripcion', 'coevaluacion')},
        ),
        migrations.AlterUniqueTogether(
            name='grupo',
            unique_together={('nombre', 'curso'), ('numero', 'curso')},
        ),
        migrations.AlterUniqueTogether(
            name='docentecurso',
            unique_together={('docente', 'curso')},
        ),
        migrations.AlterUniqueTogether(
            name='curso',
            unique_together={('datos', 'semestre', 'seccion', 'ano')},
        ),
        migrations.AlterUniqueTogether(
            name='coevaluacion',
            unique_together={('nombre', 'curso')},
        ),
        migrations.AlterUniqueTogether(
            name='alumnocurso',
            unique_together={('alumno', 'curso')},
        ),
        migrations.AlterUniqueTogether(
            name='alumnocoevaluacion',
            unique_together={('alumno', 'coevaluacion')},
        ),
    ]
