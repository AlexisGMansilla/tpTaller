from django.shortcuts import render, redirect
from .forms import VideojuegoForm

# Vista para registrar nuevos videojuegos
def registrar_videojuego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST)  # Recibir los datos del formulario
        if form.is_valid():
            form.save()  # Guardar el nuevo videojuego en la base de datos
            return redirect('lista_videojuegos')  # Redirigir a la lista de videojuegos después de guardar
    else:
        form = VideojuegoForm()  # Formulario vacío si se accede por GET
    
    return render(request, 'registrar_videojuego.html', {'form': form})
