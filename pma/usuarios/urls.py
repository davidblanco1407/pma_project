from django.urls import path, include
from .views import registro, inicio_sesion, home

urlpatterns = [
    path("", home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/registro/", registro, name="registro"),
    path("accounts/login/", inicio_sesion, name="login"),
]