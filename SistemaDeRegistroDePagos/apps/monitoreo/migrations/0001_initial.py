# Generated by Django 4.0.4 on 2022-07-24 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='condicionesPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaEscrituracion', models.DateField()),
                ('montoFinanciamiento', models.DecimalField(decimal_places=2, max_digits=8)),
                ('plazo', models.IntegerField()),
                ('tasaInteres', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cuotaKi', models.DecimalField(blank=True, decimal_places=2, max_digits=8)),
                ('comisionCuota', models.DecimalField(decimal_places=2, max_digits=8)),
                ('mantenimientoCuota', models.DecimalField(decimal_places=2, max_digits=8)),
                ('multaMantenimiento', models.DecimalField(decimal_places=2, max_digits=8)),
                ('multaFinanciamiento', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estado', models.BooleanField(default=True)),
                ('detalleVenta', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.detalleventa')),
            ],
        ),
        migrations.CreateModel(
            name='tablaAmortizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detalleVenta', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.detalleventa')),
            ],
        ),
        migrations.CreateModel(
            name='resumenPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaUltimoPago', models.DateField()),
                ('fechaUltimoCorte', models.DateField()),
                ('saldoCapital', models.DecimalField(decimal_places=2, max_digits=8)),
                ('fechaCancelado', models.DateField()),
                ('descuentoPP', models.DecimalField(decimal_places=2, max_digits=8)),
                ('prima', models.DecimalField(decimal_places=2, max_digits=8)),
                ('abonosCapital', models.DecimalField(decimal_places=2, max_digits=8)),
                ('abonosComision', models.DecimalField(decimal_places=2, max_digits=8)),
                ('abonosRecargo', models.DecimalField(decimal_places=2, max_digits=8)),
                ('abonosOtros', models.DecimalField(decimal_places=2, max_digits=8)),
                ('abonosIntereses', models.DecimalField(decimal_places=2, max_digits=8)),
                ('abonosMantenimiento', models.DecimalField(decimal_places=2, max_digits=8)),
                ('detalleVenta', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.detalleventa')),
            ],
        ),
        migrations.CreateModel(
            name='estadoCuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaRegistro', models.DateField(auto_now_add=True)),
                ('nombre', models.CharField(blank=True, max_length=20)),
                ('condicionesPago', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='monitoreo.condicionespago')),
            ],
        ),
        migrations.CreateModel(
            name='cuotaAmortizacion',
            fields=[
                ('numeroCuota', models.IntegerField(primary_key=True, serialize=False)),
                ('fechaPago', models.DateField()),
                ('diasInteres', models.IntegerField()),
                ('montoCancelado', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tasaInteres', models.DecimalField(decimal_places=2, max_digits=8)),
                ('interesGenerado', models.DecimalField(decimal_places=2, max_digits=8)),
                ('interesPagado', models.DecimalField(decimal_places=2, max_digits=8)),
                ('comision', models.DecimalField(decimal_places=2, max_digits=8)),
                ('subTotal', models.DecimalField(decimal_places=2, max_digits=8)),
                ('abonoCapital', models.DecimalField(decimal_places=2, max_digits=8)),
                ('saldoCapital', models.DecimalField(decimal_places=2, max_digits=8)),
                ('saldoInteres', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tablaAmortizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoreo.tablaamortizacion')),
            ],
        ),
    ]
