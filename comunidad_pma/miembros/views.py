from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Miembro, Sancion, SolicitudCorreccion
from .forms import MiembroForm, SancionForm

class SoloStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

def home(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        miembro = Miembro.objects.filter(email=correo).first()
        if miembro:
            return render(request, "miembros/verificacion_resultado.html", {"miembro": miembro})
        else:
            messages.error(request, "No se encontró ningún miembro con ese correo.")
    return render(request, "miembros/home.html")

def solicitar_correccion(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if request.method == "POST":
        descripcion = request.POST.get("descripcion")
        SolicitudCorreccion.objects.create(miembro=miembro, descripcion=descripcion)
        messages.success(request, "Tu solicitud fue enviada correctamente.")
        return redirect("home")
    return render(request, "miembros/solicitud_correccion.html", {"miembro": miembro})

# Vistas CRUD protegidas con SoloStaffMixin
class ListaMiembrosView(SoloStaffMixin, ListView):
    model = Miembro
    template_name = 'miembros/lista_miembros.html'
    context_object_name = 'miembros'

class CrearMiembroView(SoloStaffMixin, CreateView):
    model = Miembro
    form_class = MiembroForm
    template_name = 'miembros/formulario_miembro.html'
    success_url = reverse_lazy('miembros:lista_miembros')

class EditarMiembroView(SoloStaffMixin, UpdateView):
    model = Miembro
    form_class = MiembroForm
    template_name = 'miembros/formulario_miembro.html'
    success_url = reverse_lazy('miembros:lista_miembros')

class EliminarMiembroView(SoloStaffMixin, DeleteView):
    model = Miembro
    template_name = 'miembros/eliminar_miembro.html'
    success_url = reverse_lazy('miembros:lista_miembros')

class DetalleMiembroView(SoloStaffMixin, DetailView):
    model = Miembro
    template_name = 'miembros/detalle_miembro.html'

class CrearSancionView(SoloStaffMixin, CreateView):
    model = Sancion
    form_class = SancionForm
    template_name = 'miembros/formulario_sancion.html'

    # Método para pasar el pk del miembro al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')  # Pasamos el pk al contexto
        return context

    # Guardamos la sanción asociada al miembro usando el pk
    def form_valid(self, form):
        form.instance.miembro_id = self.kwargs['pk']
        return super().form_valid(form)

    # Redirigimos al detalle del miembro después de crear la sanción
    def get_success_url(self):
        return reverse_lazy('miembros:detalle_miembro', kwargs={'pk': self.kwargs['pk']})
