# spa/views.py

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Producto
from .forms import ProductoForm, BusquedaForm

def inicio(request):
    productos = Producto.objects.all()

    # Filtrado por categoría
    categoria = request.GET.get('categoria')
    if categoria:
        productos = productos.filter(categoria__icontains=categoria)

    # Búsqueda por nombre o descripción
    busqueda_form = BusquedaForm(request.GET)
    if busqueda_form.is_valid():
        busqueda = busqueda_form.cleaned_data['busqueda']
        if busqueda:
            productos = productos.filter(
                Q(nombre__icontains=busqueda) | Q(descripcion__icontains=busqueda)
            )

    return render(request, 'inicio.html', {'productos': productos, 'busqueda_form': busqueda_form})

@login_required(login_url='login')
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect('inicio')
    else:
        form = ProductoForm()

    return render(request, 'agregar_producto.html', {'form': form})

@login_required(login_url='login')
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('inicio')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

@login_required(login_url='login')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('inicio')

    return render(request, 'eliminar_producto.html', {'producto': producto})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido, {username}. Has iniciado sesión correctamente.')
                return redirect('inicio')
            else:
                messages.error(request, 'Error de inicio de sesión. Por favor, verifica tu nombre de usuario y contraseña.')
        else:
            messages.error(request, 'Error de inicio de sesión. Por favor, verifica tu nombre de usuario y contraseña.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('inicio')

def registrarse(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Te has registrado exitosamente.')
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
