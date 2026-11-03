"""Invitación especial: 3ra Reunión Federativa 2026 (FABVPBA). No va a la página de venta."""
import sys, base64, os
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from base import armar, cuenta_regresiva, confirmacion, ESQUELETO
from modelos import txt, inv, mapa
from album import agregar

IMG = sys.argv[1]   # carpeta con plaza.jpg, escuela.jpg, emblema.jpg, logo.png
def uri(n, t):
    return f"data:{t};base64," + base64.b64encode(open(os.path.join(IMG, n), "rb").read()).decode()
EMBLEMA, LOGO = uri("emblema.jpg","image/jpeg"), uri("logo.png","image/png")
PLAZA, ESCUELA = "https://evocard.com.ar/fed/saladillo-plaza.jpg", "https://evocard.com.ar/fed/saladillo-escuela.jpg"

ACTIVIDADES = [
  ("desayuno", "Desayuno en el Cuartel (07:00)"),
  ("operaciones", "Reunión Sistemas de Operaciones, Capacitación y Escuela de Cadetes"),
  ("fondo", "Reunión del Fondo Federativo"),
  ("admin", "Capacitación Administrativa (subsidios, TAD, documentación)"),
  ("ley", "Capacitación Ley 13.802 y Documentación Bomberil Básica"),
  ("gib", "Capacitación GIB"),
  ("genero", "Capacitación para Regionales de Género y Ética"),
]
checks = "\n".join(f'              <label class="check"><input type="checkbox" value="{t}"><span>{t}</span></label>' for _, t in ACTIVIDADES)

