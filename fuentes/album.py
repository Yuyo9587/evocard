"""Sección "Compartí tus fotos" que se agrega a todas las invitaciones."""
import re

ALBUM_CSS = """
/* Álbum de fotos */
.album-card{text-align:center}
.album-card .campo{text-align:left;margin-bottom:16px}
.album-card input[type=text]{border:1px solid var(--line);border-radius:10px;padding:10px 12px;width:100%;background:transparent}
.album-barra{height:6px;border-radius:9px;background:var(--line);overflow:hidden;margin:16px auto 0;max-width:320px}
.album-barra i{display:block;height:100%;width:0;background:var(--acc,var(--leaf,var(--lila)));transition:width .3s}
"""

def album_html(lab="Álbum de la fiesta", titulo="Compartí tus fotos",
               sub="Durante la fiesta, subí acá tus fotos. Todas van a un mismo álbum para que nadie se pierda nada."):
    return f"""  <section id="album">
    <div class="wrap">
      <span class="lab">{lab}</span>
      <h2>{titulo}</h2>
      <p class="sub">{sub}</p>
      <div class="card album-card">
        <input type="file" id="albumArchivos" accept="image/*" multiple hidden>
        <div class="campo" id="albumAutorCampo">
          <label for="albumAutor">Tu nombre (opcional)</label>
          <input type="text" id="albumAutor" maxlength="60" autocomplete="name">
        </div>
        <button class="btn" type="button" id="albumBtn">Subir mis fotos</button>
        <div class="album-barra" id="albumBarra" hidden><i id="albumProg"></i></div>
        <p class="fine" id="albumMsg" role="status"></p>
      </div>
    </div>
  </section>

"""

CONEXION_FOTO = """,
  async subirFoto(datos){
    let r;
    try{ r = await fetch(INV.planilla, { method:"POST", headers:{ "Content-Type":"text/plain;charset=utf-8" }, body: JSON.stringify(Object.assign({ accion:"subirFoto" }, datos)) }); }
    catch(e){ throw new Error("No se pudo subir. Revisá tu conexión e intentá de nuevo."); }
    const j = await r.json();
    if(!j.ok) throw new Error(j.error || "No se pudo subir la foto.");
    return j.foto;
  }
};"""

ALBUM_JS = r"""
/* ===== Álbum de fotos: los invitados suben sus fotos a la carpeta del evento ===== */
(function(){
  const sec = $("#album"); if(!sec) return;
  if(INV.albumActivo === false){ sec.hidden = true; return; }
  const btn = $("#albumBtn"), input = $("#albumArchivos"), msg = $("#albumMsg"), barra = $("#albumBarra"), prog = $("#albumProg");
  const real = !!INV.planilla;
  if(!real && INV.album){   /* sin planilla, pero con un álbum externo (por ejemplo Google Fotos) */
    $("#albumAutorCampo").hidden = true; btn.textContent = "Abrir el álbum";
    btn.addEventListener("click", () => window.open(INV.album, "_blank", "noopener")); return;
  }
  btn.addEventListener("click", () => input.click());
  async function achicar(archivo){
    const url = URL.createObjectURL(archivo);
    try{
      const img = await new Promise((ok, mal) => { const im = new Image(); im.onload = () => ok(im); im.onerror = () => mal(new Error("No se pudo leer la foto.")); im.src = url; });
      const k = Math.min(1, 1600 / Math.max(img.naturalWidth, img.naturalHeight));
      const c = document.createElement("canvas"); c.width = Math.round(img.naturalWidth * k); c.height = Math.round(img.naturalHeight * k);
      c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
      return c.toDataURL("image/jpeg", 0.82).split(",")[1];
    } finally { URL.revokeObjectURL(url); }
  }
  input.addEventListener("change", async () => {
    const archivos = [...input.files].filter(f => /^image\//.test(f.type) || /\.(jpe?g|png|heic|heif|webp)$/i.test(f.name)); input.value = "";
    if(!archivos.length) return;
    if(!real){ msg.textContent = `Elegiste ${archivos.length === 1 ? "1 foto" : archivos.length + " fotos"}. En la invitación real se suben al álbum del evento y se ven en el panel.`; return; }
    btn.disabled = true; barra.hidden = false; let subidas = 0, fallas = 0, aviso = "";
    for(let i = 0; i < archivos.length; i++){
      msg.textContent = `Subiendo ${i + 1} de ${archivos.length}…`; prog.style.width = (i / archivos.length * 100) + "%";
      try{
        const datos = await achicar(archivos[i]);
        await Conexion.subirFoto({ tipo:"image/jpeg", datos, autor: $("#albumAutor").value.trim() || INV.invitado || "" });
        subidas++;
      }catch(e){ fallas++; if(/cerrado|lleno/.test(e.message)){ aviso = e.message; break; } }
    }
    prog.style.width = "100%"; btn.disabled = false; setTimeout(() => barra.hidden = true, 1500);
    msg.textContent = aviso || (subidas
      ? `¡Gracias! ${subidas === 1 ? "Se subió 1 foto" : "Se subieron " + subidas + " fotos"} al álbum.` + (fallas ? ` ${fallas === 1 ? "Una no se pudo subir" : fallas + " no se pudieron subir"}: probá de nuevo con esas.` : "")
      : "No se pudo subir. Revisá tu conexión e intentá de nuevo.");
  });
  /* El QR de las mesas abre la invitación con ?album: saltea el sobre y va directo a esta sección */
  if(new URLSearchParams(location.search).has("album")){
    const s = $("#sobre"); s.classList.add("abriendo", "abierto"); $("#musica").hidden = false;
    setTimeout(() => sec.scrollIntoView({ block:"start" }), 150);
  }
})();
"""

def agregar(html, sub=None):
    """Agrega la sección, el CSS, la conexión y el código del álbum a una invitación ya armada."""
    if 'id="albumBtn"' in html: return html
    # sección antes de la confirmación
    html, n = re.subn(r'(  <section[^>]*id="confirmar")', lambda m: album_html(**({"sub": sub} if sub else {})) + m.group(1), html, count=1)
    assert n == 1, "no encontré la sección de confirmación"
    # CSS
    html = html.replace("</style>", ALBUM_CSS + "</style>", 1)
    # INV.albumActivo
    html, n = re.subn(r'(\n  /\* Dirección de la planilla del evento)',
                      '\n  /* Álbum de fotos: true = los invitados pueden subir fotos (necesita planilla). false = se oculta la sección */\n  albumActivo: true,\\1', html, count=1)
    if n == 0:  # modelos generados (JSON con comillas)
        html, n = re.subn(r'(\n  /\* Dirección de la planilla del evento[^\n]*\*/\n  "planilla")',
                          '\n  /* Álbum de fotos: true = los invitados pueden subir fotos (necesita planilla). false = se oculta la sección */\n  "albumActivo": true,\\1', html, count=1)
    assert n == 1, "no encontré INV.planilla"
    # Conexion.subirFoto
    html, n = re.subn(r'\n    return j\.invitado;\n  \}\n\};', '\n    return j.invitado;\n  }' + CONEXION_FOTO, html, count=1)
    assert n == 1, "no encontré el final de Conexion"
    # código, antes de iniciarInvitado();
    i = html.rindex("iniciarInvitado();")
    html = html[:i] + ALBUM_JS + "\n" + html[i:]
    return html
