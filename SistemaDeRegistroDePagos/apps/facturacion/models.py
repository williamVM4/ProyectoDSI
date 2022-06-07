from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class prima(models.Model):
    numeroReciboPrima = models.CharField(max_length=10, primary_key=True)
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, on_delete=models.CASCADE)
    fechaPrima = models.DateField()
    montoPrima = models.FloatField()
    conceptoPrima = models.CharField(max_length=50)

    def __str__(self):
        return self.numeroReciboPrima

class BasePagoModel(models.Model):
    usuarioCreacion = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True, null = True)
    conceptoOtros = models.CharField(max_length=100,blank=True)
    montoOtros = models.FloatField(blank=True)
    fechaPago = models.DateField()
    numeroCuotaEstadoCuenta = models.ForeignKey('monitoreo.cuotaEstadoCuenta',blank=True, on_delete=models.CASCADE)
    monto = models.FloatField()
    tipoPago = models.CharField(max_length=100)
    class Meta:
        abstract = True

class pagoFinanciamiento(BasePagoModel):
    numeroReciboFinanciamiento = models.CharField(max_length=30, primary_key=True)
    mantenimiento = models.FloatField()
    comision = models.FloatField()
    
    def __str__(self):
        return self.numeroReciboFinanciamiento

class pagoMantenimiento(BasePagoModel):
    numeroReciboMantenimiento = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.numeroReciboMantenimiento



