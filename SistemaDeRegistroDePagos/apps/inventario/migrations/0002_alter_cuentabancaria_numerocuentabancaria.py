# Generated by Django 4.0.4 on 2022-06-11 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuentabancaria',
            name='numeroCuentaBancaria',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
