from django.urls import path
from . import views

app_name = 'miembros'

urlpatterns = [
    path('', views.home, name='home'),
    path('solicitar-correccion/<int:pk>/', views.solicitar_correccion, name='solicitar_correccion'),
    path('listar/', views.ListaMiembrosView.as_view(), name='lista_miembros'),
    path('crear/', views.CrearMiembroView.as_view(), name='crear_miembro'),
    path('editar/<int:pk>/', views.EditarMiembroView.as_view(), name='editar_miembro'),
    path('eliminar/<int:pk>/', views.EliminarMiembroView.as_view(), name='eliminar_miembro'),
    path('detalle/<int:pk>/', views.DetalleMiembroView.as_view(), name='detalle_miembro'),
    path('sancion/crear/<int:pk>/', views.CrearSancionView.as_view(), name='crear_sancion'),
    path('verificar-correo/', views.verificar_correo, name='verificar_correo'),
    path('reactivar/<int:id>/', views.reactivar_miembro, name='reactivar_miembro'),
    path('about/', views.about, name='about'),  # Nueva ruta para la página "Acerca de"
]

# Configuración para manejar errores 404
handler404 = 'miembros.views.error_404'
