from django.db import models

# Create your models here.
class condicionesPago(models.Model):
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, on_delete=models.CASCADE)
    fechaEscrituracion = models.DateField()
    montoFinanciamiento = models.DecimalField(max_digits=8, decimal_places=2)
    plazo = models.IntegerField()
    tasaInteres = models.DecimalField(max_digits=8, decimal_places=2)
    cuotaKi = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    comisionCuota = models.DecimalField(max_digits=8, decimal_places=2)
    mantenimientoCuota = models.DecimalField(max_digits=8, decimal_places=2)
    multaMantenimiento = models.DecimalField(max_digits=8, decimal_places=2)
    multaFinanciamiento = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.detalleVenta

class resumenPago(models.Model):
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, on_delete=models.CASCADE)
    fechaUltimoPago = models.DateField()
    fechaUltimoCorte = models.DateField()
    saldoCapital = models.DecimalField(max_digits=8, decimal_places=2)
    fechaCancelado = models.DateField()
    descuentoPP = models.DecimalField(max_digits=8, decimal_places=2)
    prima = models.DecimalField(max_digits=8, decimal_places=2)
    abonosCapital = models.DecimalField(max_digits=8, decimal_places=2)
    abonosComision = models.DecimalField(max_digits=8, decimal_places=2)
    abonosRecargo = models.DecimalField(max_digits=8, decimal_places=2)
    abonosOtros = models.DecimalField(max_digits=8, decimal_places=2)
    abonosIntereses = models.DecimalField(max_digits=8, decimal_places=2)
    abonosMantenimiento = models.DecimalField(max_digits=8, decimal_places=2)


class tablaAmortizacion(models.Model):
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, on_delete=models.CASCADE)

class cuotaAmortizacion(models.Model):
    numeroCuota = models.IntegerField(primary_key=True)
    tablaAmortizacion = models.ForeignKey(tablaAmortizacion, on_delete=models.CASCADE)
    fechaPago = models.DateField()
    diasInteres = models.IntegerField()
    montoCancelado = models.DecimalField(max_digits=8, decimal_places=2)
    tasaInteres = models.DecimalField(max_digits=8, decimal_places=2)
    interesGenerado = models.DecimalField(max_digits=8, decimal_places=2)
    interesPagado = models.DecimalField(max_digits=8, decimal_places=2)
    comision = models.DecimalField(max_digits=8, decimal_places=2)
    subTotal = models.DecimalField(max_digits=8, decimal_places=2)
    abonoCapital = models.DecimalField(max_digits=8, decimal_places=2)
    saldoCapital = models.DecimalField(max_digits=8, decimal_places=2)
    saldoInteres = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return self.numeroCuota

class estadoCuenta(models.Model):
    condicionesPago = models.ForeignKey(condicionesPago,blank=True, on_delete=models.CASCADE)
    fechaRegistro=models.DateField(auto_now_add=True,blank=True)
    nombre = models.CharField(max_length=20,blank=True)