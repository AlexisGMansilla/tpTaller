from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_videojuego, name='registrar_videojuego'),
]