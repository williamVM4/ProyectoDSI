# Generated by Django 4.0.4 on 2022-05-27 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0002_propietario_alter_proyectoturistico_options_lote_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='prima',
            fields=[
                ('numeroRecibo', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('fechaPrima', models.DateField()),
                ('montoPrima', models.FloatField()),
                ('conceptoPrima', models.CharField(max_length=50)),
                ('detalleVenta', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.detalleventa')),
            ],
        ),
    ]
