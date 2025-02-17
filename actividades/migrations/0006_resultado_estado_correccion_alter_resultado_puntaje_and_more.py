# Generated by Django 5.0.6 on 2024-06-28 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0005_estudiante_actividad'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultado',
            name='estado_correccion',
            field=models.CharField(default='pendiente', max_length=20),
        ),
        migrations.AlterField(
            model_name='resultado',
            name='puntaje',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resultado',
            name='ventana_perdida',
            field=models.TextField(blank=True, null=True),
        ),
    ]
