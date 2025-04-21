from django import forms
from .models import Miembro, Sancion

class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = '__all__'

class SancionForm(forms.ModelForm):
    class Meta:
        model = Sancion
        fields = ['motivo', 'cantidad_llamados']
