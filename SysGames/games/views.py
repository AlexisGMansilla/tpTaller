from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideojuegoForm, AlquilerForm
from .models import Videojuego, Alquiler, Plataforma, Genero
from django.utils import timezone

def index(request):
    return render(request, 'index.html')

def registrar_videojuego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST) 
        if form.is_valid():
            form.save()  
            return redirect('listar_videojuegos')  
    else:
        form = VideojuegoForm() 
    
    return render(request, 'registrar_videojuego.html', {'form': form})



def listar_videojuegos(request):
    plataforma_id = request.GET.get('plataforma', None)  # Obtener el valor de la plataforma seleccionada
    genero_id = request.GET.get('genero', None)  # Obtener el valor del género seleccionado

    plataformas = Plataforma.objects.all()  # Obtener todas las plataformas para mostrar en el formulario
    generos = Genero.objects.all()  # Obtener todos los géneros para mostrar en el formulario

    # Aplicar los filtros de plataforma y género
    videojuegos = Videojuego.objects.all()  # Comenzar con todos los videojuegos

    if plataforma_id:  # Si se ha seleccionado una plataforma
        videojuegos = videojuegos.filter(plataforma_id=plataforma_id)

    if genero_id:  # Si se ha seleccionado un género
        videojuegos = videojuegos.filter(genero_id=genero_id)

    return render(request, 'lista_videojuegos.html', {
        'videojuegos': videojuegos,
        'plataformas': plataformas,  # Pasar plataformas a la plantilla
        'generos': generos,  # Pasar géneros a la plantilla
    })

def listar_alquileres(request):
    alquileres = Alquiler.objects.all()
    return render(request, 'lista_alquileres.html', {'alquileres': alquileres})

def finalizar_alquiler(request, alquiler_id):
    alquiler = get_object_or_404(Alquiler, id=alquiler_id)
    if alquiler.fecha_devolucion is None:  # Solo si no se ha devuelto aún
        alquiler.fecha_devolucion = timezone.now()
        alquiler.save()

        # Actualizar el stock del videojuego
        alquiler.videojuego.stock += 1
        alquiler.videojuego.save()

    return redirect('lista_alquileres')

def registrar_alquiler(request):
    if request.method == 'POST':
        form = AlquilerForm(request.POST)
        if form.is_valid():
            alquiler = form.save(commit=False)
            videojuego = alquiler.videojuego

            # Verificar si hay stock disponible
            if videojuego.stock > 0:
                # Reducir el stock en 1
                videojuego.stock -= 1
                videojuego.save()

                # Registrar la fecha de alquiler
                alquiler.fecha_alquiler = timezone.now()
                alquiler.save()

                return redirect('lista_alquileres')  # Redirigir a la lista de alquileres
            else:
                # Manejo de error: No hay stock disponible
                form.add_error('videojuego', 'No hay stock disponible para este videojuego.')

    else:
        form = AlquilerForm()

    return render(request, 'registrar_alquiler.html', {'form': form})


def finalizar_alquiler(request, alquiler_id):
    alquiler = get_object_or_404(Alquiler, id=alquiler_id)
    
    if request.method == 'POST':
        if alquiler.fecha_devolucion is None:  # Solo si no ha sido devuelto aún
            # Registrar la fecha de devolución
            alquiler.fecha_devolucion = timezone.now()
            alquiler.save()

            # Aumentar el stock del videojuego
            alquiler.videojuego.stock += 1
            alquiler.videojuego.save()

            return redirect('lista_alquileres')  # Redirigir a la lista de alquileres

    return render(request, 'finalizar_alquiler.html', {'alquiler': alquiler})
