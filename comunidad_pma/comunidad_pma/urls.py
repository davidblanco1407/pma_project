from django.contrib import admin
from django.urls import path, include
from miembros.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Página de inicio
    path('miembros/', include('miembros.urls', namespace='miembros')),
    path('accounts/', include('django.contrib.auth.urls')),  # Login y logout
]
