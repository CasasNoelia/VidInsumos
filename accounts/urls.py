from django.urls import path
from .import views

urlpatterns = [

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),

    path('accounts/', views.perfilEditar, name="accounts"),

    path('productos/', views.productos, name='productos'),
    path('cliente/<str:pk_test>/', views.cliente, name="cliente"),

    path('crear_pedido/<str:pk>/', views.crearPedido, name="crear_pedido"),
    path('actualizar_pedido/<str:pk>/', views.actualizarPedido, name="actualizar_pedido"),
    path('eliminar_pedido/<str:pk>/', views.eliminarPedido, name="eliminar_pedido"),
]