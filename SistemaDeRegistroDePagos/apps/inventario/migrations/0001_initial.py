# Generated by Django 4.0.4 on 2022-07-24 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='asignacionLote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eliminado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='propietario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dui', models.CharField(max_length=10)),
                ('nombrePropietario', models.CharField(max_length=60)),
                ('direccion', models.CharField(max_length=50)),
                ('profesion', models.CharField(max_length=50)),
                ('trabajo', models.CharField(blank=True, default='', max_length=50)),
                ('direccionTrabajo', models.CharField(blank=True, default='', max_length=50)),
                ('telefonoTrabajo', models.CharField(blank=True, default='', max_length=9)),
                ('telefonoCasa', models.CharField(blank=True, default='', max_length=9)),
                ('telefonoCelular', models.CharField(max_length=9)),
                ('correoElectronico', models.EmailField(blank=True, default='', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='proyectoTuristico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreProyectoTuristico', models.CharField(max_length=50)),
                ('empresa', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='lote',
            fields=[
                ('matriculaLote', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('numeroLote', models.CharField(max_length=3)),
                ('poligono', models.CharField(max_length=2)),
                ('identificador', models.CharField(blank=True, max_length=5)),
                ('areaMCuadrado', models.DecimalField(decimal_places=2, max_digits=8)),
                ('areaVCuadrada', models.DecimalField(blank=True, decimal_places=2, max_digits=8)),
                ('proyectoTuristico', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.proyectoturistico')),
            ],
        ),
        migrations.CreateModel(
            name='detalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precioVenta', models.DecimalField(decimal_places=2, max_digits=8)),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estado', models.BooleanField(default=True)),
                ('lote', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.lote')),
                ('propietarios', models.ManyToManyField(through='inventario.asignacionLote', to='inventario.propietario')),
            ],
        ),
        migrations.CreateModel(
            name='cuentaBancaria',
            fields=[
                ('numeroCuentaBancaria', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombreCuentaBancaria', models.CharField(max_length=50)),
                ('tipoCuenta', models.CharField(max_length=30)),
                ('banco', models.CharField(max_length=30)),
                ('proyectoTuristico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.proyectoturistico')),
            ],
        ),
        migrations.AddField(
            model_name='asignacionlote',
            name='detalleVenta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.detalleventa'),
        ),
        migrations.AddField(
            model_name='asignacionlote',
            name='propietario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.propietario'),
        ),
        migrations.CreateModel(
            name='asignacionProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dui', models.CharField(max_length=10)),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.propietario')),
                ('proyectoTuristico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.proyectoturistico')),
            ],
            options={
                'unique_together': {('dui', 'proyectoTuristico')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='asignacionlote',
            unique_together={('propietario', 'detalleVenta')},
        ),
    ]
