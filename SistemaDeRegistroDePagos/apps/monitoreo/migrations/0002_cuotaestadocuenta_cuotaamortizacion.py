# Generated by Django 4.0.4 on 2022-06-09 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoreo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuotaestadocuenta',
            name='cuotaAmortizacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoreo.cuotaamortizacion'),
        ),
    ]