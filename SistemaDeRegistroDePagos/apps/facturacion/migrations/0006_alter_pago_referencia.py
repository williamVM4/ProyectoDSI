# Generated by Django 4.0.4 on 2022-06-09 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0005_alter_pago_tipopago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='referencia',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]