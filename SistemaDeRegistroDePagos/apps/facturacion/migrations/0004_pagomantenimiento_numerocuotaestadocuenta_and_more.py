# Generated by Django 4.0.4 on 2022-05-29 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0003_pagofinanciamiento_pagomantenimiento'),
        ('monitoreo', '0002_remove_resumenpago_condicionespago_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagomantenimiento',
            name='numeroCuotaEstadoCuenta',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='monitoreo.cuotaestadocuenta'),
        ),
        migrations.AddField(
            model_name='pagofinanciamiento',
            name='numeroCuotaEstadoCuenta',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='monitoreo.cuotaestadocuenta'),
        ),
    ]
