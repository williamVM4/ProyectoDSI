from django.db import models


# Create your models here.
class prima(models.Model):
    numeroReciboPrima = models.CharField(max_length=10, primary_key=True)
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, on_delete=models.CASCADE)
    fechaPrima = models.DateField()
    montoPrima = models.FloatField()
    conceptoPrima = models.CharField(max_length=50)

    def __str__(self):
        return self.numeroReciboPrima

class pagoFinanciamiento(models.Model):
    numeroReciboFinanciamiento = models.CharField(max_length=30, primary_key=True)
    numeroCuotaEstadoCuenta = models.ForeignKey('monitoreo.cuotaEstadoCuenta',blank=True, on_delete=models.CASCADE)
    fechaPago = models.DateField()
    monto = models.FloatField()
    mantenimiento = models.FloatField()
    comision = models.FloatField()
    conceptoOtros = models.CharField(max_length=50)
    montoOtros = models.FloatField()

    def __str__(self):
        return self.numeroReciboFinanciamiento

class pagoMantenimiento(models.Model):
    numeroReciboMantenimiento = models.CharField(max_length=30, primary_key=True)
    numeroCuotaEstadoCuenta = models.ForeignKey('monitoreo.cuotaEstadoCuenta',blank=True, on_delete=models.CASCADE)
    fechaPago = models.DateField()
    monto = models.FloatField()
    conceptoOtros = models.CharField(max_length=50)
    montoOtros = models.FloatField()

    def __str__(self):
        return self.numeroReciboFinanciamiento



