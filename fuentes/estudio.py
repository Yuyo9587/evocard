"""Arma estudio.html (el editor privado de modelos) a partir de estudio_plantilla.html.
Mete adentro, sin cambiarlas, las mismas piezas que usan todos los modelos (base.py y album.py),
así lo que se diseña en el estudio funciona igual con la planilla y el panel.

Uso: python3 estudio.py <carpeta de salida>      (por ejemplo: python3 estudio.py ..)
Si falta estudio_plantilla.html, se recupera sola a partir de ../estudio.html.
"""
import json, os, sys
from base import CSS_BASE, JS_BASE, ESQUELETO
from album import ALBUM_CSS, ALBUM_JS, CONEXION_FOTO, album_html

aqui = os.path.dirname(os.path.abspath(__file__))
piezas = dict(CSS_BASE=CSS_BASE, JS_BASE=JS_BASE, ESQUELETO=ESQUELETO,
              ALBUM_CSS=ALBUM_CSS, ALBUM_JS=ALBUM_JS, CONEXION_FOTO=CONEXION_FOTO,
              ALBUM_HTML=album_html())
texto = json.dumps(piezas, ensure_ascii=False).replace("</", "<\\/")
ruta_plantilla = os.path.join(aqui, "estudio_plantilla.html")
if not os.path.exists(ruta_plantilla):
    import re
    publicado = open(os.path.join(aqui, "..", "estudio.html"), encoding="utf8").read()
    recuperada, n = re.subn(r"^const BASE = .*;$", "/*__BASE__*/", publicado, count=1, flags=re.M)
    assert n == 1, "no encontré la línea BASE en estudio.html"
    open(ruta_plantilla, "w", encoding="utf8").write(recuperada)
    print("recuperé estudio_plantilla.html desde estudio.html")
plantilla = open(ruta_plantilla, encoding="utf8").read()
assert "/*__BASE__*/" in plantilla
salida = plantilla.replace("/*__BASE__*/", "const BASE = " + texto + ";")
destino = os.path.join(sys.argv[1] if len(sys.argv) > 1 else os.path.join(aqui, ".."), "estudio.html")
open(destino, "w", encoding="utf8").write(salida)
print("listo:", destino, len(salida), "bytes")
