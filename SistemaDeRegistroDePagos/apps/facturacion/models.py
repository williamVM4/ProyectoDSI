from math import fabs
from django.db import models
from django.contrib.auth.models import User
from crum import get_current_user

pago_tipo = [
    (1, 'Efectivo'),
    (2, 'Banco')
]

class pago(models.Model):
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    prima = models.ForeignKey('prima', on_delete=models.CASCADE, null=True)
    pagoFinanciamiento = models.ForeignKey('pagoFinanciamiento', on_delete=models.CASCADE, null=True)
    pagoMantenimiento = models.ForeignKey('pagoMantenimiento', on_delete=models.CASCADE, null=True)
    tipoPago = models.IntegerField(
        null=False, blank=False,
        choices=pago_tipo
    )
    referencia = models.CharField(max_length=100, blank=True, default="")
    cuentaBancaria = models.ForeignKey('inventario.cuentaBancaria',blank=True, null = True, on_delete=models.CASCADE)
    fechaPago = models.DateField()
    observaciones = models.TextField(max_length=200,default="")
    
# Create your models here.
class prima(models.Model):
    numeroReciboPrima = models.CharField(max_length=10, primary_key=True)
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, on_delete=models.CASCADE)
    usuarioCreacion = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null = True, related_name='user_creation_prima')
    conceptoPrima = models.CharField(max_length=50)

    def __str__(self):
        return self.numeroReciboPrima



class BasePagoModel(models.Model):
    conceptoOtros = models.CharField(max_length=100,blank=True, default="")
    montoOtros = models.DecimalField(blank=True,default=0,max_digits=8, decimal_places=2)
    numeroCuotaEstadoCuenta = models.ForeignKey('monitoreo.cuotaEstadoCuenta',blank=True, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True

class pagoFinanciamiento(BasePagoModel):
    numeroReciboFinanciamiento = models.CharField(max_length=30, primary_key=True)
    usuarioCreacion = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null = True, related_name='user_creation_financiamiento')
    mantenimiento = models.DecimalField(max_digits=8, decimal_places=2)
    comision = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return self.numeroReciboFinanciamiento

    def save(self, force_insert=False, force_update=False,using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation_financiamiento = user
        super(pagoFinanciamiento,self).save()

class pagoMantenimiento(BasePagoModel):
    numeroReciboMantenimiento = models.CharField(max_length=30, primary_key=True)
    usuarioCreacion = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null = True, related_name='user_creation_mantenimiento')

    def __str__(self):
        return self.numeroReciboMantenimiento




