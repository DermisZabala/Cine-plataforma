from django import forms
from .models import Pelicula, Serie, Anime, Temporada, Episodio, TemporadaAnime, EpisodioAnime, Comentario, Genero

class ContenidoBaseForm(forms.ModelForm):
    generos = forms.ModelMultipleChoiceField(
        queryset=Genero.objects.all(),
        widget=forms.CheckboxSelectMultiple, # O forms.SelectMultiple si prefieres
        required=False
    )
    class Meta:
        exclude = ['fecha_subida'] # Se añade automáticamente

class PeliculaForm(ContenidoBaseForm):
    class Meta(ContenidoBaseForm.Meta):
        model = Pelicula

class SerieForm(ContenidoBaseForm):
    class Meta(ContenidoBaseForm.Meta):
        model = Serie

class AnimeForm(ContenidoBaseForm):
    class Meta(ContenidoBaseForm.Meta):
        model = Anime

class TemporadaForm(forms.ModelForm):
    class Meta:
        model = Temporada
        fields = ['serie', 'numero_temporada', 'titulo'] # Si es para Serie

class TemporadaAnimeForm(forms.ModelForm):
    class Meta:
        model = TemporadaAnime
        fields = ['anime', 'numero_temporada', 'titulo'] # Si es para Anime


class EpisodioForm(forms.ModelForm):
    class Meta:
        model = Episodio
        fields = ['temporada', 'numero_episodio', 'titulo_episodio', 'iframe_url', 'sinopsis_episodio']

class EpisodioAnimeForm(forms.ModelForm):
    class Meta:
        model = EpisodioAnime
        fields = ['temporada_anime', 'numero_episodio', 'titulo_episodio', 'iframe_url', 'sinopsis_episodio']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('nombre_autor', 'email_autor', 'texto')
        widgets = {
            'nombre_autor': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'email_autor': forms.EmailInput(attrs={'placeholder': 'Tu email (opcional)'}),
            'texto': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu comentario...'}),
        }