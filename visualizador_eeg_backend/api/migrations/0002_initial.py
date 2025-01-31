# Generated by Django 5.1.1 on 2024-09-04 18:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Canal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_canal', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Enfermedad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Frecuencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frecuencia', models.FloatField()),
                ('canal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.canal')),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_paciente', models.CharField(max_length=30)),
                ('enfermedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.enfermedad')),
            ],
        ),
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_sesion', models.DateTimeField()),
                ('intervalo', models.DecimalField(decimal_places=6, max_digits=8)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.paciente')),
            ],
        ),
        migrations.AddField(
            model_name='canal',
            name='sesion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.sesion'),
        ),
    ]
