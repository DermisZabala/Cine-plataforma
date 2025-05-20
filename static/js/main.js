document.addEventListener('DOMContentLoaded', function() {

    // ---- Funcionalidad "Mostrar más" Contenido ----
    const btnMostrarMasContenido = document.getElementById('btnMostrarMasContenido'); // Cambiado ID
    const contenidoGrid = document.getElementById('contenidoGrid');
    
    if (btnMostrarMasContenido && contenidoGrid) {
        let currentOffsetContenido = parseInt(btnMostrarMasContenido.dataset.initialItems || '10');
        const itemsPerLoadContenido = parseInt(btnMostrarMasContenido.dataset.itemsPerLoad || '5');
        const tipoContenido = btnMostrarMasContenido.dataset.tipo;

        btnMostrarMasContenido.addEventListener('click', function() {
            btnMostrarMasContenido.disabled = true;
            btnMostrarMasContenido.textContent = 'Cargando...';

            let url = '';
            if (tipoContenido === 'pelicula') {
                url = `/peliculas/cargar_mas/?offset=${currentOffsetContenido}`;
            } else if (tipoContenido === 'serie') {
                url = `/series/cargar_mas/?offset=${currentOffsetContenido}`;
            } else if (tipoContenido === 'anime') {
                url = `/animes/cargar_mas/?offset=${currentOffsetContenido}`;
            }

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.html) {
                        contenidoGrid.insertAdjacentHTML('beforeend', data.html);
                        currentOffsetContenido += itemsPerLoadContenido;
                    }
                    if (data.hay_mas) {
                        btnMostrarMasContenido.disabled = false;
                        btnMostrarMasContenido.textContent = 'Mostrar más';
                    } else {
                        btnMostrarMasContenido.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Error al cargar más contenido:', error);
                    btnMostrarMasContenido.disabled = false;
                    btnMostrarMasContenido.textContent = 'Error. Intentar de nuevo';
                });
        });
    }

    // ---- Acordeón para Temporadas ----
    const temporadaHeaders = document.querySelectorAll('.temporada-header');
    temporadaHeaders.forEach(header => {
        header.addEventListener('click', function() {
            this.classList.toggle('active');
            const episodiosLista = this.nextElementSibling;
            if (this.classList.contains('active')) {
                episodiosLista.style.maxHeight = episodiosLista.scrollHeight + "px";
            } else {
                episodiosLista.style.maxHeight = "0";
            }
        });
    });

    // ---- Reproducción de Episodios (Actualizar Iframe) ----
    const episodioPlayerContainer = document.getElementById('episodioPlayerContainer');
    const episodioIframe = document.getElementById('episodioPlayer');
    
    if (episodioPlayerContainer && episodioIframe) {
        const botonesReproducir = document.querySelectorAll('.btn-reproducir-episodio');
        
        botonesReproducir.forEach(boton => {
            boton.addEventListener('click', function(e) {
                e.preventDefault();
                const iframeUrl = this.dataset.iframeUrl;
                const episodioTitulo = this.dataset.episodioTitulo || "Episodio";

                if (iframeUrl) {
                    episodioIframe.src = iframeUrl;
                    episodioPlayerContainer.style.display = 'block';
                    episodioPlayerContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    
                    const reproductorTitulo = episodioPlayerContainer.querySelector('h3');
                    if(reproductorTitulo) reproductorTitulo.textContent = `Reproduciendo: ${episodioTitulo}`;
                }
            });
        });

        const initialEpisodioUrl = episodioPlayerContainer.dataset.initialEpisodioUrl;
        const initialEpisodioTitulo = episodioPlayerContainer.dataset.initialEpisodioTitulo;

        if (initialEpisodioUrl) {
             episodioIframe.src = initialEpisodioUrl;
             episodioPlayerContainer.style.display = 'block';
             const reproductorTitulo = episodioPlayerContainer.querySelector('h3');
             if(reproductorTitulo && initialEpisodioTitulo) reproductorTitulo.textContent = `Reproduciendo: ${initialEpisodioTitulo}`;

             const temporadaActiva = document.querySelector('.temporada-header.initially-active');
             if(temporadaActiva) {
                temporadaActiva.classList.add('active');
                const episodiosLista = temporadaActiva.nextElementSibling;
                // Esperar un poco para que el DOM se actualice si es necesario
                setTimeout(() => {
                    episodiosLista.style.maxHeight = episodiosLista.scrollHeight + "px";
                }, 100);
             }
        } else {
            episodioPlayerContainer.style.display = 'none';
        }
    }

    // ---- Activar el link de navegación actual ----
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('header nav ul li a');
    navLinks.forEach(link => {
        // Comparar solo el path, ignorar query params
        if (link.getAttribute('href').split('?')[0] === currentPath) {
            link.classList.add('active');
        }
    });


    // ---- Funcionalidad "Mostrar más Comentarios" ----
    const btnMostrarMasComentarios = document.getElementById('btnMostrarMasComentarios');
    const listaComentarios = document.getElementById('listaComentarios');
    const COMENTARIOS_POR_PAGINA = 5; // Debe coincidir con el backend

    if (btnMostrarMasComentarios && listaComentarios) {
        let currentOffsetComentarios = parseInt(btnMostrarMasComentarios.dataset.initialItems || COMENTARIOS_POR_PAGINA.toString());
        const contentTypeId = btnMostrarMasComentarios.dataset.contentTypeId;
        const objectId = btnMostrarMasComentarios.dataset.objectId;

        btnMostrarMasComentarios.addEventListener('click', function() {
            btnMostrarMasComentarios.disabled = true;
            btnMostrarMasComentarios.textContent = 'Cargando...';

            const url = `/comentarios/cargar_mas/?content_type_id=${contentTypeId}&object_id=${objectId}&offset=${currentOffsetComentarios}`;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.html) {
                        listaComentarios.insertAdjacentHTML('beforeend', data.html);
                        currentOffsetComentarios += COMENTARIOS_POR_PAGINA;
                    }
                    if (data.hay_mas) {
                        btnMostrarMasComentarios.disabled = false;
                        btnMostrarMasComentarios.textContent = 'Mostrar más comentarios';
                    } else {
                        btnMostrarMasComentarios.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Error al cargar más comentarios:', error);
                    btnMostrarMasComentarios.disabled = false;
                    btnMostrarMasComentarios.textContent = 'Error. Intentar de nuevo';
                });
        });
    }

    // Ocultar mensaje de comentario enviado después de unos segundos
    const mensajeComentario = document.querySelector('.mensaje-comentario-enviado');
    if (mensajeComentario) {
        setTimeout(() => {
            mensajeComentario.style.transition = 'opacity 0.5s ease';
            mensajeComentario.style.opacity = '0';
            setTimeout(() => mensajeComentario.remove(), 500);
        }, 4000); // 4 segundos
    }

});