# Generated by Django 5.0.6 on 2024-06-05 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0002_resultado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultado',
            name='fecha',
        ),
        migrations.AddField(
            model_name='resultado',
            name='detalles',
            field=models.TextField(blank=True, null=True),
        ),
    ]
