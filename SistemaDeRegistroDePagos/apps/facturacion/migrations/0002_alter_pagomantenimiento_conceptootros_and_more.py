# Generated by Django 4.0.4 on 2022-06-07 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagomantenimiento',
            name='conceptoOtros',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='pagomantenimiento',
            name='montoOtros',
            field=models.FloatField(blank=True),
        ),
    ]
