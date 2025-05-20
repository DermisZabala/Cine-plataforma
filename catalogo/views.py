from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404, HttpResponseForbidden
from django.template.loader import render_to_string
from .models import (Pelicula, Serie, Anime, Episodio, EpisodioAnime, Comentario,
                   Genero, Temporada, TemporadaAnime) # Añadir modelos necesarios
from .forms import (PeliculaForm, SerieForm, AnimeForm, EpisodioForm, EpisodioAnimeForm,
                  ComentarioForm, TemporadaForm, TemporadaAnimeForm) # Añadir forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q # Para búsquedas complejas
from itertools import chain # Para combinar querysets
from operator import attrgetter # Para ordenar listas de objetos mezclados

ITEMS_POR_PAGINA_INICIAL = 10
ITEMS_POR_CARGA_ADICIONAL = 5
COMENTARIOS_POR_PAGINA = 5

# Decorador para superusuario
def superuser_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser,
        login_url='/admin/login/' # O una página de login personalizada
    )(view_func)
    return decorated_view_func

def inicio(request):
    # Últimas 10 publicaciones combinadas
    ultimas_peliculas = Pelicula.objects.all().order_by('-fecha_subida')[:5]
    ultimas_series = Serie.objects.all().order_by('-fecha_subida')[:5]
    ultimos_animes = Anime.objects.all().order_by('-fecha_subida')[:5]

    # Combinar y ordenar por fecha_subida
    # Esto es un poco más complejo porque son tipos diferentes.
    # Una forma es convertirlos a una lista de diccionarios o una clase común.
    # O, más simple para pocos items, obtenerlos y ordenarlos en Python.
    
    # Opción más robusta: iterar y marcar el tipo, luego ordenar
    ultimas_publicaciones_raw = sorted(
        chain(ultimas_peliculas, ultimas_series, ultimos_animes),
        key=attrgetter('fecha_subida'),
        reverse=True
    )
    
    # Tomar los N más recientes del conjunto combinado
    N_MAS_RECIENTES = 10 # Por ejemplo
    ultimas_publicaciones = ultimas_publicaciones_raw[:N_MAS_RECIENTES]


    context = {
        'ultimas_publicaciones': ultimas_publicaciones,
    }
    return render(request, 'catalogo/inicio.html', context)

# --- Vistas de Listas (Peliculas, Series, Anime) ---
# (lista_peliculas, cargar_mas_peliculas, lista_series, cargar_mas_series, lista_animes, cargar_mas_animes)
# Se mantienen similares, solo asegúrate de que el contexto tenga 'tipo_contenido'

def lista_peliculas(request):
    peliculas = Pelicula.objects.all().order_by('-fecha_subida')[:ITEMS_POR_PAGINA_INICIAL]
    total_peliculas = Pelicula.objects.count()
    context = {
        'peliculas': peliculas,
        'mostrar_boton_mas': total_peliculas > ITEMS_POR_PAGINA_INICIAL,
        'tipo_contenido': 'pelicula',
        'page_title': 'Películas'
    }
    return render(request, 'catalogo/lista_contenido.html', context) # Usaremos una plantilla genérica

def cargar_mas_peliculas(request):
    offset_actual = int(request.GET.get('offset', ITEMS_POR_PAGINA_INICIAL))
    peliculas = Pelicula.objects.all().order_by('-fecha_subida')[offset_actual:offset_actual + ITEMS_POR_CARGA_ADICIONAL]
    html = ""
    for pelicula in peliculas:
        html += render_to_string('catalogo/partials/_item_contenido.html', {'item': pelicula, 'tipo_item': 'pelicula'})
    siguientes_existen = Pelicula.objects.all().order_by('-fecha_subida')[offset_actual + ITEMS_POR_CARGA_ADICIONAL:].exists()
    return JsonResponse({'html': html, 'hay_mas': siguientes_existen})

def lista_series(request):
    series = Serie.objects.all().order_by('-fecha_subida')[:ITEMS_POR_PAGINA_INICIAL]
    total_series = Serie.objects.count()
    context = {
        'series_items': series, # Renombrar para no colisionar con 'peliculas' en la plantilla genérica
        'mostrar_boton_mas': total_series > ITEMS_POR_PAGINA_INICIAL,
        'tipo_contenido': 'serie',
        'page_title': 'Series'
    }
    return render(request, 'catalogo/lista_contenido.html', context)

