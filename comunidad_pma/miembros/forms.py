from django import forms
from .models import Miembro, Sancion, SolicitudCorreccion
from django_countries.widgets import CountrySelectWidget
import re

class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = ['nombre_completo', 'pais', 'numero_telefono', 'email', 'activo', 'puede_regresar']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'aria-label': 'Nombre completo',
                'placeholder': 'Ingrese el nombre completo',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'aria-label': 'Correo electrónico',
                'placeholder': 'Ingrese el correo electrónico',
                'class': 'form-control',
            }),
            'numero_telefono': forms.TextInput(attrs={
                'aria-label': 'Número de teléfono',
                'placeholder': 'Ingrese el número de teléfono',
                'class': 'form-control',
                'id': 'telefono',  # Necesario para JS de intl-tel-input
            }),
            'pais': CountrySelectWidget(attrs={
                'aria-label': 'País',
                'class': 'form-control',
            }),
            'activo': forms.CheckboxInput(attrs={
                'aria-label': '¿Está activo?',
            }),
            'puede_regresar': forms.CheckboxInput(attrs={
                'aria-label': '¿Puede regresar?',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(MiembroForm, self).__init__(*args, **kwargs)
        
        # Aquí establecemos si el campo 'email' debe ser de solo lectura
        if self.instance and self.instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True

    def clean_nombre_completo(self):
        nombre = self.cleaned_data.get('nombre_completo')
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras y espacios.')
        return nombre


class SancionForm(forms.ModelForm):
    class Meta:
        model = Sancion
        fields = ['motivo', 'cantidad_llamados']
        widgets = {
            'motivo': forms.TextInput(attrs={
                'aria-label': 'Motivo de la sanción',
                'placeholder': 'Motivo de la sanción',
                'class': 'form-control',
            }),
            'cantidad_llamados': forms.NumberInput(attrs={
                'aria-label': 'Cantidad de llamados',
                'placeholder': 'Cantidad de llamados',
                'class': 'form-control',
                'min': 1,
            }),
        }

    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if len(motivo.strip()) < 5:
            raise forms.ValidationError('El motivo debe ser al menos de 5 caracteres.')
        return motivo


class SolicitudCorreccionForm(forms.ModelForm):
    class Meta:
        model = SolicitudCorreccion
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'aria-label': 'Descripción del error',
                'placeholder': 'Describa el error',
                'rows': 4,
                'cols': 50,
                'class': 'form-control',
            }),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if len(descripcion.strip()) < 10:
            raise forms.ValidationError('La descripción debe tener al menos 10 caracteres.')
        return descripcion
