# Generated by Django 4.0.4 on 2022-07-19 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propietario',
            name='dui',
            field=models.CharField(max_length=9),
        ),
    ]