def cargar_mas_series(request):
    offset_actual = int(request.GET.get('offset', ITEMS_POR_PAGINA_INICIAL))
    series_items = Serie.objects.all().order_by('-fecha_subida')[offset_actual:offset_actual + ITEMS_POR_CARGA_ADICIONAL]
    html = ""
    for serie_item in series_items:
        html += render_to_string('catalogo/partials/_item_contenido.html', {'item': serie_item, 'tipo_item': 'serie'})
    siguientes_existen = Serie.objects.all().order_by('-fecha_subida')[offset_actual + ITEMS_POR_CARGA_ADICIONAL:].exists()
    return JsonResponse({'html': html, 'hay_mas': siguientes_existen})

def lista_animes(request):
    animes = Anime.objects.all().order_by('-fecha_subida')[:ITEMS_POR_PAGINA_INICIAL]
    total_animes = Anime.objects.count()
    context = {
        'animes_items': animes, # Renombrar para no colisionar
        'mostrar_boton_mas': total_animes > ITEMS_POR_PAGINA_INICIAL,
        'tipo_contenido': 'anime',
        'page_title': 'Anime'
    }
    return render(request, 'catalogo/lista_contenido.html', context)

def cargar_mas_animes(request):
    offset_actual = int(request.GET.get('offset', ITEMS_POR_PAGINA_INICIAL))
    animes_items = Anime.objects.all().order_by('-fecha_subida')[offset_actual:offset_actual + ITEMS_POR_CARGA_ADICIONAL]
    html = ""
    for anime_item in animes_items:
        html += render_to_string('catalogo/partials/_item_contenido.html', {'item': anime_item, 'tipo_item': 'anime'})
    siguientes_existen = Anime.objects.all().order_by('-fecha_subida')[offset_actual + ITEMS_POR_CARGA_ADICIONAL:].exists()
    return JsonResponse({'html': html, 'hay_mas': siguientes_existen})


# catalogo/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse # Sigue siendo necesaria para cargar_mas_comentarios
from django.template.loader import render_to_string
from .models import (Pelicula, Serie, Anime, Episodio, EpisodioAnime, Comentario,
                   Genero, Temporada, TemporadaAnime)
from .forms import (PeliculaForm, SerieForm, AnimeForm, EpisodioForm, EpisodioAnimeForm,
                  ComentarioForm, TemporadaForm, TemporadaAnimeForm)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from itertools import chain
from operator import attrgetter

# Constantes (asegúrate de que estén definidas al principio de tu archivo views.py)
ITEMS_POR_PAGINA_INICIAL = 10
ITEMS_POR_CARGA_ADICIONAL = 5
COMENTARIOS_POR_PAGINA = 5 # Para la carga inicial y "mostrar más"

# ... (tus otras vistas: inicio, listas, cargar_mas_contenido, admin_forms, busqueda, etc. sin cambios por ahora) ...

# --- VISTA DE DETALLE DE PELÍCULA (REESCRITA) ---
def detalle_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula.objects.prefetch_related('generos'), pk=pk)
    content_type_obj = ContentType.objects.get_for_model(pelicula)

    # 1. Lógica para enviar un nuevo comentario
    form_comentario = ComentarioForm() # Formulario vacío por defecto
    if request.method == 'POST' and 'submit_comentario' in request.POST:
        form_comentario = ComentarioForm(data=request.POST) # Formulario con datos del POST
        if form_comentario.is_valid():
            nuevo_comentario = form_comentario.save(commit=False)
            nuevo_comentario.content_object = pelicula # Asocia el comentario a esta película
            # Si requieres que el autor sea un usuario logueado:
            # if request.user.is_authenticated:
            #    nuevo_comentario.autor = request.user
            nuevo_comentario.save()
            # Redirigir para evitar reenvío del formulario al recargar la página
            return redirect(request.path_info + '?comentario_enviado=1')
        # Si el formulario NO es válido, se pasará al template con los errores.

    # 2. Obtener comentarios para mostrar
    comentarios_todos = Comentario.objects.filter(
        content_type=content_type_obj,
        object_id=pelicula.id,
        activo=True
    ).order_by('-fecha_creacion') # Los más nuevos primero

    comentarios_pagina_actual = comentarios_todos[:COMENTARIOS_POR_PAGINA]
    total_comentarios_activos = comentarios_todos.count()
    mostrar_boton_mas_comentarios = total_comentarios_activos > COMENTARIOS_POR_PAGINA

    context = {
        'pelicula': pelicula,
        'item': pelicula, # Para el parcial de comentarios genérico
        'comentarios': comentarios_pagina_actual,
        'form_comentario': form_comentario, # El formulario (vacío o con errores)
        'mostrar_mas_comentarios': mostrar_boton_mas_comentarios,
        'content_type_id': content_type_obj.id, # Para el botón "Mostrar más comentarios"
        'object_id': pelicula.id,              # Para el botón "Mostrar más comentarios"
        'comentario_enviado': request.GET.get('comentario_enviado'), # Para mostrar un mensaje de éxito
        'total_comentarios_en_vista': total_comentarios_activos, # Para mostrar el conteo total
    }
    return render(request, 'catalogo/detalle_pelicula.html', context)

