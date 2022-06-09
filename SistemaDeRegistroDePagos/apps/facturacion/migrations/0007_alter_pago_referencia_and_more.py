# Generated by Django 4.0.4 on 2022-06-09 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0006_alter_pago_referencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='referencia',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='pagofinanciamiento',
            name='conceptoOtros',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='pagofinanciamiento',
            name='montoOtros',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='pagomantenimiento',
            name='conceptoOtros',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='pagomantenimiento',
            name='montoOtros',
            field=models.FloatField(blank=True, default=0),
        ),
    ]