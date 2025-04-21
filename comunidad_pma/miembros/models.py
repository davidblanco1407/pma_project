from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
import re

def validar_nombre(value):
    if not re.match(r'^[a-zA-Z\s]+$', value):
        raise ValidationError('El nombre solo puede contener letras y espacios.')

class Miembro(models.Model):
    nombre_completo = models.CharField(max_length=255, validators=[validar_nombre])
    pais = CountryField()
    numero_telefono = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    activo = models.BooleanField(default=True)
    puede_regresar = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_completo    

class Sancion(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='sanciones')
    motivo = models.CharField(max_length=255, default="Publicidad no autorizada")
    fecha = models.DateTimeField(auto_now_add=True)
    cantidad_llamados = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.miembro.nombre_completo} - {self.motivo} ({self.cantidad_llamados})"

class SolicitudCorreccion(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='solicitudes')
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    atendido = models.BooleanField(default=False)

    def __str__(self):
        return f"Solicitud de {self.miembro.nombre_completo} ({'Atendida' if self.atendido else 'Pendiente'})"
