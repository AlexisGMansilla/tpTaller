from django.db import models

# platadormas
class Plataforma(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

#genero
class Genero(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# game
class Videojuego(models.Model):
    titulo = models.CharField(max_length=200)
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    stock = models.IntegerField()

    def __str__(self):
        return self.titulo

# alquiler juegos
class Alquiler(models.Model):
    cliente = models.CharField(max_length=100)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    fecha_alquiler = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.cliente} - {self.videojuego.titulo}"
