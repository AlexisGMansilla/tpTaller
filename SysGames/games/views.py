from django.shortcuts import render, redirect
from .forms import VideojuegoForm
from .models import Videojuego
from django.shortcuts import redirect, get_object_or_404
from .models import Alquiler, Videojuego
from django.utils import timezone

def registrar_videojuego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST) 
        if form.is_valid():
            form.save()  
            return redirect('lista_videojuegos')  
    else:
        form = VideojuegoForm() 
    
    return render(request, 'registrar_videojuego.html', {'form': form})

def listar_videojuegos(request):
    plataforma_id = request.GET.get('plataforma', None)
    genero_id = request.GET.get('genero', None)

    if plataforma_id:
        videojuegos = Videojuego.objects.filter(plataforma__id=plataforma_id)
    elif genero_id:
        videojuegos = Videojuego.objects.filter(genero__id=genero_id)
    else:
        videojuegos = Videojuego.objects.all()

    return render(request, 'lista_videojuegos.html', {'videojuegos': videojuegos})

def finalizar_alquiler(request, alquiler_id):
    alquiler = get_object_or_404(Alquiler, id=alquiler_id)
    if alquiler.fecha_devolucion is None:  # Solo si no se ha devuelto aún
        alquiler.fecha_devolucion = timezone.now()
        alquiler.save()

        # Actualizar el stock del videojuego
        alquiler.videojuego.stock += 1
        alquiler.videojuego.save()

    return redirect('lista_alquileres')