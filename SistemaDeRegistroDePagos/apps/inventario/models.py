from pyexpat import model
from django.db import models

class proyectoTuristico(models.Model):
    nombreProyectoTuristico = models.CharField(max_length=50)
    empresa = models.CharField(max_length=30)

    def __str__(self):
        return self.nombreProyectoTuristico

class cuentaBancaria(models.Model):
    numeroCuentaBancaria = models.CharField(max_length=30, primary_key=True)
    proyectoTuristico = models.ForeignKey(proyectoTuristico, on_delete=models.CASCADE)
    nombreCuentaBancaria = models.CharField(max_length=50)
    tipoCuenta = models.CharField(max_length=30)
    banco = models.CharField(max_length=30)

    def __str__(self):
        return self.nombreCuentaBancaria

class lote(models.Model):
    matriculaLote = models.CharField(max_length=50, primary_key=True)
    proyectoTuristico = models.ForeignKey(proyectoTuristico, on_delete=models.CASCADE)
    numeroLote = models.IntegerField()
    poligono = models.CharField(max_length=50)
    areaMtCuadrado = models.FloatField()
    areaVCuadrada = models.FloatField()

    def __str__(self):
        return self.matriculaLote

class propietario(models.Model):
    nombrePropietario = models.CharField(max_length=50, primary_key=True)
    direccion = models.CharField(max_length=50)
    profesion = models.CharField(max_length=50)
    trabajo = models.CharField(max_length=30,blank=True,null=True)
    direccionTrabajo = models.CharField(max_length=30,blank=True,null=True)
    telefonoTrabajo = models.IntegerField(blank=True,null=True)
    telefonoCasa = models.IntegerField(blank=True,null=True)
    telefonoCelular = models.IntegerField()
    correoElectronico = models.EmailField(max_length=254,blank=True,null=True)
    eliminado = models.BooleanField()

    def __str__(self):
        return self.nombrePropietario

class detalleVenta(models.Model):
    lote = models.ForeignKey(lote, on_delete=models.CASCADE)
    precioVenta = models.FloatField(blank=True,null=True)
    descuento = models.FloatField(blank=True,null=True)
    estado = models.BooleanField()
    
    def __str__(self):
        return self.lote

class asignacionLote(models.Model):
    propietario = models.ForeignKey(propietario, on_delete=models.CASCADE)
    detalleVenta = models.ForeignKey(detalleVenta, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('propietario', 'detalleVenta')

    def __str__(self):
        return '%s %s' % (self.propietario, self.detalleVenta)



