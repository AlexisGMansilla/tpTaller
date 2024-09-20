from django import forms
from .models import Videojuego, Alquiler

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['titulo', 'plataforma', 'genero', 'stock']
        
class AlquilerForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ['cliente', 'videojuego'] 