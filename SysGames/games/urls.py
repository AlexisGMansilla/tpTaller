from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_videojuego, name='registrar_videojuego'),
    path('videojuegos/', views.listar_videojuegos, name='listar_videojuegos'),
    path('finalizar_alquiler/<int:alquiler_id>/', views.finalizar_alquiler, name='finalizar_alquiler'),
]