# --- VISTA DE DETALLE DE SERIE (REESCRITA) ---
def detalle_serie(request, pk):
    serie = get_object_or_404(Serie.objects.prefetch_related('generos', 'temporadas__episodios'), pk=pk)
    content_type_obj = ContentType.objects.get_for_model(serie)

    form_comentario = ComentarioForm()
    if request.method == 'POST' and 'submit_comentario' in request.POST:
        form_comentario = ComentarioForm(data=request.POST)
        if form_comentario.is_valid():
            nuevo_comentario = form_comentario.save(commit=False)
            nuevo_comentario.content_object = serie
            nuevo_comentario.save()
            return redirect(request.path_info + '?comentario_enviado=1' + ('&episodio_id=' + request.GET.get('episodio_id') if request.GET.get('episodio_id') else ''))


    comentarios_todos = Comentario.objects.filter(
        content_type=content_type_obj,
        object_id=serie.id,
        activo=True
    ).order_by('-fecha_creacion')

    comentarios_pagina_actual = comentarios_todos[:COMENTARIOS_POR_PAGINA]
    total_comentarios_activos = comentarios_todos.count()
    mostrar_boton_mas_comentarios = total_comentarios_activos > COMENTARIOS_POR_PAGINA

    context = {
        'serie': serie,
        'item': serie,
        'comentarios': comentarios_pagina_actual,
        'form_comentario': form_comentario,
        'mostrar_mas_comentarios': mostrar_boton_mas_comentarios,
        'content_type_id': content_type_obj.id,
        'object_id': serie.id,
        'comentario_enviado': request.GET.get('comentario_enviado'),
        'total_comentarios_en_vista': total_comentarios_activos,
    }
    if request.GET.get('episodio_id'):
        try:
            episodio_id = int(request.GET.get('episodio_id'))
            episodio_seleccionado = Episodio.objects.get(id=episodio_id, temporada__serie=serie)
            context['episodio_seleccionado'] = episodio_seleccionado
        except (ValueError, Episodio.DoesNotExist):
            pass
    return render(request, 'catalogo/detalle_serie.html', context)

# --- VISTA DE DETALLE DE ANIME (REESCRITA) ---
def detalle_anime(request, pk):
    anime = get_object_or_404(Anime.objects.prefetch_related('generos', 'temporadas_anime__episodios_anime'), pk=pk)
    content_type_obj = ContentType.objects.get_for_model(anime)

    form_comentario = ComentarioForm()
    if request.method == 'POST' and 'submit_comentario' in request.POST:
        form_comentario = ComentarioForm(data=request.POST)
        if form_comentario.is_valid():
            nuevo_comentario = form_comentario.save(commit=False)
            nuevo_comentario.content_object = anime
            nuevo_comentario.save()
            return redirect(request.path_info + '?comentario_enviado=1' + ('&episodio_id=' + request.GET.get('episodio_id') if request.GET.get('episodio_id') else ''))


    comentarios_todos = Comentario.objects.filter(
        content_type=content_type_obj,
        object_id=anime.id,
        activo=True
    ).order_by('-fecha_creacion')

    comentarios_pagina_actual = comentarios_todos[:COMENTARIOS_POR_PAGINA]
    total_comentarios_activos = comentarios_todos.count()
    mostrar_boton_mas_comentarios = total_comentarios_activos > COMENTARIOS_POR_PAGINA

    context = {
        'anime': anime,
        'item': anime,
        'comentarios': comentarios_pagina_actual,
        'form_comentario': form_comentario,
        'mostrar_mas_comentarios': mostrar_boton_mas_comentarios,
        'content_type_id': content_type_obj.id,
        'object_id': anime.id,
        'comentario_enviado': request.GET.get('comentario_enviado'),
        'total_comentarios_en_vista': total_comentarios_activos,
    }
    if request.GET.get('episodio_id'):
        try:
            episodio_id = int(request.GET.get('episodio_id'))
            episodio_seleccionado = EpisodioAnime.objects.get(id=episodio_id, temporada_anime__anime=anime)
            context['episodio_seleccionado'] = episodio_seleccionado
        except (ValueError, EpisodioAnime.DoesNotExist):
            pass
    return render(request, 'catalogo/detalle_anime.html', context)


