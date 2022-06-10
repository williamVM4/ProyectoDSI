# Generated by Django 4.0.4 on 2022-06-10 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_alter_lote_proyectoturistico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='identificador',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.CreateModel(
            name='condicionPago',
            fields=[
                ('matriculaLote', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('numeroLote', models.IntegerField()),
                ('poligono', models.CharField(max_length=5)),
                ('identificador', models.CharField(max_length=4)),
                ('areaMCuadrado', models.FloatField()),
                ('areaVCuadrada', models.FloatField()),
                ('proyectoTuristico', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.proyectoturistico')),
            ],
        ),
    ]
