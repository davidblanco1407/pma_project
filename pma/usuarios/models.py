from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

class Usuario(AbstractUser):
    roles = (
        ("admin", "Administrador"),
        ("miembro", "Miembro"),
    )
    pais = CountryField(blank_label='(Selecciona un país)')
    telefono = PhoneNumberField(blank=True)
    rol = models.CharField(max_length=10, choices=roles, default="miembro")

    def __str__(self):
        return f"{self.username} - {self.rol}"
    
    def clean(self):
        super().clean()
        if self.pais:
            self.telefono.region = self.pais.alpha_2