# La función cargar_mas_comentarios (AJAX) sigue siendo la misma y es correcta:
def cargar_mas_comentarios(request):
    content_type_id = request.GET.get('content_type_id')
    object_id = request.GET.get('object_id')
    offset = int(request.GET.get('offset', 0)) # Cuántos comentarios ya se mostraron

    try:
        content_type = ContentType.objects.get_for_id(content_type_id)
    except ContentType.DoesNotExist:
        return JsonResponse({'error': 'Tipo de contenido no válido'}, status=400)

    # Asegurarse que el offset es correcto para la siguiente página de comentarios
    # Si inicialmente mostramos COMENTARIOS_POR_PAGINA, y el offset viene como la cantidad
    # de items ya cargados, entonces el siguiente slice es correcto.
    
    comentarios = Comentario.objects.filter(
        content_type=content_type,
        object_id=object_id,
        activo=True
    ).order_by('-fecha_creacion')[offset : offset + COMENTARIOS_POR_PAGINA]

    html = ""
    for comentario in comentarios:
        html += render_to_string('catalogo/partials/_comentario_item.html', {'comentario': comentario})

    siguientes_existen = Comentario.objects.filter(
        content_type=content_type,
        object_id=object_id,
        activo=True
    ).order_by('-fecha_creacion')[offset + COMENTARIOS_POR_PAGINA:].exists()
    
    return JsonResponse({'html': html, 'hay_mas': siguientes_existen})




# --- VISTA AJAX PARA CARGAR MÁS COMENTARIOS ---
def cargar_mas_comentarios(request):
    content_type_id = request.GET.get('content_type_id')
    object_id = request.GET.get('object_id')
    offset = int(request.GET.get('offset', 0))

    try:
        content_type = ContentType.objects.get_for_id(content_type_id)
        # model_class = content_type.model_class() # No necesitamos la clase, solo el tipo y id
    except ContentType.DoesNotExist:
        return JsonResponse({'error': 'Tipo de contenido no válido'}, status=400)

    comentarios = Comentario.objects.filter(
        content_type=content_type,
        object_id=object_id,
        activo=True
    )[offset:offset + COMENTARIOS_POR_PAGINA]

    html = ""
    for comentario in comentarios:
        html += render_to_string('catalogo/partials/_comentario_item.html', {'comentario': comentario})

    siguientes_existen = Comentario.objects.filter(
        content_type=content_type,
        object_id=object_id,
        activo=True
    )[offset + COMENTARIOS_POR_PAGINA:].exists()
    
    return JsonResponse({'html': html, 'hay_mas': siguientes_existen})


# --- VISTAS PARA AÑADIR CONTENIDO (SOLO SUPERUSUARIO) ---
@superuser_required
def agregar_contenido(request, tipo_contenido):
    FormClase = None
    template_name = 'catalogo/admin_forms/agregar_contenido_form.html'
    titulo_pagina = "Agregar "

    if tipo_contenido == 'pelicula':
        FormClase = PeliculaForm
        titulo_pagina += "Película"
    elif tipo_contenido == 'serie':
        FormClase = SerieForm
        titulo_pagina += "Serie"
    elif tipo_contenido == 'anime':
        FormClase = AnimeForm
        titulo_pagina += "Anime"
    else:
        raise Http404("Tipo de contenido no válido")

    if request.method == 'POST':
        form = FormClase(request.POST, request.FILES or None) # Para portadas si las subes localmente
        if form.is_valid():
            instancia = form.save()
            # return redirect(instancia.get_absolute_url()) # Redirigir al detalle
            return redirect('catalogo:inicio') # O a donde quieras
    else:
        form = FormClase()

    return render(request, template_name, {'form': form, 'titulo_pagina': titulo_pagina, 'tipo_contenido': tipo_contenido})

@superuser_required
def agregar_temporada(request, tipo_parent): # tipo_parent puede ser 'serie' o 'anime'
    FormClase = None
    template_name = 'catalogo/admin_forms/agregar_temporada_form.html'
    titulo_pagina = "Agregar Temporada a "

    if tipo_parent == 'serie':
        FormClase = TemporadaForm
        titulo_pagina += "Serie"
    elif tipo_parent == 'anime':
        FormClase = TemporadaAnimeForm
        titulo_pagina += "Anime"
    else:
        raise Http404("Tipo de contenido padre no válido")

    if request.method == 'POST':
        form = FormClase(request.POST)
        if form.is_valid():
            temporada = form.save()
            if tipo_parent == 'serie':
                return redirect(temporada.serie.get_absolute_url())
            elif tipo_parent == 'anime':
                return redirect(temporada.anime.get_absolute_url())
    else:
        form = FormClase()
    
    # Para el selector del padre en el form
    parent_items = None
    if tipo_parent == 'serie':
        parent_items = Serie.objects.all()
    elif tipo_parent == 'anime':
        parent_items = Anime.objects.all()

    return render(request, template_name, {'form': form, 'titulo_pagina': titulo_pagina, 'parent_items': parent_items, 'tipo_parent': tipo_parent})


