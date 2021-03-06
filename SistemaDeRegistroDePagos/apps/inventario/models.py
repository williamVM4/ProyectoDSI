from django.db import models

class proyectoTuristico(models.Model):
    nombreProyectoTuristico = models.CharField(max_length=50)
    empresa = models.CharField(max_length=30)

    def __str__(self):
        return self.nombreProyectoTuristico

class cuentaBancaria(models.Model):
    numeroCuentaBancaria = models.CharField(max_length=20, primary_key=True)
    proyectoTuristico = models.ForeignKey(proyectoTuristico, on_delete=models.CASCADE)
    nombreCuentaBancaria = models.CharField(max_length=50)
    tipoCuenta = models.CharField(max_length=30)
    banco = models.CharField(max_length=30)

    def __str__(self):
        return self.nombreCuentaBancaria

class lote(models.Model):
    matriculaLote = models.CharField(max_length=50, primary_key=True)
    proyectoTuristico = models.ForeignKey(proyectoTuristico, on_delete=models.CASCADE,blank=True)
    numeroLote = models.CharField(max_length=3)
    poligono = models.CharField(max_length=2)
    identificador = models.CharField(max_length=5,blank=True)
    areaMCuadrado = models.DecimalField(max_digits=8, decimal_places=2)
    areaVCuadrada = models.DecimalField(max_digits=8, decimal_places=2, blank=True)

    def __str__(self):
        return self.identificador

class propietario(models.Model):
    dui = models.CharField(max_length=10)
    nombrePropietario = models.CharField(max_length=60)
    direccion = models.CharField(max_length=50)
    profesion = models.CharField(max_length=50)
    trabajo = models.CharField(max_length=50,blank=True,default="")
    direccionTrabajo = models.CharField(max_length=50,blank=True,default="")
    telefonoTrabajo = models.CharField(max_length=9,blank=True,default="")
    telefonoCasa = models.CharField(max_length=9,blank=True,default="")
    telefonoCelular = models.CharField(max_length=9)
    correoElectronico = models.EmailField(max_length=254,blank=True,default="")

    def __str__(self):
        return '%s %s' % (self.dui, self.nombrePropietario)

class detalleVenta(models.Model):
    lote = models.ForeignKey(lote, on_delete=models.CASCADE, blank=True)
    propietarios = models.ManyToManyField(propietario, through='asignacionLote')
    precioVenta = models.DecimalField(max_digits=8, decimal_places=2)
    descuento = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.lote.identificador

class asignacionLote(models.Model):
    propietario = models.ForeignKey(propietario, on_delete=models.CASCADE)
    detalleVenta = models.ForeignKey(detalleVenta, on_delete=models.CASCADE)
    eliminado = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('propietario', 'detalleVenta')

    def __str__(self):
        return '%s %s' % (self.propietario, self.detalleVenta)

class asignacionProyecto(models.Model):
    propietario = models.ForeignKey(propietario, on_delete=models.CASCADE)
    dui = models.CharField(max_length=10)
    proyectoTuristico = models.ForeignKey(proyectoTuristico, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('dui', 'proyectoTuristico')

    def __str__(self):
        return '%s' % (self.propietario)



