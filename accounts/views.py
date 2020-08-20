from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import PedidoForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import PedidoForm

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

def crearPedido(request, pk):
    PedidoFormSet = inlineformset_factory(Cliente, Pedido, fields=('productos', 'status'), extra=10)
    cliente = Cliente.objects.get(id=pk)
    formset = PedidoFormSet(queryset=Pedido.objects.none(), instance=cliente)
    #form = PedidoForm(initial={'cliente': cliente})
    if request.method == 'POST':
        formset = PedidoFormSet(request.POST, instance=cliente)
        if formset.is_valid():
            formset.save()
            return redirect('/')


    context = {'form': formset}
    return render(request, 'accounts/pedido_form.html', context)


def actualizarPedido(request, pk):

    pedido = Pedido.objects.get(id=pk)
    form = PedidoForm(instance=pedido)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/pedido_form.html', context)

def eliminarPedido(request,pk):
    pedido = Pedido.objects.get(id=pk)
    if request.method == "POST":
        pedido.delete()
        return redirect('/')

    context = {'item': pedido}
    return render(request, 'accounts/eliminar.html', context)