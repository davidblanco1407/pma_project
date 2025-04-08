from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import parse, is_valid_number
from django.core.exceptions import ValidationError

class Usuario(AbstractUser):
    # Definimos los roles disponibles
    roles = (
        ("admin", "Administrador"),
        ("miembro", "Miembro"),
    )

    # Campos personalizados
    pais = CountryField(blank_label='(Selecciona un país)')
    telefono = PhoneNumberField()  # Teléfono obligatorio
    rol = models.CharField(max_length=10, choices=roles, default="miembro")

    def __str__(self):
        return f"{self.username} - {self.rol}"

    def clean(self):
        """
        Método para validaciones adicionales al guardar el objeto.
        Se asegura de que el número de teléfono esté asociado al país del usuario
        y es válido según las reglas de ese país.
        """
        super().clean()

        if self.pais:
            if self.telefono:
                try:
                    # Intentamos analizar el número de teléfono usando el código de país del usuario
                    telefono_con_codigo = parse(str(self.telefono), self.pais.code)

                    # Validamos si el número es válido con el código de país
                    if not is_valid_number(telefono_con_codigo):
                        raise ValidationError(f"El número de teléfono no es válido para el país {self.pais.name}.")
                    else:
                        self.telefono = telefono_con_codigo  # Se guarda el número de teléfono con el código de país adecuado
                except Exception as e:
                    raise ValidationError(f"El número de teléfono no es válido: {str(e)}")
            else:
                raise ValidationError("El número de teléfono es obligatorio.")
        else:
            raise ValidationError("El país es obligatorio para asociar un número de teléfono.")
