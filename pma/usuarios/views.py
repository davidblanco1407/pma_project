from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegistroUsuarioForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Vista de Registro de Usuario
def registro(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "¡Registro exitoso! Has iniciado sesión correctamente.")
            return redirect("home")
        else:
            # Mensajes de error si el formulario no es válido
            messages.error(request, "Hubo un problema al registrar al usuario. Por favor, revisa los datos ingresados.")
    else:
        form = RegistroUsuarioForm()
    return render(request, "registration/register.html", {"form": form})

# Vista de Home
@login_required  # Aseguramos que solo los usuarios autenticados puedan acceder a esta vista
def home(request):
    return render(request, "home.html")
