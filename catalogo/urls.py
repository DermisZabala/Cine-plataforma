# catalogo/urls.py
from django.urls import path
from . import views

app_name = 'catalogo' # MUY IMPORTANTE para los namespaces en las plantillas

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('peliculas/', views.lista_peliculas, name='lista_peliculas'),
    path('peliculas/cargar_mas/', views.cargar_mas_peliculas, name='cargar_mas_peliculas'),
    path('peliculas/<int:pk>/', views.detalle_pelicula, name='detalle_pelicula'),

    path('series/', views.lista_series, name='lista_series'),
    path('series/cargar_mas/', views.cargar_mas_series, name='cargar_mas_series'),
    path('series/<int:pk>/', views.detalle_serie, name='detalle_serie'),

    path('animes/', views.lista_animes, name='lista_animes'),
    path('animes/cargar_mas/', views.cargar_mas_animes, name='cargar_mas_animes'),
    path('animes/<int:pk>/', views.detalle_anime, name='detalle_anime'),

    # URLs para agregar contenido (admin frontend) - CAMBIADO EL PREFIJO
    path('gestion/agregar/<str:tipo_contenido>/', views.agregar_contenido, name='agregar_contenido'),
    path('gestion/agregar_temporada/<str:tipo_parent>/', views.agregar_temporada, name='agregar_temporada'),
    path('gestion/agregar_episodio/<str:tipo_parent>/', views.agregar_episodio, name='agregar_episodio'),

    # URL para búsqueda
    path('buscar/', views.busqueda, name='busqueda'),

    # URL para cargar más comentarios (AJAX)
    path('comentarios/cargar_mas/', views.cargar_mas_comentarios, name='cargar_mas_comentarios'),
]