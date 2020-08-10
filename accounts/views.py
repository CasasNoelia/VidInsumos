from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'accounts/dashboard.html')

def productos(request):
    return render(request, 'accounts/productos.html')

def cliente(request):
    return render(request, 'accounts/cliente.html')
