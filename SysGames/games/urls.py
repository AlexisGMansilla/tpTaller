from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registrar/', views.registrar_videojuego, name='registrar_videojuego'),
    path('videojuegos/', views.listar_videojuegos, name='listar_videojuegos'),
    path('alquileres/', views.listar_alquileres, name='lista_alquileres'),
    path('finalizar_alquiler/<int:alquiler_id>/', views.finalizar_alquiler, name='finalizar_alquiler')
]
