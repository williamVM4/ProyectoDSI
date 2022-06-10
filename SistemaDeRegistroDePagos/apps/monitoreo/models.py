from django.db import models

# Create your models here.
class condicionesPago(models.Model):
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, on_delete=models.CASCADE)
    fechaEscrituracion = models.DateField()
    montoFinanciamiento = models.DecimalField(max_digits=8, decimal_places=6)
    plazo = models.IntegerField()
    tasaInteres = models.DecimalField(max_digits=8, decimal_places=6)
    cuotaKi = models.DecimalField(max_digits=8, decimal_places=6)
    comisionCuota = models.DecimalField(max_digits=8, decimal_places=6)
    mantenimientoCuota = models.DecimalField(max_digits=8, decimal_places=6)
    multaMantenimiento = models.DecimalField(max_digits=8, decimal_places=6)
    multaFinanciamiento = models.DecimalField(max_digits=8, decimal_places=6)

    def __str__(self):
        return self.detalleVenta

class resumenPago(models.Model):
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, on_delete=models.CASCADE)
    fechaUltimoPago = models.DateField()
    fechaUltimoCorte = models.DateField()
    saldoCapital = models.DecimalField(max_digits=8, decimal_places=6)
    fechaCancelado = models.DateField()
    descuentoPP = models.DecimalField(max_digits=8, decimal_places=6)
    prima = models.DecimalField(max_digits=8, decimal_places=6)
    abonosCapital = models.DecimalField(max_digits=8, decimal_places=6)
    abonosComision = models.DecimalField(max_digits=8, decimal_places=6)
    abonosRecargo = models.DecimalField(max_digits=8, decimal_places=6)
    abonosOtros = models.DecimalField(max_digits=8, decimal_places=6)
    abonosIntereses = models.DecimalField(max_digits=8, decimal_places=6)
    abonosMantenimiento = models.DecimalField(max_digits=8, decimal_places=6)


class tablaAmortizacion(models.Model):
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, on_delete=models.CASCADE)

class cuotaAmortizacion(models.Model):
    numeroCuota = models.IntegerField(primary_key=True)
    tablaAmortizacion = models.ForeignKey(tablaAmortizacion, on_delete=models.CASCADE)
    fechaPago = models.DateField()
    diasInteres = models.IntegerField()
    montoCancelado = models.DecimalField(max_digits=8, decimal_places=6)
    tasaInteres = models.DecimalField(max_digits=8, decimal_places=6)
    interesGenerado = models.DecimalField(max_digits=8, decimal_places=6)
    interesPagado = models.DecimalField(max_digits=8, decimal_places=6)
    comision = models.DecimalField(max_digits=8, decimal_places=6)
    mantenimiento = models.DecimalField(max_digits=8, decimal_places=6)
    subTotal = models.DecimalField(max_digits=8, decimal_places=6)
    abonoCapital = models.DecimalField(max_digits=8, decimal_places=6)
    saldoCapital = models.DecimalField(max_digits=8, decimal_places=6)
    saldoInteres = models.DecimalField(max_digits=8, decimal_places=6)
    def __str__(self):
        return self.numeroCuota

class estadoCuenta(models.Model):
    detalleVenta = models.ForeignKey('inventario.detalleVenta',blank=True, on_delete=models.CASCADE)

class cuotaEstadoCuenta(models.Model):
    numeroCuota = models.IntegerField()
    estadoCuenta = models.ForeignKey(estadoCuenta, on_delete=models.CASCADE)
    cuotaAmortizacion = models.ForeignKey(cuotaAmortizacion, on_delete=models.CASCADE, null=True)
    diasInteres = models.IntegerField()
    tasaInteres = models.DecimalField(max_digits=8, decimal_places=6)
    interesGenerado = models.DecimalField(max_digits=8, decimal_places=6)
    interesPagado = models.DecimalField(max_digits=8, decimal_places=6)
    subTotal = models.DecimalField(max_digits=8, decimal_places=6)
    abonoCapital = models.DecimalField(max_digits=8, decimal_places=6)
    saldoCapital = models.DecimalField(max_digits=8, decimal_places=6)
    saldoInteres = models.DecimalField(max_digits=8, decimal_places=6)
    def __str__(self):
        return self.numeroCuota