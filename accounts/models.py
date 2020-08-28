from django.db import models
from django.contrib.auth.models import User

# Create your models here. Cambio de name x nombre en Cliente

class Cliente(models.Model):
    user = models.OneToOneField(User, null=True,  on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, null=True)
    tel = models.CharField(max_length=200, null=True)
    direccion = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nombre


class Vendedor(models.Model):
    nombre = models.CharField(max_length=200, null=True)
    tel = models.CharField(max_length=200, null=True)
    RUT = models.CharField(max_length=200, null=True)
    direccion = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    #def __str__(self):
        #return self.nombre

class Productos(models.Model):

    CATEGORIA = (
        ('Limpieza', 'Limpieza'),
        ('Proteccion','Proteccion'),
    )
    nombre = models.CharField(max_length=200, null=True)
    precio = models.FloatField(null=True)
    categoria = models.CharField(max_length=200, null=True, choices=CATEGORIA)
    digital = models.BooleanField(default=False,null=True, blank=True)
    marca = models.CharField(max_length=200, null=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    imagen = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):


    STATUS = (
        ('Pendiente', 'Pendiente'),
        ('Pronto para entrega','Pronto para entrega'),
        ('Entregado', 'Entregado'),
    )

    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL)
    vendedor = models.ForeignKey(Vendedor, null=True, on_delete=models.SET_NULL)
    completo = models.BooleanField(default=False)
    transaccion_id = models.CharField(max_length=100, null=True)
    productos = models.ForeignKey(Productos, null=True, on_delete=models.SET_NULL)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    #def __str__(self):
        #return str(self.id)

    #cambie return self.productos.name X return str(self.id)

    @property
    def get_carrito_total(self):
        pedidoitems = self.pedidoitem_set.all()
        total = sum([item.get_total for item in pedidoitems])
        return total

    @property
    def get_carrito_items(self):
        pedidoitems = self.pedidoitem_set.all()
        total = sum([item.cantidad for item in pedidoitems])
        return total

class PedidoItem(models.Model):

    productos = models.ForeignKey(Productos, null=True, on_delete=models.SET_NULL)
    pedido = models.ForeignKey(Pedido, null=True, on_delete=models.SET_NULL)
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def get_total(self):
        total = self.productos.precio * self.cantidad
        return total


class Envio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
    direccion = models.CharField(max_length=200, null=False)
    ciudad = models.CharField(max_length=200, null=False)
    estado = models.CharField(max_length=200, null=False)
    codigo_postal = models.CharField(max_length=200, null=False)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.direccion


@property
def imagenURL(self):
	try:
	    url = self.imagen.url
	except:
		url = ''
	return url




