from django.urls import path
from .views import registro, home

urlpatterns = [
    path("accounts/registro/", registro, name="registro"),
]
