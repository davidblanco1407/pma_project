from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegistroUsuarioForm
from django.contrib.auth.forms import AuthenticationForm

# Vista de Registro de Usuario
def registro(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("home")
    else:
        form = RegistroUsuarioForm()
    return render(request, "usuarios/registro.html", {"form": form})

# Vista de Inicio de Sesión
def inicio_sesion(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect("home")
        else:
            # Agregar un mensaje de error si las credenciales son incorrectas
            messages.error(request, "Usuario o contraseña incorrectos.")
    # Si el método es GET o la autenticación falla, renderiza el formulario de login
    form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})

# Vista de Home
def home(request):
    return render(request, "home.html")