@superuser_required
def agregar_episodio(request, tipo_parent): # tipo_parent puede ser 'serie' o 'anime'
    FormClase = None
    template_name = 'catalogo/admin_forms/agregar_episodio_form.html'
    titulo_pagina = "Agregar Episodio a "

    if tipo_parent == 'serie':
        FormClase = EpisodioForm
        titulo_pagina += "Serie"
    elif tipo_parent == 'anime':
        FormClase = EpisodioAnimeForm
        titulo_pagina += "Anime"
    else:
        raise Http404("Tipo de contenido padre no válido")

    if request.method == 'POST':
        form = FormClase(request.POST)
        if form.is_valid():
            episodio = form.save()
            # Redirigir al detalle de la serie/anime a la que pertenece el episodio
            if tipo_parent == 'serie':
                return redirect(episodio.temporada.serie.get_absolute_url())
            elif tipo_parent == 'anime':
                return redirect(episodio.temporada_anime.anime.get_absolute_url())
    else:
        form = FormClase()
    
    # Para el selector de temporada en el form
    temporadas = None
    if tipo_parent == 'serie':
        temporadas = Temporada.objects.select_related('serie').all()
    elif tipo_parent == 'anime':
        temporadas = TemporadaAnime.objects.select_related('anime').all()

    return render(request, template_name, {'form': form, 'titulo_pagina': titulo_pagina, 'temporadas': temporadas, 'tipo_parent': tipo_parent})


# --- VISTA DE BÚSQUEDA ---
def busqueda(request):
    query = request.GET.get('q', '')
    tipo_filtro = request.GET.get('tipo', '') # peliculas, series, animes, todos

    resultados_peliculas = []
    resultados_series = []
    resultados_animes = []

    if query:
        q_obj = Q(titulo__icontains=query) | Q(sinopsis__icontains=query) | Q(elenco__icontains=query) | Q(generos__nombre__icontains=query)
        
        if tipo_filtro == 'peliculas' or tipo_filtro == 'todos' or not tipo_filtro:
            resultados_peliculas = Pelicula.objects.filter(q_obj).distinct().prefetch_related('generos')
        
        if tipo_filtro == 'series' or tipo_filtro == 'todos' or not tipo_filtro:
            resultados_series = Serie.objects.filter(q_obj).distinct().prefetch_related('generos')

        if tipo_filtro == 'animes' or tipo_filtro == 'todos' or not tipo_filtro:
            resultados_animes = Anime.objects.filter(q_obj).distinct().prefetch_related('generos')
    
    # Combinar resultados para la plantilla si es 'todos' o no hay filtro específico
    todos_los_resultados = []
    if tipo_filtro == 'todos' or not tipo_filtro:
        # No es ideal ordenar después de obtenerlos si son muchos, pero para este caso puede funcionar.
        # Si el rendimiento es crítico, se necesitaría una solución más compleja (ej. full-text search engine como Elasticsearch)
        todos_los_resultados = sorted(
            chain(resultados_peliculas, resultados_series, resultados_animes),
            key=lambda x: x.titulo # O por fecha_subida, etc.
        )
    # Si hay filtro específico, solo pasamos ese tipo de resultado
    elif tipo_filtro == 'peliculas':
        todos_los_resultados = list(resultados_peliculas)
    elif tipo_filtro == 'series':
        todos_los_resultados = list(resultados_series)
    elif tipo_filtro == 'animes':
        todos_los_resultados = list(resultados_animes)


    context = {
        'query': query,
        'tipo_filtro': tipo_filtro,
        'resultados': todos_los_resultados,
        'resultados_peliculas': resultados_peliculas if tipo_filtro == 'peliculas' else [], # Para mostrar por separado si se quiere
        'resultados_series': resultados_series if tipo_filtro == 'series' else [],
        'resultados_animes': resultados_animes if tipo_filtro == 'animes' else [],
        'hay_resultados': bool(todos_los_resultados)
    }
    return render(request, 'catalogo/resultados_busqueda.html', context)