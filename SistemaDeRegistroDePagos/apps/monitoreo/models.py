from django.db import models

# Create your models here.
class condicionesPago(models.Model):
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, on_delete=models.CASCADE)
    fechaEscrituracion = models.DateField()
    montoFinanciamiento = models.FloatField()
    plazo = models.IntegerField()
    tasaInteres = models.FloatField()
    cuotaKi = models.FloatField()
    comisionCuota = models.FloatField()
    mantenimientoCuota = models.FloatField()
    multaMantenimiento = models.FloatField()
    multaFinanciamiento = models.FloatField()

    def __str__(self):
        return self.detalleVenta

class resumenPago(models.Model):
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, null=True ,on_delete=models.CASCADE)
    fechaUltimoPago = models.DateField()
    fechaUltimoCorte = models.DateField()
    saldoCapital = models.FloatField()
    fechaCancelado = models.DateField()
    descuentoPP = models.FloatField()
    prima = models.FloatField()
    abonosCapital = models.FloatField()
    abonosComision = models.FloatField()
    abonosRecargo = models.FloatField()
    abonosOtros = models.FloatField()
    abonosIntereses = models.FloatField()
    abonosMantenimiento = models.FloatField()


class tablaAmortizacion(models.Model):
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, null=True, on_delete=models.CASCADE)

class cuotaAmortizacion(models.Model):
    numeroCuota = models.IntegerField(primary_key=True)
    tablaAmortizacion = models.ForeignKey(tablaAmortizacion, on_delete=models.CASCADE)
    fechaPago = models.DateField()
    diasInteres = models.IntegerField()
    montoCancelado = models.FloatField()
    tasaInteres = models.FloatField()
    interesGenerado = models.FloatField()
    interesPagado = models.FloatField()
    comision = models.FloatField()
    mantenimiento = models.FloatField()
    subTotal = models.FloatField()
    abonoCapital = models.FloatField()
    saldoCapital = models.FloatField()
    saldoInteres = models.FloatField()
    def __str__(self):
        return self.numeroCuota

class estadoCuenta(models.Model):
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, null=True, on_delete=models.CASCADE)

class cuotaEstadoCuenta(models.Model):
    numeroCuota = models.IntegerField(primary_key=True)
    estadoCuenta = models.ForeignKey(estadoCuenta, on_delete=models.CASCADE)
    diasInteres = models.IntegerField()
    tasaInteres = models.FloatField()
    interesGenerado = models.FloatField()
    interesPagado = models.FloatField()
    subTotal = models.FloatField()
    abonoCapital = models.FloatField()
    saldoCapital = models.FloatField()
    saldoInteres = models.FloatField()
    def __str__(self):
        return self.numeroCuota