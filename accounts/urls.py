from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name="home"),
    path('productos/', views.productos, name='productos'),
    path('cliente/<str:pk_test>/', views.cliente, name="cliente"),
    path('crear_pedido/', views.crearPedido, name="crear_pedido"),
]