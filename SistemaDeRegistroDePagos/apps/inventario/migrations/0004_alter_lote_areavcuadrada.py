# Generated by Django 4.0.4 on 2022-06-11 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_alter_lote_areamcuadrado_alter_lote_areavcuadrada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='areaVCuadrada',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8),
        ),
    ]
