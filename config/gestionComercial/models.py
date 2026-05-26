from django.db import models
from django.contrib.auth.models import User


class Producto(models.Model):

    codigo = models.CharField(
        max_length=50,
        unique=True
    )

    nombre = models.CharField(
        max_length=200
    )

    precioVenta = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    controlaStock = models.BooleanField(default=True)

    stock = models.IntegerField(default=0)

    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Cliente(models.Model):

    nombre = models.CharField(max_length=200)

    dni = models.CharField(
        max_length=20,
        unique=True
    )

    telefono = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.dni}"


class Venta(models.Model):

    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
        ('transferencia', 'Transferencia'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    metodo_pago = models.CharField(
        max_length=50,
        choices=METODOS_PAGO
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"Venta #{self.id}"


class DetalleVenta(models.Model):

    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    cantidad = models.IntegerField()

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.producto.nombre}"