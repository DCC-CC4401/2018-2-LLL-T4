# Generated by Django 2.1 on 2018-11-21 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0009_auto_20181121_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pregunta',
            name='ponderacion',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]