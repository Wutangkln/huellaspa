# spa/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('editar_producto/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('login/', views.iniciar_sesion, name='login'), 
    path('logout/', views.cerrar_sesion, name='logout'),
    path('signup/', views.registrarse, name='signup'),
]
