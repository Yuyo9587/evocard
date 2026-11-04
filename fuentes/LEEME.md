# Fuentes (código de trabajo)

Copia de respaldo del código con el que se generan las páginas. No hace falta para que el sitio funcione.

## Reunión Federativa (invitación de la Federación)
- `Codigo-federativa.gs`: programa de la planilla "Reunión Federativa 2026 - Invitaciones" (cuenta secretaria@federacionbomberos.org.ar). Es lo que va pegado en Extensiones > Apps Script. Incluye el envío de mails, las hojas Reunión y Cronograma y "Empezar una reunión nueva".
- `federativa.py`: genera `reunion-federativa.html`. Usa `base.py`, `modelos.py` y `album.py` (en la misma carpeta) y las imágenes `emblema.jpg` y `logo.png`.
  Uso: `python3 federativa.py <carpeta con emblema.jpg y logo.png> <carpeta de salida>`
- Dirección del programa publicado (/exec): está escrita dentro de `federativa.py`.

## Evocard
- `Codigo.gs`: programa de la planilla de cada evento de Evocard (con álbum de fotos).
- `base.py`, `modelos.py`, `album.py`: generador de los modelos Confeti, Nube, Gala, Luz y Agenda.

## Estudio (editor privado de modelos)
- `estudio.html` (en la raíz del sitio): página con contraseña para diseñar modelos desde cero o copiando uno existente. Descarga la **ficha** (.evocard.json, para seguir editando) y la **invitación** (.html, lista para subir).
- Se arma con `python3 estudio.py ..` a partir de `estudio_plantilla.html` (si no está en esta carpeta, `estudio.py` la recupera sola desde `estudio.html`). Mete adentro las mismas piezas de `base.py` y `album.py`, así las invitaciones del Estudio funcionan igual con la planilla y el panel.
- Permite cargar letras propias (.ttf, .otf, .woff, .woff2 o el .zip tal cual se baja); quedan guardadas adentro de la invitación.
- La contraseña es un "no pasar" (el sitio es público). Para cambiarla, se cambia `CLAVE_HUELLA` en `estudio_plantilla.html`.

