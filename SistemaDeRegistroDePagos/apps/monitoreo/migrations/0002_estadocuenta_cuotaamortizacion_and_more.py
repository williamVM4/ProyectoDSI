# Generated by Django 4.0.4 on 2022-07-19 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoreo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estadocuenta',
            name='cuotaAmortizacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoreo.cuotaamortizacion'),
        ),
        migrations.DeleteModel(
            name='cuotaEstadoCuenta',
        ),
    ]
