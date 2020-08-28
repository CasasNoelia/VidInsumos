from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Cliente)
admin.site.register(Vendedor)
admin.site.register(Productos)
admin.site.register(Pedido)
admin.site.register(PedidoItem)
admin.site.register(Envio)
