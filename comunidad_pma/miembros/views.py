from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

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

class ListaMiembrosView(SoloStaffMixin, ListView):
    model = Miembro
    template_name = 'miembros/lista_miembros.html'
    context_object_name = 'miembros'
    paginate_by = 10

    def get_queryset(self):
        queryset = Miembro.objects.all().order_by('nombre_completo')
        filtro = self.request.GET.get('filtro')
        puede_volver = self.request.GET.get('puede_volver')
        correo = self.request.GET.get('correo')

        if filtro == 'activos':
            queryset = queryset.filter(activo=True)
        elif filtro == 'inactivos':
            queryset = queryset.filter(activo=False)
            if puede_volver == 'si':
                queryset = queryset.filter(puede_regresar=True)
            elif puede_volver == 'no':
                queryset = queryset.filter(puede_regresar=False)

        if correo:
            queryset = queryset.filter(email__icontains=correo.strip())

        return queryset

def verificar_correo(request):
    correo = request.GET.get('correo')
    data = {'existe': False}

    if correo:
        try:
            miembro = Miembro.objects.filter(email=correo).first()
            if miembro:
                data.update({
                    'existe': True,
                    'activo': miembro.activo,
                    'puede_regresar': miembro.puede_regresar,
                    'id': miembro.id,
                    'nombre': miembro.nombre_completo
                })
        except Exception:
            data.update({'error': 'Hubo un problema al verificar el correo.'})

    return JsonResponse(data)

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

    def dispatch(self, request, *args, **kwargs):
        miembro = self.get_object()
        if not miembro.activo and not miembro.puede_regresar:
            messages.error(request, "No se puede editar un miembro inactivo que no puede regresar.")
            return redirect('miembros:lista_miembros')
        return super().dispatch(request, *args, **kwargs)

class EliminarMiembroView(SoloStaffMixin, DeleteView):
    model = Miembro
    success_url = reverse_lazy('miembros:lista_miembros')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        puede_volver_str = request.POST.get('puede_regresar', 'si')
        self.object.activo = False
        self.object.puede_regresar = (puede_volver_str == 'si')
        self.object.save()
        messages.success(request, f"{self.object.nombre_completo} ha sido marcado como inactivo.")
        return redirect(self.success_url)

class DetalleMiembroView(SoloStaffMixin, DetailView):
    model = Miembro
    template_name = 'miembros/detalle_miembro.html'

class CrearSancionView(SoloStaffMixin, CreateView):
    model = Sancion
    form_class = SancionForm
    template_name = 'miembros/formulario_sancion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        return context

    def dispatch(self, request, *args, **kwargs):
        miembro = get_object_or_404(Miembro, pk=self.kwargs['pk'])
        if not miembro.activo and not miembro.puede_regresar:
            messages.error(request, "Este miembro no puede recibir nuevas sanciones.")
            return redirect('miembros:detalle_miembro', pk=miembro.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.miembro_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('miembros:detalle_miembro', kwargs={'pk': self.kwargs['pk']})

# ✅ Vista corregida para reactivar miembro con respuesta JSON
@require_POST
def reactivar_miembro(request, id):
    miembro = get_object_or_404(Miembro, id=id)
    # ⚠️ Lógica corregida: solo se reactivan los que NO pueden volver y están inactivos
    if not miembro.activo and miembro.puede_regresar:
        miembro.activo = True
        miembro.save()
        return JsonResponse({
            'success': True,
            'message': f"El miembro {miembro.nombre_completo} ha sido reactivado correctamente."
        })
    else:
        return JsonResponse({
            'success': False,
            'message': "Este miembro no puede ser reactivado. Solo los inactivos que pueden volver pueden ser reactivados desde aquí."
        }, status=400)

def about(request):
    return render(request, "miembros/about.html")

def error_404(request, exception):
    """
    Vista personalizada para manejar errores 404.
    """
    return render(request, 'miembros/404.html', status=404)