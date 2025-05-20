from django.db import models
from django.urls import reverse
from django.conf import settings # Para el autor del comentario
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# ... (Modelos Genero, ContenidoBase, Pelicula, Serie, Temporada, Episodio, Anime, TemporadaAnime, EpisodioAnime sin cambios) ...
# Asegúrate que ContenidoBase, Pelicula, Serie, Anime, etc. están definidos ANTES de Comentario

class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Género")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"

class ContenidoBase(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    sinopsis = models.TextField(verbose_name="Sinopsis")
    año_lanzamiento = models.PositiveIntegerField(verbose_name="Año de Lanzamiento")
    elenco = models.CharField(max_length=500, verbose_name="Elenco", help_text="Separado por comas")
    calificacion = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Calificación (ej: 8.5)")
    portada_url = models.URLField(max_length=500, verbose_name="URL de la Portada", blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Subida")
    generos = models.ManyToManyField(Genero, verbose_name="Géneros")
    # Para poder usar GenericRelation con Comentario
    # comentarios = GenericRelation('Comentario', related_query_name='%(class)s_comentarios') # No, esto no es necesario aquí.

    class Meta:
        abstract = True
        ordering = ['-fecha_subida']

    def __str__(self):
        return self.titulo
    
    @property
    def tipo_contenido_str(self):
        return self.__class__.__name__.lower() # 'pelicula', 'serie', 'anime'


class Pelicula(ContenidoBase):
    iframe_url = models.URLField(max_length=500, verbose_name="URL del Iframe de Video")

    def get_absolute_url(self):
        return reverse('catalogo:detalle_pelicula', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"

class Serie(ContenidoBase):
    def get_absolute_url(self):
        return reverse('catalogo:detalle_serie', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Serie"
        verbose_name_plural = "Series"

class Temporada(models.Model):
    serie = models.ForeignKey(Serie, related_name='temporadas', on_delete=models.CASCADE)
    numero_temporada = models.PositiveIntegerField(verbose_name="Número de Temporada")
    titulo = models.CharField(max_length=200, blank=True, null=True, verbose_name="Título de la Temporada (opcional)")

    class Meta:
        unique_together = ('serie', 'numero_temporada')
        ordering = ['numero_temporada']
        verbose_name = "Temporada"
        verbose_name_plural = "Temporadas"

    def __str__(self):
        return f"{self.serie.titulo} - Temporada {self.numero_temporada}"

class Episodio(models.Model):
    temporada = models.ForeignKey(Temporada, related_name='episodios', on_delete=models.CASCADE)
    numero_episodio = models.PositiveIntegerField(verbose_name="Número de Episodio")
    titulo_episodio = models.CharField(max_length=200, verbose_name="Título del Episodio")
    iframe_url = models.URLField(max_length=500, verbose_name="URL del Iframe de Video")
    sinopsis_episodio = models.TextField(blank=True, null=True, verbose_name="Sinopsis del Episodio (opcional)")
    # Fecha de subida para poder ordenarlos si es necesario
    fecha_subida = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Subida")


    class Meta:
        unique_together = ('temporada', 'numero_episodio')
        ordering = ['numero_episodio']
        verbose_name = "Episodio"
        verbose_name_plural = "Episodios"

    def __str__(self):
        return f"{self.temporada} - E{self.numero_episodio:02d}: {self.titulo_episodio}"
    
    @property
    def tipo_contenido_str(self): # Para los comentarios
        return "episodio" # O podrías ser más específico si es necesario


class Anime(ContenidoBase):
    def get_absolute_url(self):
        return reverse('catalogo:detalle_anime', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Anime"
        verbose_name_plural = "Animes"

class TemporadaAnime(models.Model):
    anime = models.ForeignKey(Anime, related_name='temporadas_anime', on_delete=models.CASCADE)
    numero_temporada = models.PositiveIntegerField(verbose_name="Número de Temporada")
    titulo = models.CharField(max_length=200, blank=True, null=True, verbose_name="Título de la Temporada (opcional)")

    class Meta:
        unique_together = ('anime', 'numero_temporada')
        ordering = ['numero_temporada']
        verbose_name = "Temporada de Anime"
        verbose_name_plural = "Temporadas de Anime"

    def __str__(self):
        return f"{self.anime.titulo} - Temporada {self.numero_temporada}"

class EpisodioAnime(models.Model):
    temporada_anime = models.ForeignKey(TemporadaAnime, related_name='episodios_anime', on_delete=models.CASCADE)
    numero_episodio = models.PositiveIntegerField(verbose_name="Número de Episodio")
    titulo_episodio = models.CharField(max_length=200, verbose_name="Título del Episodio")
    iframe_url = models.URLField(max_length=500, verbose_name="URL del Iframe de Video")
    sinopsis_episodio = models.TextField(blank=True, null=True, verbose_name="Sinopsis del Episodio (opcional)")
    fecha_subida = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Subida")


    class Meta:
        unique_together = ('temporada_anime', 'numero_episodio')
        ordering = ['numero_episodio']
        verbose_name = "Episodio de Anime"
        verbose_name_plural = "Episodios de Anime"

    def __str__(self):
        return f"{self.temporada_anime} - E{self.numero_episodio:02d}: {self.titulo_episodio}"

    @property
    def tipo_contenido_str(self): # Para los comentarios
        return "episodioanime"


# --- NUEVO MODELO COMENTARIO ---
class Comentario(models.Model):
    # Si quieres que solo usuarios registrados comenten:
    # autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comentarios")
    # Si permites comentarios anónimos con nombre:
    nombre_autor = models.CharField(max_length=80, verbose_name="Nombre")
    email_autor = models.EmailField(verbose_name="Email (opcional, no se mostrará)", blank=True, null=True) # Opcional
    texto = models.TextField(verbose_name="Comentario")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True) # Para moderación

    # Campos para GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-fecha_creacion'] # Los más nuevos primero
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"

    def __str__(self):
        return f'Comentario de {self.nombre_autor} en {self.content_object}'