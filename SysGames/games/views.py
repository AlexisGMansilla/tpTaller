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
    plataforma_id = request.GET.get('plataforma', None) 
    genero_id = request.GET.get('genero', None) 

    plataformas = Plataforma.objects.all() 
    generos = Genero.objects.all() 

    videojuegos = Videojuego.objects.all()  # muestra todos los juegos

    if plataforma_id:  # SI -> se seleccion una plataforma
        videojuegos = videojuegos.filter(plataforma_id=plataforma_id)

    if genero_id:   # SI -> se seleccion un genero
        videojuegos = videojuegos.filter(genero_id=genero_id)

    return render(request, 'lista_videojuegos.html', {
        'videojuegos': videojuegos,
        'plataformas': plataformas,
        'generos': generos,
    })

def listar_alquileres(request):
    alquileres = Alquiler.objects.all()
    return render(request, 'lista_alquileres.html', {'alquileres': alquileres})

def registrar_alquiler(request):
    if request.method == 'POST':
        form = AlquilerForm(request.POST)
        if form.is_valid():
            alquiler = form.save(commit=False)
            videojuego = alquiler.videojuego

            # verifica si hay stock disponible
            if videojuego.stock > 0:
                # Reducir el stock en 1
                videojuego.stock -= 1
                videojuego.save()

                # registrar la fecha de alquiler
                alquiler.fecha_alquiler = timezone.now()
                alquiler.save()

                return redirect('lista_alquileres') 
            else:
                # Sino... no hay stock disponible
                form.add_error('videojuego', 'No hay stock disponible para este videojuego.')

    else:
        form = AlquilerForm()

    return render(request, 'registrar_alquiler.html', {'form': form})


def finalizar_alquiler(request, alquiler_id):
    alquiler = get_object_or_404(Alquiler, id=alquiler_id)
    
    if request.method == 'POST':
        if alquiler.fecha_devolucion is None:  # si no ha sido devuelto aún
            # registrar la fecha de devolución
            alquiler.fecha_devolucion = timezone.now()
            alquiler.save()

            # aumentar el stock del videojuego
            alquiler.videojuego.stock += 1
            alquiler.videojuego.save()

            return redirect('lista_alquileres') 

    return render(request, 'finalizar_alquiler.html', {'alquiler': alquiler})

def actualizar_stock(request, videojuego_id):
    videojuego = get_object_or_404(Videojuego, id=videojuego_id)
    
    if request.method == 'POST':
        nuevo_stock = request.POST.get('nuevo_stock') 
        try:
            nuevo_stock = int(nuevo_stock)  
            if nuevo_stock >= 0:  # verifica que el stock no sea negativo
                videojuego.stock = nuevo_stock
                videojuego.save()
                return redirect('listar_videojuegos') 
            else:
                # si el stock es negativo
                return render(request, 'actualizar_stock.html', {'videojuego': videojuego, 'error': 'El stock no puede ser negativo.'})
        except ValueError:
            # si el valor no es un número válido
            return render(request, 'actualizar_stock.html', {'videojuego': videojuego, 'error': 'Ingrese un número válido para el stock.'})
    
    return render(request, 'actualizar_stock.html', {'videojuego': videojuego})