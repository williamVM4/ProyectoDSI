# Generated by Django 4.0.4 on 2022-06-02 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_alter_detalleventa_descuento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacionlote',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
    ]
