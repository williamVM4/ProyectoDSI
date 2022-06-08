from django.db import models
from django.conf import settings
from crum import get_current_user

# Create your models here.
class prima(models.Model):
    numeroReciboPrima = models.CharField(max_length=10, primary_key=True)
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, on_delete=models.CASCADE)
    tipoPago = models.CharField(max_length=100)
    referencia = models.CharField(max_length=100, blank=True)
    cuentaBancaria = models.ForeignKey('inventario.cuentaBancaria',blank=True, null = True, on_delete=models.CASCADE)
    usuarioCreacion = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True, null = True, related_name='user_creation_prima')
    fechaPrima = models.DateField()
    montoPrima = models.FloatField()
    conceptoPrima = models.CharField(max_length=50)

    def __str__(self):
        return self.numeroReciboPrima

    def save(self, force_insert=False, force_update=False,using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation_prima = user
        super(prima,self).save()

class BasePagoModel(models.Model):
    conceptoOtros = models.CharField(max_length=100,blank=True)
    montoOtros = models.FloatField(blank=True)
    fechaPago = models.DateField()
    numeroCuotaEstadoCuenta = models.ForeignKey('monitoreo.cuotaEstadoCuenta',blank=True, on_delete=models.CASCADE)
    monto = models.FloatField()
    tipoPago = models.CharField(max_length=100)
    referencia = models.CharField(max_length=100, blank=True)
    cuentaBancaria = models.ForeignKey('inventario.cuentaBancaria',blank=True, null = True, on_delete=models.CASCADE)
    class Meta:
        abstract = True

class pagoFinanciamiento(BasePagoModel):
    numeroReciboFinanciamiento = models.CharField(max_length=30, primary_key=True)
    usuarioCreacion = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True, null = True, related_name='user_creation_financiamiento')
    mantenimiento = models.FloatField()
    comision = models.FloatField()
    
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
    usuarioCreacion = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True, null = True, related_name='user_creation_mantenimiento')

    def __str__(self):
        return self.numeroReciboMantenimiento

    def save(self, force_insert=False, force_update=False,using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation_mantenimiento = user
        super(pagoMantenimiento,self).save()



