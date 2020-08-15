from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
#'Pendiente' 'Pronto para entrega''Entregado'

def home(request):
    pedido = Pedido.objects.all()
    cliente = Cliente.objects.all()

    total_cliente = cliente.count()
    total_pedido = pedido.count()
    entregado = pedido.filter(status='Entregado').count()
    pendiente = pedido.filter(status='Pendiente').count()

    context = {'pedido': pedido, 'cliente': cliente,'total_cliente': total_cliente,'total_pedido': total_pedido, 'entregado': entregado, 'pendiente': pendiente }
    return render(request, 'accounts/dashboard.html', context)

def productos(request):
    productos = Productos.objects.all()
    return render(request, 'accounts/productos.html', {'productos': productos})

def cliente(request, pk_test):
    cliente = Cliente.objects.get(id=pk_test)

    pedido = cliente.pedido_set.all()
    pedido_count = pedido.count()

    context = {'cliente': cliente, 'pedido': pedido, 'pedido_count': pedido_count}
    return render(request, 'accounts/cliente.html',context)

def crearPedido(request):

    context = {}
    return render(request, 'accounts/pedido_form.html', context)