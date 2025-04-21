from django.contrib import admin
from .models import Miembro, Sancion, SolicitudCorreccion

@admin.register(Miembro)
class MiembroAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'email', 'activo', 'pais')

@admin.register(Sancion)
class SancionAdmin(admin.ModelAdmin):
    list_display = ('miembro', 'motivo', 'cantidad_llamados', 'fecha')

@admin.register(SolicitudCorreccion)
class SolicitudCorreccionAdmin(admin.ModelAdmin):
    list_display = ('miembro', 'descripcion', 'fecha', 'atendido')
    list_filter = ('atendido', 'fecha')
    search_fields = ('miembro__nombre_completo', 'descripcion')
    actions = ['marcar_como_atendidas']

    def marcar_como_atendidas(self, request, queryset):
        queryset.update(atendido=True)
    marcar_como_atendidas.short_description = "Marcar seleccionadas como atendidas"
