# Generated by Django 2.1 on 2018-11-21 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0008_pregunta_ponderacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pregunta',
            name='ponderacion',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]
