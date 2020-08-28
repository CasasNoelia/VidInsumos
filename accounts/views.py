from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import PedidoForm, CreateUserForm, ClienteForm
from .decorators import unauthenticated_user, allowed_users, admin_only


def tienda(request):
    productos = Productos.objects.all()
    context = {'productos': productos}
    return render(request, 'accounts/tienda.html', context)


def carrito(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, creacion = Pedido.objects.get_or_create(cliente=cliente, completo=False)
        items = pedido.pedidoitem_set.all()
    else:
        # Create empty cart for now for non-logged in user
        items = []

    context = {'items': items}
    return render(request, 'accounts/carrito.html', context)


def confirmacion(request):
    context = {}
    return render(request, 'accounts/confirmacion.html', context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='Cliente')
            user.groups.add(group)
            Cliente.objects.create(user=user, )

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
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


# @login_required(login_url='login')
# @admin_only
def home(request):
    pedido = Pedido.objects.all()
    cliente = Cliente.objects.all()

    total_cliente = cliente.count()

    total_pedido = pedido.count()
    entregado = pedido.filter(status='Entregado').count()
    pendiente = pedido.filter(status='Pendiente').count()

    context = {'pedido': pedido, 'cliente': cliente, 'total_cliente': total_cliente, 'total_pedido': total_pedido,
               'entregado': entregado, 'pendiente': pendiente}
    return render(request, 'accounts/dashboard.html', context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['Cliente'])
def userPage(request):
    pedido = request.user.cliente.pedido_set.all()

    total_pedido = pedido.count()
    entregado = pedido.filter(status='Entregado').count()
    pendiente = pedido.filter(status='Pendiente').count()

    print('PEDIDO:', pedido)

    context = {'pedido': pedido, 'total_pedido': total_pedido, 'entregado': entregado, 'pendiente': pendiente}

    return render(request, 'accounts/user.html', context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['Cliente'])
def perfilEditar(request):
    cliente = request.user.cliente
    form = ClienteForm(instance=cliente)

    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/perfil_editar.html', context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['Admin'])
def productos(request):
    productos = Productos.objects.all()
    return render(request, 'accounts/productos.html', {'productos': productos})


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['Cliente', 'Admin'])
def cliente(request, pk_test):
    cliente = Cliente.objects.get(id=pk_test)

    pedido = cliente.pedido_set.all()
    pedido_count = pedido.count()

    context = {'cliente': cliente, 'pedido': pedido, 'pedido_count': pedido_count}
    return render(request, 'accounts/cliente.html', context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['Admin', 'Cliente'])
def crearPedido(request, pk):
    PedidoFormSet = inlineformset_factory(Cliente, Pedido, fields=('productos', 'status'), extra=6)
    cliente = Cliente.objects.get(id=pk)
    formset = PedidoFormSet(queryset=Pedido.objects.none(), instance=cliente)
    # form = PedidoForm(initial={'cliente': cliente})
    if request.method == 'POST':
        formset = PedidoFormSet(request.POST, instance=cliente)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'accounts/pedido_form.html', context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['Admin', 'Cliente'])
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


# @login_required(login_url='login')
# allowed_users(allowed_roles=['Admin', 'Cliente'])
def eliminarPedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    if request.method == "POST":
        pedido.delete()
        return redirect('/')

    context = {'item': pedido}
    return render(request, 'accounts/eliminar.html', context)
