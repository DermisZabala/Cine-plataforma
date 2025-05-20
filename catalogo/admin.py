from django.contrib import admin
from .models import (Genero, Pelicula, Serie, Temporada, Episodio,
                   Anime, TemporadaAnime, EpisodioAnime, Comentario) # Añadir Comentario

# ... (Admin de Pelicula, Serie, Anime, etc. como antes) ...
class EpisodioInline(admin.TabularInline):
    model = Episodio
    extra = 1

class TemporadaAdmin(admin.ModelAdmin):
    inlines = [EpisodioInline]
    list_display = ('serie', 'numero_temporada', 'titulo')
    list_filter = ('serie',)

class TemporadaInline(admin.TabularInline):
    model = Temporada
    extra = 1
    show_change_link = True

class SerieAdmin(admin.ModelAdmin):
    inlines = [TemporadaInline]
    list_display = ('titulo', 'año_lanzamiento', 'calificacion', 'fecha_subida')
    list_filter = ('generos', 'año_lanzamiento')
    search_fields = ('titulo', 'elenco')
    filter_horizontal = ('generos',)

class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'año_lanzamiento', 'calificacion', 'fecha_subida')
    list_filter = ('generos', 'año_lanzamiento')
    search_fields = ('titulo', 'elenco')
    filter_horizontal = ('generos',)

class EpisodioAnimeInline(admin.TabularInline):
    model = EpisodioAnime
    extra = 1

class TemporadaAnimeAdmin(admin.ModelAdmin):
    inlines = [EpisodioAnimeInline]
    list_display = ('anime', 'numero_temporada', 'titulo')
    list_filter = ('anime',)

class TemporadaAnimeInline(admin.TabularInline):
    model = TemporadaAnime
    extra = 1
    show_change_link = True

class AnimeAdmin(admin.ModelAdmin):
    inlines = [TemporadaAnimeInline]
    list_display = ('titulo', 'año_lanzamiento', 'calificacion', 'fecha_subida')
    list_filter = ('generos', 'año_lanzamiento')
    search_fields = ('titulo', 'elenco')
    filter_horizontal = ('generos',)

# --- NUEVO ADMIN COMENTARIO ---
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_autor', 'content_object', 'fecha_creacion', 'activo')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('nombre_autor', 'texto')
    actions = ['aprobar_comentarios']

    def aprobar_comentarios(self, request, queryset):
        queryset.update(activo=True)
    aprobar_comentarios.short_description = "Aprobar comentarios seleccionados"

admin.site.register(Genero)
admin.site.register(Pelicula, PeliculaAdmin)
admin.site.register(Serie, SerieAdmin)
admin.site.register(Temporada, TemporadaAdmin)
admin.site.register(Episodio)
admin.site.register(Anime, AnimeAdmin)
admin.site.register(TemporadaAnime, TemporadaAnimeAdmin)
admin.site.register(EpisodioAnime)