from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    direccion = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Vendedor(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    RUT = models.CharField(max_length=200, null=True)
    direccion = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Productos(models.Model):

    CATEGORIA = (
        ('Limpieza', 'Limpieza'),
        ('Proteccion','Proteccion'),
    )
    name = models.CharField(max_length=200, null=True)
    precio = models.FloatField(null=True)
    categoria = models.CharField(max_length=200, null=True, choices=CATEGORIA)
    marca = models.CharField(max_length=200, null=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Pedido(models.Model):

    STATUS = (
        ('Pendiente', 'Pendiente'),
        ('Pronto para entrega','Pronto para entrega'),
        ('Entregado', 'Entregado'),
    )

    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL)
    vendedor = models.ForeignKey(Vendedor, null=True, on_delete=models.SET_NULL)
    productos = models.ForeignKey(Productos, null=True, on_delete=models.SET_NULL)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.productos.name