m = dict(
  titulo="3ra Reunión Federativa 2026 · Saladillo",
  fuentes="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:ital,wght@0,400;0,500;0,600;1,400&display=swap",
  css=""":root{
  --bg:#0D0D0E; --banda:#151515; --card:#1A1918; --card-solid:#1A1918;
  --ink:#F3EBDA; --muted:#B4AA97; --acc:#C9A24A; --acc-ink:#111; --acc-soft:rgba(201,162,74,.14); --hl:#D6B25E; --line:rgba(201,162,74,.28); --field:#121212; --err:#F2A99B;
  --f-title:"Barlow Condensed", "Arial Narrow", sans-serif; --title-w:700; --h2:2.4rem;
  --f-body:"Barlow", "Segoe UI", sans-serif; --f-sans:"Barlow", "Segoe UI", sans-serif; --f-num:"Barlow Condensed", sans-serif; --num-w:700;
  --fs:17px; --sub-style:normal; --r-btn:4px; --r-card:8px; --dot-r:0; --bullet:"▸";
  --sobre-bg:radial-gradient(circle at 50% 30%,#2A2416,#0B0B0B 70%);
  --env-back:#B8923F; --env-front:#D4B467; --env-flap:#C7A353; --env-ink:#1A140A;
  --seal-bg:#0D0D0E; --seal-ink:#C9A24A; --seal-font:"Barlow Condensed", sans-serif; --seal-fs:1.4rem;
  --tap:#D6B25E; --ribbon-bg:#C9A24A; --ribbon-ink:#111;
  color-scheme:dark;
}""",
  css_extra="""h2{text-transform:uppercase;letter-spacing:.02em}
.env .seal{overflow:hidden;border:2px solid #C9A24A;width:92px;height:92px;margin:-46px 0 0 -46px}
.env .seal img{width:100%;height:100%;object-fit:cover;display:block}
.env .to{font-size:.92rem;padding-inline:12px;line-height:1.3}
.oro{background:linear-gradient(180deg,#E6CB86,#B98F3A 55%,#D9BC72);-webkit-background-clip:text;background-clip:text;color:transparent}
.portada{padding-top:76px}
.emblema{width:112px;height:112px;border-radius:50%;border:2px solid var(--acc);display:block;margin:0 auto 18px;box-shadow:0 0 0 6px rgba(201,162,74,.08)}
.quien{font-size:.98rem;color:var(--muted);max-width:34ch;margin:0 auto}
.num-reunion{font-family:var(--f-title);font-weight:600;font-size:1.25rem;letter-spacing:.24em;text-transform:uppercase;color:var(--hl);margin-top:18px}
.titulo{font-family:var(--f-title);font-weight:700;font-size:clamp(3rem,15vw,4.6rem);line-height:.95;text-transform:uppercase;margin-block:6px 18px}
.fecha-grande{font-weight:600;color:var(--ink)}
.sede{margin-top:12px;font-family:var(--f-title);font-size:1.15rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.foto{margin:34px auto 0;border-radius:var(--r-card);overflow:hidden;border:1px solid var(--line);position:relative}
.foto img{display:block;width:100%;height:auto}
.foto figcaption{position:absolute;left:0;right:0;bottom:0;padding:26px 14px 10px;background:linear-gradient(transparent,rgba(0,0,0,.8));font-family:var(--f-title);font-weight:600;letter-spacing:.14em;text-transform:uppercase;font-size:.95rem;color:#E9D49A;text-align:left}
.texto{font-size:1.05rem;line-height:1.65;color:var(--ink);text-align:left;margin-top:18px}
.texto + .texto{margin-top:12px}
.presentes{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:22px}
.presentes div{border:1px solid var(--line);border-radius:var(--r-card);padding:14px 10px;font-family:var(--f-title);font-weight:600;font-size:1.12rem;letter-spacing:.04em;text-transform:uppercase;color:var(--hl);background:var(--acc-soft)}
.timeline .h{font-family:var(--f-title);font-weight:700;font-size:1.15rem;color:var(--hl)}
.timeline h3{font-family:var(--f-body);font-weight:600;font-size:1.05rem}
.timeline p{font-size:.95rem}
.simul{list-style:none;margin:8px 0 0;padding:0;display:grid;gap:7px}
.timeline .simul li{display:block;padding:0 0 0 14px;position:relative;color:var(--ink);font-size:.95rem;line-height:1.4}
.timeline .simul li::before{content:"";position:absolute;left:0;top:.55em;bottom:auto;width:6px;height:6px;background:var(--acc);border:0}
.timeline .simul li::before{display:block}
.aviso{margin-top:10px;border-left:3px solid var(--acc);background:var(--acc-soft);padding:10px 12px;font-size:.92rem;color:var(--ink);border-radius:0 6px 6px 0}
.lugar{display:grid;gap:4px;text-align:left}
.lugar b{font-family:var(--f-title);font-weight:700;font-size:1.35rem;letter-spacing:.02em;text-transform:uppercase}
.lugar p{color:var(--muted)}
.lugar + .lugar{margin-top:14px}
.gib{display:grid;gap:8px;justify-items:center}
.gib b{font-family:var(--f-title);font-size:1.6rem;text-transform:uppercase;letter-spacing:.04em;color:var(--hl);line-height:1.1}
.checks{display:grid;gap:8px}
.check{display:flex;gap:10px;align-items:flex-start;font-size:.95rem;line-height:1.35;cursor:pointer}
.check input{accent-color:#C9A24A;width:18px;height:18px;margin-top:1px;flex:none}
footer img{width:150px;height:auto;display:block;margin:14px auto 0;border-radius:6px}
footer .lab{display:block}
@media (max-width:360px){.presentes{grid-template-columns:1fr}}""",
  sello=f'<img src="{EMBLEMA}" alt="">',
  cuerpo=f"""<main>
  <section class="portada">
    <div class="wrap">
      <p class="saludo" id="saludo">Invitación para Bomberos Voluntarios de Marcos Paz</p>
      <img class="emblema" src="{EMBLEMA}" alt="Escudo de la Federación de Asociaciones de Bomberos Voluntarios de la Provincia de Buenos Aires" style="margin-top:22px">
      <p class="quien">La Federación de Asociaciones de Bomberos Voluntarios de la Provincia de Buenos Aires los invita a participar de la</p>
      <p class="num-reunion" id="rNum">3ra Reunión</p>
      <h1 class="titulo oro" id="rTitulo">Federativa 2026</h1>
      <p class="fecha-grande" id="rFecha">Sábado 12 · 09 · 2026</p>
      <p class="sede" id="rSede">Saladillo · Región Centro Centro</p>
      <figure class="foto" id="rFoto1"><img src="{PLAZA}" alt="Foto de la ciudad"><figcaption>Ciudad de Saladillo</figcaption></figure>
    </div>
  </section>

{cuenta_regresiva("Faltan", "Cuenta regresiva")}

  <section class="banda">
    <div class="wrap">
      <span class="lab">El encuentro</span>
      <h2>Los esperamos</h2>
      <p class="texto" id="rTexto">En esta oportunidad, la Región Centro Centro y en particular los Bomberos Voluntarios de Saladillo nos recibirán para debatir propuestas y sentar las bases del progreso de nuestras entidades asociadas.</p>
      <p class="texto" id="rPresentesLab">En este importante encuentro estarán presentes:</p>
      <div class="presentes" id="rPresentes">
        <div>Comisión Directiva</div>
        <div>Presidentes de Regiones</div>
        <div>Directores de Sistemas</div>
        <div>Fondo Federativo</div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="lab" id="diaLab">Sábado 12 de septiembre</span>
      <h2>Cronograma</h2>
      <ol class="timeline" id="rCrono">
        <li data-parte="cena"><span class="h">07:00</span><div class="t"><h3>Desayuno en el Cuartel</h3><p>Rivadavia N° 2852, Saladillo</p><a target="_blank" rel="noopener" href="{mapa('Rivadavia 2852, Saladillo, Provincia de Buenos Aires')}">Cómo llegar</a></div></li>
        <li data-parte="cena"><span class="h">08:00</span><div class="t"><h3>Recibimiento de delegaciones y acreditación</h3><p>Escuela Secundaria N° 2 Manuel Pardal</p></div></li>
        <li data-parte="cena"><span class="h">08:30</span><div class="t"><h3>Reuniones y capacitaciones simultáneas</h3>
          <ul class="simul">
            <li>Reunión Sistemas de Operaciones, Capacitación y Escuela de Cadetes</li>
            <li>Reunión del Fondo Federativo</li>
            <li>Capacitación Administrativa, Rendición de Subsidios Nacionales y Provinciales, TAD, Documentación Administrativa</li>
            <li>Capacitación Ley 13.802 y Documentación Bomberil Básica</li>
            <li>Capacitación GIB</li>
            <li>Capacitación para Regionales de Género y Ética</li>
          </ul></div></li>
        <li data-parte="fiesta"><span class="h">10:00</span><div class="t"><h3>Acto Protocolar por Apertura de la 3ra Reunión Federativa</h3>
          <p class="aviso">Todas las personas de las reuniones y capacitaciones deben participar en el acto, por lo que se pide culminar o interrumpir las mismas durante este horario.</p></div></li>
        <li data-parte="fiesta"><span class="h">11:30</span><div class="t"><h3>Reunión de Comisión Directiva FABVPBA</h3></div></li>
      </ol>
    </div>
  </section>

  <section class="banda">
    <div class="wrap">
      <span class="lab">Lugar</span>
      <h2>Dónde</h2>
      <figure class="foto" style="margin-top:24px" id="rFoto2"><img src="{ESCUELA}" alt="Foto del lugar"></figure>
      <div id="rLugares">
      <div class="card lugar">
        <b>Escuela Secundaria N° 2 Manuel Pardal</b>
        <p>Av. Pereyra 3046, Saladillo, Provincia de Buenos Aires · desde las 8:00 h</p>
        <a target="_blank" rel="noopener" href="{mapa('Av. Pereyra 3046, Saladillo, Provincia de Buenos Aires')}">Cómo llegar</a>
      </div>
      <div class="card lugar">
        <b>Cuartel de Bomberos Voluntarios de Saladillo</b>
        <p>Rivadavia N° 2852 · desayuno a las 7:00 h</p>
        <a target="_blank" rel="noopener" href="{mapa('Rivadavia 2852, Saladillo, Provincia de Buenos Aires')}">Cómo llegar</a>
      </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="card gib" id="rAvisoCard">
        <span class="lab">Importante</span>
        <b id="rAviso">No olviden realizar su inscripción en el GIB</b>
        <p class="sub" id="rAvisoDet">La inscripción oficial se hace en el GIB. La confirmación de esta invitación nos ayuda a organizar la recepción de las delegaciones.</p>
      </div>
    </div>
  </section>

{confirmacion("Delegaciones", "Confirmación", "Confirmen la asistencia de su delegación.",
  "Sí, asistimos", "No podremos asistir",
  f'''          <div class="campo" data-si>
            <label for="responsable">Responsable de la delegación</label>
            <input type="text" id="responsable" data-extra="Responsable" maxlength="80" autocomplete="name">
          </div>
          <div class="campo" data-si>
            <label for="telefono">Teléfono de contacto</label>
            <input type="text" id="telefono" data-extra="Teléfono" maxlength="30" inputmode="tel" autocomplete="tel">
          </div>
          <fieldset data-si>
            <legend>¿En qué actividades participan?</legend>
            <div class="checks" id="actividades">
{checks}
            </div>
            <input type="hidden" id="actividadesTxt" data-extra="Actividades">
          </fieldset>
''', "Consultas o comentarios", "Invitación dirigida a las entidades asociadas.", menu=False)}
</main>

<footer>
  <p class="lab">Los esperamos</p>
  <img src="{LOGO}" alt="La Federación · Federación de Asociaciones de Bomberos Voluntarios de la Provincia de Buenos Aires">
</footer>""",
  ribbon="Boceto · invitación de prueba para la Reunión Federativa",
  inv=inv(invitado="Bomberos Voluntarios de Marcos Paz", lugares=6, fechaEvento="2026-09-12T08:00:00-03:00", fechaFin="2026-09-12T13:00:00-03:00",
          titulo="3ra Reunión Federativa 2026 · Saladillo", lugarAgenda="Escuela Secundaria N° 2 Manuel Pardal, Av. Pereyra 3046, Saladillo, Provincia de Buenos Aires", horaFiesta="10:00"),
  txt=txt(saludo="Invitación para", saludoGenerico="Invitación", reservamos="Reservamos", desdeLas="Los esperamos desde las",
          yaConfirmaste="Ya confirmaron", yaNoVienen="Nos avisaron que no podrán asistir.", siCambio="Si algo cambia, pueden modificar la respuesta.",
          elegi="Indiquen si asistirán para poder enviar.", usaLink="Para confirmar, usen el link que recibió su cuartel.",
          confirmaste="Confirmaron", nota="le llega a la Federación", graciasSi="¡Gracias, los esperamos!",
          graciasNo="Gracias por avisarnos", graciasNoP="Esperamos contar con ustedes en la próxima Reunión Federativa.",
          porWhatsapp="Completen los datos y la confirmación nos llega por WhatsApp.", faltaNombre="Escriban el nombre del cuartel para saber quién confirma.",
          abrioWhatsapp="Se abrió WhatsApp con la confirmación. Toquen Enviar para que nos llegue."),
  musica='{ onda:"sine", notas:[392,523.25,659.25,783.99,659.25,523.25,587.33,783.99], paso:850, volumen:0.035, cola:1.8 }',
  deco=r"""(function(){
  const c = $("#deco"), x = c.getContext("2d");
  function dibujar(){
    const dpr = window.devicePixelRatio || 1, W = innerWidth, H = innerHeight;
    c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    x.fillStyle = "#0D0D0E"; x.fillRect(0, 0, W, H);
    let s = 11; const rnd = () => (s = (s * 9301 + 49297) % 233280) / 233280;
    for(let i = 0; i < 260; i++){
      const y = rnd() * H, w = 40 + rnd() * W * .5, x0 = rnd() * W - w / 2;
      x.strokeStyle = `rgba(214,178,94,${.015 + rnd() * .035})`; x.lineWidth = .6 + rnd();
      x.beginPath(); x.moveTo(x0, y); x.lineTo(x0 + w, y); x.stroke();
    }
    const g = x.createLinearGradient(0, 0, 0, 5); g.addColorStop(0, "#E6CB86"); g.addColorStop(1, "#B98F3A");
    x.fillStyle = g; x.fillRect(0, 0, W, 4);
  }
  dibujar(); addEventListener("resize", dibujar);
})();""",
  extra_js=r"""/* ===== Datos de la reunión: se leen de la hoja "Reunión" y "Cronograma" de la planilla ===== */
const MESES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"];
const DIAS = ["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"];
const escH = t => String(t == null ? "" : t).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
const mapaUrl = q => "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(q);
function fotoUrl(v){
  const m = String(v).match(/\/d\/([A-Za-z0-9_-]{20,})/) || String(v).match(/[?&]id=([A-Za-z0-9_-]{20,})/);
  return m ? "https://drive.google.com/thumbnail?id=" + m[1] + "&sz=w1600" : String(v);
}
function ponerFoto(id, url, pie){
  const f = $(id); if(!f) return;
  if(!url){ f.hidden = true; return; }
  f.hidden = false; f.querySelector("img").src = fotoUrl(url);
  const c = f.querySelector("figcaption"); if(c){ c.textContent = pie || ""; c.hidden = !pie; }
}
function ajustarCuenta(){
  meta = new Date(INV.fechaEvento).getTime(); tick();
  const f = d => new Date(d).toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  const a = $("#agendar");
  if(a && !isNaN(meta)) a.href = "https://calendar.google.com/calendar/render?action=TEMPLATE&text=" + encodeURIComponent(INV.titulo)
    + "&dates=" + f(INV.fechaEvento) + "/" + f(INV.fechaFin) + "&location=" + encodeURIComponent(INV.lugarAgenda);
  const cd = $(".cd"), sec = cd && cd.closest("section"); if(!sec) return;
  const paso = Date.now() >= new Date(INV.fechaFin).getTime();
  cd.hidden = paso; if(a) a.hidden = paso;
  sec.querySelector(".lab").textContent = paso ? "Fecha" : "Faltan";
  sec.querySelector("h2").textContent = paso ? (window.DIA_LARGO || "") : "Cuenta regresiva";
}
async function cargarReunion(){
  if(!INV.planilla){ ajustarCuenta(); return; }
  let d;
  try{ d = await fetch(INV.planilla + "?accion=reunion").then(r => r.json()); }catch(e){ ajustarCuenta(); return; }
  if(!d || !d.ok){ ajustarCuenta(); return; }
  const r = d.reunion, cr = d.cronograma || [];
  const m = String(r.fecha || "").match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
  const hm = h => { const x = String(h || "").match(/(\d{1,2})[:.](\d{2})/); return x ? x[1].padStart(2,"0") + ":" + x[2] : "08:00"; };
  if(m){
    const [dd, mm, aa] = [m[1].padStart(2,"0"), m[2].padStart(2,"0"), m[3]];
    const dia = new Date(Number(aa), Number(mm) - 1, Number(dd));
    $("#rFecha").textContent = DIAS[dia.getDay()] + " " + dd + " · " + mm + " · " + aa;
    window.DIA_LARGO = DIAS[dia.getDay()] + " " + Number(dd) + " de " + MESES[Number(mm) - 1];
    $("#diaLab").textContent = window.DIA_LARGO;
    INV.fechaEvento = aa + "-" + mm + "-" + dd + "T" + hm(r.hora) + ":00-03:00";
    INV.fechaFin = aa + "-" + mm + "-" + dd + "T" + hm(r.hora_fin || "13:00") + ":00-03:00";
  }
  $("#rNum").textContent = (r.numero || "") + " Reunión";
  $("#rTitulo").textContent = "Federativa " + (r.anio || "");
  $("#rSede").textContent = [r.ciudad, r.region].filter(Boolean).join(" · ");
  INV.titulo = (r.numero || "") + " Reunión Federativa " + (r.anio || "") + (r.ciudad ? " · " + r.ciudad : "");
  INV.lugarAgenda = [r.lugar, r.direccion].filter(Boolean).join(", ");
  document.title = INV.titulo;
  ponerFoto("#rFoto1", r.foto1, r.foto1_pie);
  ponerFoto("#rFoto2", r.foto2, "");
  $("#rTexto").textContent = r.texto || "";
  const pres = String(r.presentes || "").split(",").map(x => x.trim()).filter(Boolean);
  $("#rPresentesLab").hidden = !pres.length;
  $("#rPresentes").innerHTML = pres.map(x => "<div>" + escH(x) + "</div>").join("");
  /* cronograma: las actividades seguidas con la misma hora se agrupan como simultáneas */
  const grupos = [];
  cr.forEach(a => { const g = grupos[grupos.length - 1]; if(g && g.hora === a.hora) g.items.push(a); else grupos.push({ hora: a.hora, items: [a] }); });
  $("#rCrono").innerHTML = grupos.map(g => {
    let cuerpo;
    if(g.items.length > 1){
      cuerpo = "<h3>Actividades simultáneas</h3><ul class=\"simul\">" + g.items.map(a => "<li>" + escH(a.titulo) + (a.detalle ? " · <span style=\"color:var(--muted)\">" + escH(a.detalle) + "</span>" : "") + "</li>").join("") + "</ul>";
    } else {
      const a = g.items[0];
      cuerpo = "<h3>" + escH(a.titulo) + "</h3>" + (a.detalle ? (a.destacar ? "<p class=\"aviso\">" : "<p>") + escH(a.detalle) + "</p>" : "")
        + (a.mapa ? "<a target=\"_blank\" rel=\"noopener\" href=\"" + mapaUrl(a.mapa) + "\">Cómo llegar</a>" : "");
    }
    return "<li><span class=\"h\">" + escH(g.hora) + "</span><div class=\"t\">" + cuerpo + "</div></li>";
  }).join("");
  /* lugares */
  let lug = "";
  if(r.lugar) lug += "<div class=\"card lugar\"><b>" + escH(r.lugar) + "</b><p>" + escH(r.direccion || "") + (r.hora ? " · desde las " + escH(r.hora) + " h" : "") + "</p>"
    + (r.direccion ? "<a target=\"_blank\" rel=\"noopener\" href=\"" + mapaUrl(r.direccion) + "\">Cómo llegar</a>" : "") + "</div>";
  if(r.lugar2) lug += "<div class=\"card lugar\"><b>" + escH(r.lugar2) + "</b><p>" + escH([r.direccion2, r.detalle2].filter(Boolean).join(" · ")) + "</p>"
    + (r.direccion2 ? "<a target=\"_blank\" rel=\"noopener\" href=\"" + mapaUrl(r.direccion2) + "\">Cómo llegar</a>" : "") + "</div>";
  $("#rLugares").innerHTML = lug;
  /* aviso */
  $("#rAvisoCard").closest("section").hidden = !r.aviso;
  $("#rAviso").textContent = r.aviso || ""; $("#rAvisoDet").textContent = r.aviso_detalle || "";
  /* actividades para marcar al confirmar */
  const marcar = cr.filter(a => a.marcar);
  $("#actividades").innerHTML = marcar.map(a => "<label class=\"check\"><input type=\"checkbox\" value=\"" + escH(a.titulo) + "\"><span>" + escH(a.titulo) + " (" + escH(a.hora) + ")</span></label>").join("");
  const fsAct = $("#actividades").closest("fieldset");
  if(!marcar.length){ fsAct.removeAttribute("data-si"); fsAct.hidden = true; }
  ajustarCuenta();
}
cargarReunion();

/* Actividades marcadas: se juntan en un campo que llega al panel o al WhatsApp */
(function(){
  const caja = $("#actividades"), txt = $("#actividadesTxt");
  caja.addEventListener("change", () => { txt.value = [...caja.querySelectorAll("input:checked")].map(i => i.value).join("; "); });
})();
""",
)

html = armar(m)   # sin álbum de fotos
for a, b in [("<legend>¿Vienen?</legend>", "<legend>¿Asistirá su cuartel?</legend>"),
             ("¿Cuántos van a ir?", "¿Cuántas personas integran la delegación?"),
             ("Tu nombre y apellido", "Cuartel"),
             ("Para Familia Gómez", "Para Bomberos Voluntarios de Marcos Paz"),
             ("Tocá para abrir", "Toquen para abrir"),
             ("const meta = new Date(INV.fechaEvento).getTime();", "let meta = new Date(INV.fechaEvento).getTime();"),
             ('generico ? "Para vos"', 'generico ? "Para las entidades asociadas"'),
             ('"planilla": ""', '"planilla": "https://script.google.com/macros/s/AKfycbzaKVEa_d3gW49ZBuZEBbe63h8A0Eahp5C1yroO8nCYYccVUqcgnvwdpnA1fpVv-Ay5OQ/exec"')]:
    assert a in html, a
    html = html.replace(a, b)
dest = sys.argv[2]
open(os.path.join(dest, "reunion-federativa.html"), "w", encoding="utf8").write(ESQUELETO + html + "\n</body>\n</html>\n")
print(len(html))
