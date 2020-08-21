
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import PedidoForm, CreateUserForm


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def home(request):
    pedido = Pedido.objects.all()
    cliente = Cliente.objects.all()

    total_cliente = cliente.count()
    total_pedido = pedido.count()
    entregado = pedido.filter(status='Entregado').count()
    pendiente = pedido.filter(status='Pendiente').count()

    context = {'pedido': pedido, 'cliente': cliente,'total_cliente': total_cliente,'total_pedido': total_pedido, 'entregado': entregado, 'pendiente': pendiente }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def productos(request):
    productos = Productos.objects.all()
    return render(request, 'accounts/productos.html', {'productos': productos})


@login_required(login_url='login')
def cliente(request, pk_test):
    cliente = Cliente.objects.get(id=pk_test)

    pedido = cliente.pedido_set.all()
    pedido_count = pedido.count()



    context = {'cliente': cliente, 'pedido': pedido, 'pedido_count': pedido_count}
    return render(request, 'accounts/cliente.html',context)

@login_required(login_url='login')
def crearPedido(request, pk):
    PedidoFormSet = inlineformset_factory(Cliente, Pedido, fields=('productos', 'status'), extra=6)
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

@login_required(login_url='login')
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


@login_required(login_url='login')
def eliminarPedido(request,pk):
    pedido = Pedido.objects.get(id=pk)
    if request.method == "POST":
        pedido.delete()
        return redirect('/')

    context = {'item': pedido}
    return render(request, 'accounts/eliminar.html', context)