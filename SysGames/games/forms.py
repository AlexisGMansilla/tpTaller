from django import forms
from .models import games

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = games
        fields = ['titulo', 'plataforma', 'genero', 'stock']