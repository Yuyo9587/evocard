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
