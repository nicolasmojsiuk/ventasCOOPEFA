from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = "Usuario o contraseña incorrectos"

    return render(request, 'login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')  # después de logout vuelve al login

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def vendedores(request):
    return render(request, "vendedores.html")
@login_required(login_url='login')
def clientes(request):
    return render(request, "clientes.html")
@login_required(login_url='login')
def caja(request):
    return render(request, "caja.html")
@login_required(login_url='login')
def ventas(request):
    return render(request, "ventas.html")
@login_required(login_url='login')
def presupuestos(request):
    return render(request, "presupuestos.html")
@login_required(login_url='login')
def informes(request):
    return render(request, "informes.html")
@login_required(login_url='login')
def ajustes(request):
    return render(request, "ajustes.html")