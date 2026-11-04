from base import armar, cuenta_regresiva, confirmacion

def txt(**k):
    d = dict(saludo="Querida", saludoGenerico="Querido invitado", reservamos="Reservamos",
             desdeLas="Te esperamos desde las", yaConfirmaste="Ya confirmaste",
             yaNoVienen="Nos avisaste que no pueden venir.", siCambio="Si algo cambia, podés modificar tu respuesta.",
             elegi="Elegí si vienen o no para poder enviar.", usaLink="Para confirmar, usá el link personal que te enviaron.",
             confirmaste="Confirmaste", nota="le llega a la familia", graciasSi="¡Te esperamos!",
             graciasNo="Te vamos a extrañar", graciasNoP="Gracias por avisarnos con tiempo.",
             porWhatsapp="Completá tus datos y tu respuesta nos llega por WhatsApp.",
             faltaNombre="Escribí tu nombre para que sepamos quién confirma.",
             abrioWhatsapp="Se abrió WhatsApp con tu respuesta. Tocá Enviar para que nos llegue.")
    d.update(k)
    import json
    return json.dumps(d, ensure_ascii=False, indent=2)

def inv(**k):
    import json
    base = dict(invitado="Familia Gómez", lugares=3)
    base.update(k)
    base["whatsapp"] = ""
    base["maxLugares"] = 6
    base["planilla"] = ""
    s = json.dumps(base, ensure_ascii=False, indent=2)
    s = s.replace('"whatsapp": ""', '/* Plan Básico (sin planilla): número del cliente que recibe las confirmaciones por WhatsApp, con código de país. Ej: 5491112345678 */\n  "whatsapp": ""')
    s = s.replace('"maxLugares": 6', '/* Plan Básico: hasta cuántas personas puede confirmar cada invitado */\n  "maxLugares": 6')
    return s.replace('"planilla": ""', '/* Dirección de la planilla del evento (termina en /exec). Vacía = invitación de muestra. */\n  "planilla": ""')

def mapa(q):
    from urllib.parse import quote
    return "https://www.google.com/maps/search/?api=1&amp;query=" + quote(q)

def dato_copia(etq, id_, valor):
    return f'<div class="dato"><span>{etq}</span><b id="{id_}">{valor}</b><button class="copiar" type="button" data-copy="{id_}">Copiar</button></div>'

MODELOS = {}

# ---------------------------------------------------------------- CONFETI (cumpleaños infantil)
MODELOS["confeti"] = dict(
  titulo="¡Cumplo 6! · Benja",
  fuentes="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700&display=swap",
  css=""":root{
  --bg:#FFF4E2; --banda:#FFE6C4; --card:#FFFFFF; --card-solid:#FFFFFF; --ink:#3A2410; --muted:#7A5A3E;
  --acc:#E2572B; --acc-ink:#FFFFFF; --acc-soft:#FDE3D8; --hl:#2E8B87; --line:#F0D2AC; --field:#FFFAF2;
  --f-title:"Baloo 2", "Arial Rounded MT Bold", sans-serif; --title-w:800; --h2:2.5rem;
  --f-body:"Nunito", "Segoe UI", sans-serif; --f-sans:"Nunito", "Segoe UI", sans-serif; --f-num:"Baloo 2", sans-serif; --num-w:800;
  --sub-style:normal; --r-btn:14px; --r-card:22px; --dot-r:3px; --bullet:"★"; --fs:18px;
  --sobre-bg:radial-gradient(circle at 20% 20%,#FFD8A8 0 6px,transparent 7px) 0 0/46px 46px, radial-gradient(circle at 70% 60%,#9FD8D3 0 5px,transparent 6px) 0 0/58px 58px, #FFE9C7;
  --env-back:#2E8B87; --env-front:#3AA19C; --env-flap:#257571; --env-ink:#FFFFFF;
  --seal-bg:radial-gradient(circle at 35% 30%,#FF9A73 0,#E2572B 65%); --seal-ink:#FFFFFF; --seal-font:"Baloo 2", sans-serif; --seal-fs:2.6rem;
  --tap:#E2572B; --ribbon-bg:#3A2410; --ribbon-ink:#FFE9C7;
  color-scheme:light;
}""",
  css_extra=""".cumplo{font-family:var(--f-title);font-weight:800;font-size:1.5rem;color:var(--hl);margin-top:18px}
.edad{display:grid;place-items:center;width:128px;height:128px;margin:14px auto 6px;border-radius:50%;background:var(--acc);color:#fff;font-family:var(--f-title);font-weight:800;font-size:5rem;line-height:1;padding-top:8px;transform:rotate(-6deg);box-shadow:0 10px 0 -2px #B9411D}
.nombre{font-family:var(--f-title);font-weight:800;font-size:clamp(4rem,19vw,6rem);line-height:1;margin-block:6px 16px;color:var(--ink)}
.timeline h3,.lugar h3{font-family:var(--f-title);font-weight:700}
.lugar{display:grid;gap:4px}
.lugar h3{font-size:1.5rem}
.lugar .hora{font-family:var(--f-title);font-weight:800;font-size:2rem;color:var(--acc)}
.choice span{font-weight:600}
footer .nombre{font-size:3.4rem;margin:4px 0 0}""",
  sello="B",
  cuerpo=f"""<main>
  <section class="portada">
    <div class="wrap">
      <p class="saludo" id="saludo">Hola Familia Gómez</p>
      <p class="cumplo">¡Cumplo</p>
      <div class="edad" aria-hidden="true">6</div>
      <h1 class="nombre">Benja</h1>
      <p class="fecha-grande">Sáb 10 · 04 · 2027</p>
      <p class="invita">Vení a saltar, jugar y comer torta conmigo. ¡Va a estar buenísimo!</p>
    </div>
  </section>

{cuenta_regresiva("Falta poquito", "¿Cuánto falta?")}

  <section class="banda">
    <div class="wrap">
      <span class="lab" id="diaLab">Sábado 10 de abril</span>
      <h2>Dónde y cuándo</h2>
      <div class="card lugar">
        <span class="hora">16 a 19 h</span>
        <h3>Peloteros Saltarín</h3>
        <p class="sub">Av. Belgrano 1234 · Marcos Paz</p>
        <a target="_blank" rel="noopener" href="{mapa('Marcos Paz, Buenos Aires')}">Cómo llegar</a>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="lab">Para tener en cuenta</span>
      <h2>Qué traer</h2>
      <div class="card">
        <ul class="lista">
          <li>Ropa cómoda para saltar y correr.</li>
          <li>Medias antideslizantes: son obligatorias en el pelotero.</li>
          <li>Muchas ganas de jugar.</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="banda">
    <div class="wrap">
      <span class="lab">Regalos</span>
      <h2>Si querés regalarme algo</h2>
      <p class="sub">Me encantan los dinosaurios y los autitos. Si preferís, también podés colaborar con este alias.</p>
      <div class="card">
        <div class="datos">
          <div class="dato"><span>Titular</span><b>Carla Ruiz (mamá)</b></div>
          {dato_copia("Alias", "alias", "benja.cumple6")}
        </div>
        <p class="err" id="copyMsg" role="status"></p>
      </div>
    </div>
  </section>

{confirmacion("Confirmá antes del 3 de abril", "¿Venís a mi cumple?", "Reservamos 3 lugares para Familia Gómez.",
  "¡Sí, vamos!", "No podemos",
  '''          <div class="campo" data-si>
            <label for="chicos">¿Cuántos son chicos?</label>
            <select id="chicos" data-extra="Chicos"></select>
          </div>
''', "Un mensaje para Benja", "Los adultos que acompañan también cuentan como lugar.", banda=False,
  menu_opciones=["Ninguno", "Sin TACC (celíaco)", "Vegetariano", "Alergia (la aclaramos en el mensaje)"])}
</main>

<footer>
  <p class="lab">¡Te espero!</p>
  <p class="nombre">Benja</p>
</footer>""",
  ribbon="Modelo Confeti · invitación de muestra con datos de ejemplo",
  inv=inv(fechaEvento="2027-04-10T16:00:00-03:00", fechaFin="2027-04-10T19:00:00-03:00",
          titulo="Cumple de Benja", lugarAgenda="Peloteros Saltarín, Marcos Paz, Buenos Aires", horaFiesta="16:00"),
  txt=txt(saludo="Hola", saludoGenerico="¡Hola!", nota="les llega a los papás de Benja",
          graciasSi="¡Genial, te espero!", graciasNo="¡Te vamos a extrañar!", graciasNoP="Gracias por avisar. ¡Otra vez será!"),
  musica='{ onda:"triangle", notas:[523.25,659.25,783.99,1046.5,783.99,659.25,587.33,698.46,880,1174.66,880,698.46,523.25,783.99,659.25,523.25], paso:240, volumen:0.04, cola:0.45 }',
  deco=r"""(function(){
  const c = $("#deco"), x = c.getContext("2d");
  const colores = ["#E2572B","#2E8B87","#F2B134","#7DC4BF","#F28C6B","#3A6EA5"];
  let W, H, piezas = [];
  function armar(){
    const dpr = window.devicePixelRatio || 1; W = innerWidth; H = innerHeight;
    c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    const n = Math.round(W * H / 14000);
    piezas = Array.from({length: n}, () => ({ x: Math.random() * W, y: Math.random() * H, w: 5 + Math.random() * 6, h: 8 + Math.random() * 8,
      a: Math.random() * 6.28, va: (Math.random() - .5) * .08, vy: .4 + Math.random() * .9, vx: (Math.random() - .5) * .4, c: colores[Math.floor(Math.random() * colores.length)], redondo: Math.random() > .7 }));
  }
  function dibujar(){
    x.clearRect(0, 0, W, H); x.globalAlpha = .55;
    for(const p of piezas){
      if(!reduce){ p.y += p.vy; p.x += p.vx; p.a += p.va; if(p.y > H + 20){ p.y = -20; p.x = Math.random() * W; } }
      x.save(); x.translate(p.x, p.y); x.rotate(p.a); x.fillStyle = p.c;
      if(p.redondo){ x.beginPath(); x.arc(0, 0, p.w * .55, 0, 6.28); x.fill(); } else x.fillRect(-p.w / 2, -p.h / 2, p.w, p.h * Math.abs(Math.cos(p.a)) + 2);
      x.restore();
    }
    if(!reduce) requestAnimationFrame(dibujar);
  }
  armar(); addEventListener("resize", () => { armar(); if(reduce) dibujar(); }); dibujar();
})();""")

# ---------------------------------------------------------------- NUBE (baby shower)
MODELOS["nube"] = dict(
  titulo="Baby shower · Esperando a Emma",
  fuentes="https://fonts.googleapis.com/css2?family=Parisienne&family=Quicksand:wght@400;500;600;700&display=swap",
  css=""":root{
  --bg:#F3F7FB; --banda:linear-gradient(180deg,rgba(234,242,249,0),#EAF2F9 15%,#FBEFEA 85%,rgba(251,239,234,0)); --card:rgba(255,255,255,.88); --card-solid:#FFFFFF;
  --ink:#33475A; --muted:#687C8F; --acc:#6F98BA; --acc-ink:#FFFFFF; --acc-soft:#E5EFF7; --hl:#D08A70; --line:#DCE6EF; --field:#FAFCFE;
  --f-title:"Parisienne", "Snell Roundhand", cursive; --h2:3rem;
  --f-body:"Quicksand", "Segoe UI", sans-serif; --f-sans:"Quicksand", "Segoe UI", sans-serif; --f-num:"Quicksand", sans-serif; --num-w:600;
  --sub-style:normal; --bullet:"♡"; --fs:18px;
  --sobre-bg:linear-gradient(180deg,#E6F0F8,#FDF6F0);
  --env-back:#D7E5F2; --env-front:#E4EEF7; --env-flap:#C9DAEA; --env-ink:#33475A;
  --seal-bg:radial-gradient(circle at 35% 30%,#F8D9CD 0,#E3A48E 70%); --seal-ink:#FFFFFF; --seal-font:"Parisienne", cursive; --seal-fs:2.6rem;
  --tap:#6F98BA; --ribbon-bg:#33475A; --ribbon-ink:#FFFFFF;
  color-scheme:light;
}""",
  css_extra=""".esperando{font-family:var(--f-sans);font-weight:600;font-size:.95rem;letter-spacing:.3em;text-transform:uppercase;color:var(--hl);margin-top:24px}
.esperando2{font-family:var(--f-sans);font-size:1.05rem;color:var(--muted);margin-top:14px}
.nombre{font-family:var(--f-title);font-weight:400;font-size:clamp(5rem,24vw,7.5rem);line-height:1;margin-block:0 16px;color:var(--ink)}
.timeline h3{font-weight:700}
footer .nombre{font-size:4rem;margin:0}""",
  sello="E",
  cuerpo=f"""<main>
  <section class="portada">
    <div class="wrap">
      <p class="saludo" id="saludo">Querida Familia Gómez</p>
      <p class="esperando">Baby shower</p>
      <p class="esperando2">Esperando a</p>
      <h1 class="nombre">Emma</h1>
      <p class="fecha-grande">Dom 18 · 04 · 2027</p>
      <p class="invita">Estamos contando los días para conocerla. ¿Nos acompañás a celebrar su llegada?</p>
    </div>
  </section>

{cuenta_regresiva("Llega pronto", "Cuenta regresiva")}

  <section class="banda">
    <div class="wrap">
      <span class="lab" id="diaLab">Domingo 18 de abril</span>
      <h2>Momentos de la tarde</h2>
      <ol class="timeline">
        <li><span class="h">17:00</span><div class="t"><h3>Bienvenida y merienda</h3><p>Casa de la abuela Inés · Marcos Paz</p><a target="_blank" rel="noopener" href="{mapa('Marcos Paz, Buenos Aires')}">Cómo llegar</a></div></li>
        <li><span class="h">18:00</span><div class="t"><h3>Juegos</h3><p>¿Quién adivina cuánto mide la panza?</p></div></li>
        <li><span class="h">18:45</span><div class="t"><h3>Apertura de regalos</h3><p>Con mucha emoción (y pañuelitos)</p></div></li>
        <li><span class="h">19:30</span><div class="t"><h3>Torta y brindis</h3><p>Por Emma</p></div></li>
      </ol>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="lab">Regalos sugeridos</span>
      <h2>Lo que más necesitamos</h2>
      <div class="card">
        <ul class="lista">
          <li>Pañales talle P y M</li>
          <li>Ropita de 3 a 6 meses</li>
          <li>Toallitas húmedas y cremitas</li>
        </ul>
        <p class="sub" style="margin-top:18px">Si preferís, podés colaborar con este alias:</p>
        <div class="datos">
          <div class="dato"><span>Titular</span><b>Ana Torres</b></div>
          {dato_copia("Alias", "alias", "emma.babyshower")}
        </div>
        <p class="err" id="copyMsg" role="status"></p>
      </div>
    </div>
  </section>

{confirmacion("Confirmá antes del 11 de abril", "¿Venís?", "Reservamos 3 lugares para Familia Gómez.",
  "¡Sí, voy!", "No puedo ir",
  '''          <div class="campo" data-si>
            <label for="consejo">Un consejo para los futuros papás</label>
            <input type="text" id="consejo" data-extra="Consejo" maxlength="140" placeholder="Opcional" autocomplete="off">
          </div>
''', "Un mensaje para Emma", "Esta invitación es personal. Te pedimos no reenviarla.",
  menu_opciones=["Ninguno", "Vegetariano", "Sin TACC (celíaco)", "Otro (lo aclaramos en el mensaje)"])}
</main>

<footer>
  <p class="lab">Te esperamos</p>
  <p class="nombre">Emma</p>
</footer>""",
  ribbon="Modelo Nube · invitación de muestra con datos de ejemplo",
  inv=inv(fechaEvento="2027-04-18T17:00:00-03:00", fechaFin="2027-04-18T20:00:00-03:00",
          titulo="Baby shower de Emma", lugarAgenda="Marcos Paz, Buenos Aires", horaFiesta="17:00"),
  txt=txt(nota="les llega a Ana y Diego", graciasSi="¡Te esperamos!", graciasNoP="Gracias por avisarnos. Emma también te manda un abrazo."),
  musica='{ onda:"sine", notas:[783.99,659.25,587.33,523.25,587.33,659.25,587.33,392,523.25,587.33,659.25,783.99,659.25,587.33,523.25,523.25], paso:620, volumen:0.05, cola:2.2 }',
  deco=r"""(function(){
  const c = $("#deco"), x = c.getContext("2d");
  let W, H, nubes = [];
  function nube(cx, cy, s, a){
    x.globalAlpha = a; x.fillStyle = "#FFFFFF";
    for(const [dx, dy, r] of [[-1.1, .15, .55], [-.45, -.25, .75], [.35, -.15, .65], [1, .2, .5], [0, .3, .6]]){ x.beginPath(); x.arc(cx + dx * s, cy + dy * s, r * s, 0, 6.28); x.fill(); }
  }
  function armar(){
    const dpr = window.devicePixelRatio || 1; W = innerWidth; H = innerHeight;
    c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    nubes = Array.from({length: 7}, (_, i) => ({ x: Math.random() * W, y: (i + .5) / 7 * H, s: 28 + Math.random() * 30, v: .08 + Math.random() * .14, a: .55 + Math.random() * .35 }));
  }
  function dibujar(){
    const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#E6F0F8"); g.addColorStop(1, "#FDF4EE");
    x.globalAlpha = 1; x.fillStyle = g; x.fillRect(0, 0, W, H);
    for(const n of nubes){ if(!reduce){ n.x += n.v; if(n.x - n.s * 2 > W) n.x = -n.s * 2; } nube(n.x, n.y, n.s, n.a); }
    if(!reduce) requestAnimationFrame(dibujar);
  }
  armar(); addEventListener("resize", () => { armar(); if(reduce) dibujar(); }); dibujar();
})();""")

# ---------------------------------------------------------------- GALA (institucional)
MODELOS["gala"] = dict(
  titulo="80 aniversario · Club Social Las Acacias",
  fuentes="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Jost:wght@400;500&display=swap",
  css=""":root{
  --bg:#0F1A30; --banda:rgba(201,165,92,.07); --card:rgba(255,255,255,.035); --card-solid:#16243F;
  --ink:#F2EBDD; --muted:#B9B2A4; --acc:#C9A55C; --acc-ink:#14213D; --acc-soft:rgba(201,165,92,.14); --hl:#C9A55C; --line:rgba(201,165,92,.3); --field:#14213D; --err:#F2A99B;
  --f-title:"Cinzel", "Trajan Pro", Georgia, serif; --title-w:500; --h2:2.1rem;
  --f-body:"Cormorant Garamond", Georgia, serif; --f-sans:"Jost", "Futura", sans-serif; --f-num:"Cinzel", Georgia, serif;
  --r-btn:2px; --r-card:4px; --dot-r:0; --bullet:"◆";
  --sobre-bg:radial-gradient(circle at 50% 30%,#1D2E52,#0B1426 72%);
  --env-back:#14213D; --env-front:#1A2A4A; --env-flap:#22355A; --env-ink:#F2EBDD;
  --seal-bg:radial-gradient(circle at 35% 30%,#F1DDA8 0,#C9A55C 55%,#97793D 100%); --seal-ink:#14213D; --seal-font:"Cinzel", serif; --seal-fs:1.7rem;
  --tap:#C9A55C; --ribbon-bg:#C9A55C; --ribbon-ink:#14213D;
  color-scheme:dark;
}""",
  css_extra="""h2{letter-spacing:.06em}
.marco{border:1px solid var(--line);outline:1px solid var(--line);outline-offset:7px;padding:44px 18px 40px;margin-inline:8px}
.aniv{font-family:var(--f-title);font-size:3.6rem;line-height:1;color:var(--acc);margin-top:18px}
.aniv small{display:block;font-family:var(--f-sans);font-size:.72rem;letter-spacing:.4em;text-transform:uppercase;color:var(--muted);margin-top:8px}
.entidad{font-family:var(--f-title);font-weight:500;font-size:clamp(1.9rem,8vw,2.6rem);line-height:1.15;letter-spacing:.04em;margin-block:18px 6px}
.tipo{font-style:italic;font-size:1.4rem;color:var(--muted);margin-bottom:18px}
.timeline .t::before{transform:rotate(45deg)}
.valor{font-family:var(--f-title);font-size:2.4rem;color:var(--acc);line-height:1.1}
.valor small{display:block;font-family:var(--f-sans);font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-top:6px}
footer .entidad{font-size:1.6rem;margin:6px 0 0}
#cbu{font-size:.95rem;letter-spacing:.01em}""",
  sello="80",
  cuerpo=f"""<main>
  <section class="portada">
    <div class="wrap">
      <div class="marco">
        <p class="saludo" id="saludo">Estimada Familia Gómez</p>
        <p class="aniv">80<small>Aniversario</small></p>
        <h1 class="entidad">Club Social Las Acacias</h1>
        <p class="tipo">Cena de gala</p>
        <p class="fecha-grande">Sáb 05 · 06 · 2027</p>
        <p class="invita">Tenemos el honor de invitarlos a celebrar ochenta años de historia compartida.</p>
      </div>
    </div>
  </section>

{cuenta_regresiva("Faltan", "Cuenta regresiva")}

  <section class="banda">
    <div class="wrap">
      <span class="lab" id="diaLab">Sábado 5 de junio</span>
      <h2>Programa</h2>
      <ol class="timeline">
        <li data-parte="cena"><span class="h">21:00</span><div class="t"><h3>Recepción</h3><p>Salón principal del Club · Marcos Paz</p><a target="_blank" rel="noopener" href="{mapa('Marcos Paz, Buenos Aires')}">Cómo llegar</a></div></li>
        <li data-parte="cena"><span class="h">22:00</span><div class="t"><h3>Palabras de la Comisión Directiva</h3><p>Ochenta años en primera persona</p></div></li>
        <li data-parte="cena"><span class="h">22:30</span><div class="t"><h3>Cena</h3><p>Con mesas por institución</p></div></li>
        <li data-parte="fiesta"><span class="h">23:45</span><div class="t"><h3>Reconocimientos</h3><p>A socios fundadores y entidades amigas</p></div></li>
        <li data-parte="fiesta"><span class="h">00:30</span><div class="t"><h3>Brindis y baile</h3><p>Con orquesta en vivo</p></div></li>
      </ol>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="lab">Vestimenta</span>
      <h2>Etiqueta</h2>
      <p class="sub">Traje oscuro. Vestido largo o de cóctel.</p>
    </div>
  </section>

  <section class="banda">
    <div class="wrap">
      <span class="lab">Valor de la tarjeta</span>
      <h2>Reservá tu lugar</h2>
      <div class="card">
        <p class="valor">$45.000<small>Por persona · incluye cena, bebidas y brindis</small></p>
        <div class="datos" style="margin-top:22px">
          <div class="dato"><span>Titular</span><b>Club Social Las Acacias</b></div>
          {dato_copia("Alias", "alias", "acacias.80.gala")}
          {dato_copia("CBU", "cbu", "0000003100098765432109")}
        </div>
        <p class="err" id="copyMsg" role="status"></p>
        <p class="sub" style="margin-top:6px">Abone antes del 20 de mayo y envíe el comprobante a la secretaría del Club.</p>
      </div>
    </div>
  </section>

{confirmacion("Antes del 20 de mayo", "Confirmación", "Reservamos 3 lugares para Familia Gómez.",
  "Asistiremos", "No podremos asistir",
  '''          <div class="campo" data-si>
            <label for="institucion">Institución o grupo (para armar las mesas)</label>
            <input type="text" id="institucion" data-extra="Institución" maxlength="80" placeholder="Ej: Bomberos Voluntarios" autocomplete="off">
          </div>
''', "Un saludo para el Club", "Invitación personal e intransferible.", banda=False)}
</main>

<footer>
  <p class="lab">Los esperamos</p>
  <p class="entidad">Las Acacias · 1947 – 2027</p>
</footer>""",
  ribbon="Modelo Gala · invitación de muestra con datos de ejemplo",
  inv=inv(fechaEvento="2027-06-05T21:00:00-03:00", fechaFin="2027-06-06T03:00:00-03:00",
          titulo="Cena de gala 80 aniversario · Club Social Las Acacias", lugarAgenda="Club Social Las Acacias, Marcos Paz, Buenos Aires", horaFiesta="23:45"),
  txt=txt(saludo="Estimada", saludoGenerico="Estimado invitado", desdeLas="Los esperamos desde las",
          yaConfirmaste="Ya confirmó", yaNoVienen="Nos avisó que no podrá asistir.", siCambio="Si algo cambia, puede modificar su respuesta.",
          elegi="Indique si asistirán para poder enviar.", usaLink="Para confirmar, use el link personal que recibió.",
          confirmaste="Confirmó", nota="le llega a la Comisión Directiva", graciasSi="Muchas gracias",
          graciasNo="Lamentamos su ausencia", graciasNoP="Gracias por avisarnos con anticipación.",
          porWhatsapp="Complete sus datos y su respuesta nos llega por WhatsApp.", faltaNombre="Escriba su nombre para saber quién confirma.",
          abrioWhatsapp="Se abrió WhatsApp con su respuesta. Toque Enviar para que nos llegue."),
  musica='{ onda:"sine", notas:[392,493.88,587.33,783.99,739.99,587.33,493.88,440,523.25,659.25,783.99,659.25,587.33,493.88,440,392], paso:520, volumen:0.045, cola:1.8 }',
  deco=r"""(function(){
  const c = $("#deco"), x = c.getContext("2d");
  function dibujar(){
    const dpr = window.devicePixelRatio || 1, W = innerWidth, H = innerHeight;
    c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    const g = x.createRadialGradient(W / 2, 0, 0, W / 2, 0, Math.max(W, H)); g.addColorStop(0, "#1A2B4D"); g.addColorStop(1, "#0B1426");
    x.fillStyle = g; x.fillRect(0, 0, W, H);
    x.strokeStyle = "rgba(201,165,92,.16)"; x.lineWidth = 1;
    const abanico = (cx, cy, desde, hasta, r) => {
      for(let i = 0; i <= 12; i++){ const a = desde + (hasta - desde) * i / 12; x.beginPath(); x.moveTo(cx, cy); x.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r); x.stroke(); }
      for(const k of [.35, .55, .75]){ x.beginPath(); x.arc(cx, cy, r * k, desde, hasta); x.stroke(); }
    };
    const r = Math.min(W, H) * .42;
    abanico(0, 0, 0, Math.PI / 2, r); abanico(W, 0, Math.PI / 2, Math.PI, r);
    abanico(0, H, -Math.PI / 2, 0, r); abanico(W, H, Math.PI, Math.PI * 1.5, r);
  }
  dibujar(); addEventListener("resize", dibujar);
})();""")

# ---------------------------------------------------------------- LUZ (comunión y bautismo)
MODELOS["luz"] = dict(
  titulo="Mi primera comunión · Joaquín",
  fuentes="https://fonts.googleapis.com/css2?family=Pinyon+Script&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Jost:wght@400;500&display=swap",
  css=""":root{
  --bg:#FFFDF8; --banda:linear-gradient(180deg,rgba(245,240,229,0),#F5F0E5 15%,#F5F0E5 85%,rgba(245,240,229,0)); --card:rgba(255,255,255,.9); --card-solid:#FFFFFF;
  --ink:#4B3F2A; --muted:#7D7260; --acc:#A88848; --acc-ink:#FFFFFF; --acc-soft:#F4EDDD; --hl:#A88848; --line:#E8DFCB; --field:#FFFEFB;
  --f-title:"Pinyon Script", "Snell Roundhand", cursive; --h2:2.9rem;
  --f-body:"Cormorant Garamond", Georgia, serif; --f-sans:"Jost", "Futura", sans-serif; --f-num:"Cormorant Garamond", Georgia, serif; --bullet:"✦";
  --sobre-bg:radial-gradient(circle at 50% 30%,#FFFFFF,#F1EBDD 75%);
  --env-back:#EDE5D3; --env-front:#F6F1E6; --env-flap:#E6DCC6; --env-ink:#4B3F2A;
  --seal-bg:radial-gradient(circle at 35% 30%,#F3E3BC 0,#C9A962 55%,#9C7D3E 100%); --seal-ink:#FFFFFF; --seal-font:"Pinyon Script", cursive; --seal-fs:2.6rem;
  --tap:#A88848; --ribbon-bg:#4B3F2A; --ribbon-ink:#FFFDF8;
  color-scheme:light;
}""",
  css_extra=""".cruz{display:block;width:26px;height:40px;margin:22px auto 8px}
.motivo{font-family:var(--f-sans);font-size:.85rem;letter-spacing:.32em;text-transform:uppercase;color:var(--acc)}
.nombre{font-family:var(--f-title);font-weight:400;font-size:clamp(4.4rem,21vw,6.6rem);line-height:1.05;margin-block:4px 16px;color:var(--ink)}
.padrinos{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:22px}
.padrinos div{display:grid;gap:2px}
.padrinos span{font-family:var(--f-sans);font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
.padrinos b{font-family:var(--f-title);font-weight:400;font-size:1.8rem;line-height:1.2;white-space:nowrap}
@media (max-width:380px){.padrinos{grid-template-columns:1fr}}
footer .nombre{font-size:3.6rem;margin:0}""",
  sello="J",
  cuerpo=f"""<main>
  <section class="portada">
    <div class="wrap">
      <p class="saludo" id="saludo">Querida Familia Gómez</p>
      <svg class="cruz" viewBox="0 0 26 40" aria-hidden="true"><rect x="11.5" y="0" width="3" height="40" fill="#A88848"/><rect x="2" y="10" width="22" height="3" fill="#A88848"/></svg>
      <p class="motivo">Mi primera comunión</p>
      <h1 class="nombre">Joaquín</h1>
      <p class="fecha-grande">Dom 10 · 10 · 2027</p>
      <p class="invita">Quiero que me acompañes en este día tan especial para mí y para mi familia.</p>
    </div>
  </section>

{cuenta_regresiva("Falta poco", "Cuenta regresiva")}

  <section class="banda">
    <div class="wrap">
      <span class="lab" id="diaLab">Domingo 10 de octubre</span>
      <h2>La celebración</h2>
      <ol class="timeline">
        <li><span class="h">10:00</span><div class="t"><h3>Santa misa</h3><p>Parroquia San José · Marcos Paz</p><a target="_blank" rel="noopener" href="{mapa('Parroquia San José, Marcos Paz, Buenos Aires')}">Cómo llegar</a></div></li>
        <li><span class="h">13:00</span><div class="t"><h3>Almuerzo familiar</h3><p>Quinta Los Tilos · Marcos Paz</p><a target="_blank" rel="noopener" href="{mapa('Marcos Paz, Buenos Aires')}">Cómo llegar</a></div></li>
        <li><span class="h">16:00</span><div class="t"><h3>Torta y recuerdos</h3><p>Para cerrar el día en familia</p></div></li>
      </ol>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="lab">Me acompañan</span>
      <h2>Mis padrinos</h2>
      <div class="card">
        <div class="padrinos">
          <div><span>Madrina</span><b>Sofía Ruiz</b></div>
          <div><span>Padrino</span><b>Martín López</b></div>
        </div>
      </div>
    </div>
  </section>

  <section class="banda">
    <div class="wrap">
      <span class="lab">Un recuerdo</span>
      <h2>Si querés hacerme un regalo</h2>
      <p class="sub">Tu compañía es el mejor regalo. Si además querés hacerme un obsequio, este es el alias de mis papás.</p>
      <div class="card">
        <div class="datos">
          <div class="dato"><span>Titular</span><b>Marcela Díaz (mamá)</b></div>
          {dato_copia("Alias", "alias", "joaco.comunion")}
        </div>
        <p class="err" id="copyMsg" role="status"></p>
      </div>
    </div>
  </section>

{confirmacion("Antes del 1 de octubre", "Confirmá tu asistencia", "Reservamos 3 lugares para Familia Gómez.",
  "¡Sí, vamos!", "No podemos ir", "", "Unas palabras para Joaquín", "Esta invitación es personal. Te pedimos no reenviarla.", banda=False,
  menu_opciones=["Ninguno", "Vegetariano", "Sin TACC (celíaco)", "Menú infantil", "Otro (lo aclaramos en el mensaje)"])}
</main>

<footer>
  <p class="lab">Te espero</p>
  <p class="nombre">Joaquín</p>
</footer>""",
  ribbon="Modelo Luz · para comunión, confirmación o bautismo · datos de ejemplo",
  inv=inv(fechaEvento="2027-10-10T10:00:00-03:00", fechaFin="2027-10-10T17:00:00-03:00",
          titulo="Primera comunión de Joaquín", lugarAgenda="Parroquia San José, Marcos Paz, Buenos Aires", horaFiesta="13:00"),
  txt=txt(nota="le llega a la familia de Joaquín", graciasSi="¡Gracias por acompañarme!", graciasNo="Te vamos a extrañar"),
  musica='{ onda:"sine", notas:[523.25,587.33,659.25,523.25,698.46,659.25,587.33,523.25,659.25,698.46,783.99,659.25,587.33,523.25,493.88,523.25], paso:700, volumen:0.045, cola:2.4 }',
  deco=r"""(function(){
  const c = $("#deco"), x = c.getContext("2d");
  let W, H, motas = [];
  function armar(){
    const dpr = window.devicePixelRatio || 1; W = innerWidth; H = innerHeight;
    c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    motas = Array.from({length: Math.round(W * H / 22000)}, () => ({ x: Math.random() * W, y: Math.random() * H, r: .8 + Math.random() * 1.8, v: .1 + Math.random() * .25, f: Math.random() * 6.28 }));
  }
  function dibujar(t){
    x.clearRect(0, 0, W, H);
    const cx = W / 2, rays = 14, giro = reduce ? 0 : (t || 0) / 60000;
    for(let i = 0; i < rays; i++){
      const a = Math.PI * (.08 + .84 * i / (rays - 1)) + Math.sin(giro + i) * .01;
      const g = x.createLinearGradient(cx, -40, cx + Math.cos(a) * H, -40 + Math.sin(a) * H);
      g.addColorStop(0, "rgba(232,210,150,.22)"); g.addColorStop(1, "rgba(232,210,150,0)");
      x.fillStyle = g; x.beginPath(); x.moveTo(cx, -40);
      x.lineTo(cx + Math.cos(a - .035) * H * 1.2, -40 + Math.sin(a - .035) * H * 1.2);
      x.lineTo(cx + Math.cos(a + .035) * H * 1.2, -40 + Math.sin(a + .035) * H * 1.2); x.fill();
    }
    for(const m of motas){
      if(!reduce){ m.y -= m.v; if(m.y < -5){ m.y = H + 5; m.x = Math.random() * W; } }
      x.globalAlpha = .35 + .3 * Math.sin(m.f + (t || 0) / 900); x.fillStyle = "#D9BE7A";
      x.beginPath(); x.arc(m.x, m.y, m.r, 0, 6.28); x.fill(); x.globalAlpha = 1;
    }
    if(!reduce) requestAnimationFrame(dibujar);
  }
  armar(); addEventListener("resize", () => { armar(); if(reduce) dibujar(0); }); dibujar(0);
})();""")

# ---------------------------------------------------------------- AGENDA (corporativo, congresos, jornadas: sin valor de tarjeta)
MODELOS["agenda"] = dict(
  titulo="Jornada de Innovación Pyme 2027",
  fuentes="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
  css=""":root{
  --bg:#F5F7FA; --banda:#EAF1F0; --card:#FFFFFF; --card-solid:#FFFFFF;
  --ink:#16233A; --muted:#5B6678; --acc:#0F7B6C; --acc-ink:#FFFFFF; --acc-soft:#E3F1EE; --hl:#0F7B6C; --line:#D9E0E7; --field:#FFFFFF;
  --f-title:"Plus Jakarta Sans", "Segoe UI", system-ui, sans-serif; --title-w:700; --h2:2rem;
  --f-body:"Plus Jakarta Sans", "Segoe UI", system-ui, sans-serif; --f-sans:"Plus Jakarta Sans", "Segoe UI", system-ui, sans-serif; --f-num:"Plus Jakarta Sans", system-ui, sans-serif; --num-w:700;
  --fs:17px; --sub-style:normal; --r-btn:10px; --r-card:14px; --dot-r:2px; --bullet:"→";
  --sobre-bg:linear-gradient(160deg,#16233A,#0E3B42 85%);
  --env-back:#E9EEF3; --env-front:#F5F7FA; --env-flap:#DDE5EC; --env-ink:#16233A;
  --seal-bg:linear-gradient(145deg,#14967F,#0B5E53); --seal-ink:#FFFFFF; --seal-font:"Plus Jakarta Sans", system-ui, sans-serif; --seal-fs:1.5rem;
  --tap:#BFE3DC; --ribbon-bg:#16233A; --ribbon-ink:#FFFFFF;
  color-scheme:light;
}""",
  css_extra="""h2{letter-spacing:-.01em}
.seal{font-weight:800;letter-spacing:.02em}
.org{font-family:var(--f-sans);font-size:.78rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--acc);margin-top:22px}
.evento{font-family:var(--f-title);font-weight:800;font-size:clamp(2.1rem,9vw,3rem);line-height:1.08;letter-spacing:-.02em;margin-block:12px 14px}
.chip{display:inline-block;font-family:var(--f-sans);font-size:.78rem;font-weight:600;color:var(--acc);background:var(--acc-soft);border-radius:999px;padding:6px 14px;margin-bottom:22px}
.fecha-grande{font-weight:600;letter-spacing:.18em}
.donde{margin-top:12px;color:var(--muted);font-size:.95rem}
.timeline h3{font-family:var(--f-title);font-weight:700;font-size:1.05rem}
.timeline p{font-size:.92rem}
.timeline .tag{display:inline-block;font-family:var(--f-sans);font-size:.66rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin-bottom:2px}
.oradores{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:26px}
.orador{background:var(--card);border:1px solid var(--line);border-radius:var(--r-card);padding:20px 14px;display:grid;justify-items:center;gap:6px;min-width:0}
.orador .ini{width:56px;height:56px;border-radius:50%;display:grid;place-items:center;font-weight:700;font-size:1.05rem;color:#fff;background:linear-gradient(145deg,#14967F,#16233A)}
.orador b{font-family:var(--f-title);font-weight:700;font-size:1rem;line-height:1.25}
.orador span{font-size:.82rem;color:var(--muted);line-height:1.35}
.lugar{display:grid;gap:4px;text-align:left}
.lugar b{font-family:var(--f-title);font-weight:700;font-size:1.15rem}
.lugar p{color:var(--muted);font-size:.95rem}
.lista{font-size:.98rem}
.libre{font-family:var(--f-title);font-weight:800;font-size:1.6rem;color:var(--acc);line-height:1.1}
.libre small{display:block;font-family:var(--f-sans);font-size:.8rem;font-weight:500;color:var(--muted);margin-top:6px}
footer .evento{font-size:1.4rem;margin:6px 0 0}
@media (max-width:360px){.oradores{grid-template-columns:1fr}}""",
  sello="JI",
  cuerpo=f"""<main>
  <section class="portada">
    <div class="wrap">
      <p class="saludo" id="saludo">Invitación para Laura Méndez</p>
      <p class="org">Cámara de Comercio de Marcos Paz presenta</p>
      <h1 class="evento">Jornada de Innovación Pyme 2027</h1>
      <span class="chip">Congreso regional · Entrada libre y gratuita</span><br>
      <p class="fecha-grande">Jue 16 · 09 · 2027</p>
      <p class="donde">Centro de Convenciones Municipal · Marcos Paz</p>
      <p class="invita">Una jornada para conocer herramientas concretas, escuchar casos reales y conectar con otras empresas de la región.</p>
    </div>
  </section>

{cuenta_regresiva("Faltan", "Cuenta regresiva")}

  <section class="banda">
    <div class="wrap">
      <span class="lab" id="diaLab">Jueves 16 de septiembre</span>
      <h2>Agenda</h2>
      <ol class="timeline">
        <li data-parte="cena"><span class="h">08:30</span><div class="t"><h3>Acreditación y café de bienvenida</h3><p>Hall central</p></div></li>
        <li data-parte="cena"><span class="h">09:15</span><div class="t"><h3>Apertura</h3><p>Palabras de la Comisión Directiva de la Cámara</p></div></li>
        <li data-parte="cena"><span class="h">09:45</span><div class="t"><span class="tag">Panel</span><h3>Financiamiento para pymes en 2027</h3><p>Créditos, garantías y programas disponibles</p></div></li>
        <li data-parte="cena"><span class="h">11:00</span><div class="t"><h3>Pausa y networking</h3><p>Café y espacio de encuentro</p></div></li>
        <li data-parte="fiesta"><span class="h">11:30</span><div class="t"><span class="tag">Taller</span><h3>Inteligencia artificial aplicada al comercio</h3><p>Casos prácticos para vender y atender mejor</p></div></li>
        <li data-parte="fiesta"><span class="h">14:00</span><div class="t"><span class="tag">Rondas</span><h3>Rondas de negocios</h3><p>Encuentros de 15 minutos entre empresas</p></div></li>
        <li data-parte="fiesta"><span class="h">17:00</span><div class="t"><h3>Cierre y entrega de certificados</h3><p>Auditorio principal</p></div></li>
      </ol>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="lab">Disertantes</span>
      <h2>Quiénes exponen</h2>
      <div class="oradores">
        <div class="orador"><span class="ini">MS</span><b>Mariana Sosa</b><span>Economista, especialista en financiamiento pyme</span></div>
        <div class="orador"><span class="ini">DR</span><b>Diego Ramírez</b><span>Consultor en transformación digital</span></div>
        <div class="orador"><span class="ini">CL</span><b>Carla Luna</b><span>Fundadora de una red de comercios de la zona</span></div>
        <div class="orador"><span class="ini">JP</span><b>Javier Paz</b><span>Coordinador de rondas de negocios</span></div>
      </div>
    </div>
  </section>

  <section class="banda">
    <div class="wrap">
      <span class="lab">Lugar</span>
      <h2>Cómo llegar</h2>
      <div class="card lugar">
        <b>Centro de Convenciones Municipal</b>
        <p>Av. Principal 1200 · Marcos Paz, Buenos Aires</p>
        <a target="_blank" rel="noopener" href="{mapa('Marcos Paz, Buenos Aires')}">Ver en el mapa</a>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="lab">Información útil</span>
      <h2>Antes de venir</h2>
      <div class="card">
        <p class="libre">Sin costo<small>Cupos limitados: confirme su asistencia para reservar su lugar</small></p>
        <ul class="lista">
          <li>Se entregan certificados de asistencia.</li>
          <li>Traiga su DNI para la acreditación.</li>
          <li>Estacionamiento sin cargo y acceso para personas con movilidad reducida.</li>
          <li>Wi-Fi disponible durante toda la jornada.</li>
        </ul>
      </div>
    </div>
  </section>

{confirmacion("Inscripción hasta el 9 de septiembre", "Confirme su asistencia", "Reservamos 1 lugar para Laura Méndez.",
  "Asistiré", "No podré asistir",
  '''          <div class="campo" data-si>
            <label for="empresa">Empresa u organización</label>
            <input type="text" id="empresa" data-extra="Empresa" maxlength="80" autocomplete="organization">
          </div>
          <div class="campo" data-si>
            <label for="cargo">Cargo</label>
            <input type="text" id="cargo" data-extra="Cargo" maxlength="60" autocomplete="organization-title">
          </div>
''', "Consultas o comentarios", "Actividad sin costo. Cupos limitados.", menu=False)}
</main>

<footer>
  <p class="lab">Lo esperamos</p>
  <p class="evento">Jornada de Innovación Pyme 2027</p>
</footer>""",
  ribbon="Modelo Agenda · para jornadas, congresos y reuniones de empresa · datos de ejemplo",
  inv=inv(invitado="Laura Méndez", lugares=1, fechaEvento="2027-09-16T08:30:00-03:00", fechaFin="2027-09-16T17:30:00-03:00",
          titulo="Jornada de Innovación Pyme 2027", lugarAgenda="Centro de Convenciones Municipal, Marcos Paz, Buenos Aires", horaFiesta="11:30"),
  txt=txt(saludo="Invitación para", saludoGenerico="Invitación", reservamos="Reservamos", desdeLas="Lo esperamos desde las",
          yaConfirmaste="Ya confirmó", yaNoVienen="Nos avisó que no podrá asistir.", siCambio="Si algo cambia, puede modificar su respuesta.",
          elegi="Indique si asistirá para poder enviar.", usaLink="Para inscribirse, use el link personal que recibió.",
          confirmaste="Confirmó", nota="le llega a la organización", graciasSi="¡Inscripción confirmada!",
          graciasNo="Gracias por avisarnos", graciasNoP="Esperamos contar con su presencia en una próxima edición.",
          porWhatsapp="Complete sus datos y su inscripción nos llega por WhatsApp.", faltaNombre="Escriba su nombre y apellido para saber quién se inscribe.",
          abrioWhatsapp="Se abrió WhatsApp con su inscripción. Toque Enviar para que nos llegue."),
  extra_js=r"""/* Si la invitación es para una sola persona, no tiene sentido preguntar cuántas van */
(function(){
  const campo = $("#campoCant"), sel = $("#cant");
  const ver = () => { campo.hidden = sel.options.length < 2 || $("#asisteNo").checked; };
  new MutationObserver(ver).observe(sel, { childList:true });
  document.querySelectorAll('input[name="asiste"]').forEach(r => r.addEventListener("change", ver));
  ver();
})();""",
  musica='{ onda:"sine", notas:[523.25,659.25,783.99,659.25,587.33,739.99,880,739.99], paso:900, volumen:0.03, cola:1.6 }',
  deco=r"""(function(){
  const c = $("#deco"), x = c.getContext("2d");
  function dibujar(){
    const dpr = window.devicePixelRatio || 1, W = innerWidth, H = innerHeight;
    c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    x.clearRect(0, 0, W, H);
    x.fillStyle = "rgba(22,35,58,.07)";
    for(let px = 12; px < W; px += 24) for(let py = 12; py < H; py += 24){ x.beginPath(); x.arc(px, py, 1, 0, 6.28); x.fill(); }
    x.strokeStyle = "rgba(15,123,108,.16)"; x.lineWidth = 2;
    for(let i = 0; i < 4; i++){ x.beginPath(); x.moveTo(W - 160 + i * 22, -10); x.lineTo(W + 40 + i * 22, 190); x.stroke(); }
    for(let i = 0; i < 3; i++){ x.beginPath(); x.moveTo(-40 + i * 22, H - 150); x.lineTo(120 + i * 22, H + 10); x.stroke(); }
  }
  dibujar(); addEventListener("resize", dibujar);
})();""")

# ---------------------------------------------------------------- MAGIA (temática: fiesta de magia, diseño original)
SOMBRERO = """<svg class="sombrero" viewBox="0 0 160 150" aria-hidden="true">
  <defs><linearGradient id="gS" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5B3FA8"/><stop offset="1" stop-color="#2A1A5E"/></linearGradient></defs>
  <path d="M84 6 C70 40 58 78 48 112 L118 112 C112 86 104 62 100 44 C108 40 118 42 126 50 C118 30 102 20 84 6 Z" fill="url(#gS)"/>
  <path d="M52 100 L114 100 L118 112 L48 112 Z" fill="#E7B84B"/>
  <ellipse cx="82" cy="118" rx="70" ry="14" fill="#3A2580"/>
  <path d="M74 60 l3.5 7.5 8 .9-6 5.5 1.7 8-7.2-4.1-7.2 4.1 1.7-8-6-5.5 8-.9z" fill="#F6D57A"/>
  <circle cx="92" cy="84" r="3" fill="#F6D57A"/><circle cx="66" cy="40" r="2" fill="#F6D57A"/>
</svg>"""
MODELOS["magia"] = dict(
  titulo="Una noche de magia · Sofía cumple 8",
  fuentes="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Cinzel:wght@500;600&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap",
  css=""":root{
  --bg:#120D2B; --banda:rgba(255,255,255,.04); --card:rgba(255,255,255,.06); --card-solid:#1E1645;
  --ink:#F4ECDA; --muted:#BDB3D6; --acc:#E7B84B; --acc-ink:#1A1238; --acc-soft:rgba(231,184,75,.14); --hl:#F2CF73; --line:rgba(231,184,75,.28); --field:#1A1238; --err:#F4A8A0;
  --f-title:"Cinzel Decorative", "Cinzel", Georgia, serif; --title-w:700; --h2:2.2rem;
  --f-body:"EB Garamond", Georgia, serif; --f-sans:"Cinzel", Georgia, serif; --f-num:"Cinzel", Georgia, serif; --num-w:600;
  --r-btn:6px; --r-card:14px; --dot-r:50%; --bullet:"✦"; --fs:19px;
  --sobre-bg:radial-gradient(ellipse at 50% 20%,#2C1F66,#0B0820 70%);
  --env-back:#C9B48A; --env-front:#E9DCB8; --env-flap:#D8C79D; --env-ink:#3B2A12;
  --seal-bg:radial-gradient(circle at 35% 30%,#8E6CE0 0,#4B2C9C 60%,#2E1A66 100%); --seal-ink:#F6D57A; --seal-font:"Cinzel Decorative", serif; --seal-fs:2.2rem;
  --tap:#F2CF73; --ribbon-bg:#E7B84B; --ribbon-ink:#1A1238;
  color-scheme:dark;
}""",
  css_extra="""h2{letter-spacing:.02em}
.sombrero{display:block;width:150px;height:auto;margin:6px auto 0;filter:drop-shadow(0 10px 22px rgba(120,90,220,.45));animation:flotar 5s ease-in-out infinite}
@keyframes flotar{50%{transform:translateY(-8px) rotate(-2deg)}}
@media (prefers-reduced-motion: reduce){.sombrero{animation:none}}
.anuncio{font-family:var(--f-sans);font-size:.85rem;letter-spacing:.32em;text-transform:uppercase;color:var(--hl);margin-top:14px}
.nombre{font-family:var(--f-title);font-weight:700;font-size:clamp(3.4rem,16vw,5.2rem);line-height:1.02;margin-block:8px 6px;background:linear-gradient(180deg,#FFF1C2,#E7B84B 60%,#B9862E);-webkit-background-clip:text;background-clip:text;color:transparent}
.edad{font-family:var(--f-sans);font-size:1.25rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:18px}
.edad b{color:var(--hl);font-size:1.6rem}
.fecha-grande{color:var(--ink)}
.cd div{background:rgba(255,255,255,.05)}
.timeline h3{font-family:var(--f-sans);font-weight:600;font-size:1.1rem;letter-spacing:.03em}
.lugar{display:grid;gap:4px}
.lugar h3{font-family:var(--f-sans);font-weight:600;font-size:1.3rem}
.lugar .hora{font-family:var(--f-title);font-size:1.7rem;color:var(--hl)}
.pergamino{background:linear-gradient(180deg,#F1E6C8,#E3D3A8);color:#3B2A12;border:0;box-shadow:0 18px 40px -20px rgba(0,0,0,.7)}
.pergamino .lista li::before{color:#7A4FC9}
footer .nombre{font-size:3rem;margin:4px 0 0}""",
  sello="S",
  cuerpo=f"""<main>
  <section class="portada">
    <div class="wrap">
      <p class="saludo" id="saludo">Querida Familia Gómez</p>
      {SOMBRERO}
      <p class="anuncio">Están invitados a una noche de magia</p>
      <h1 class="nombre">Sofía</h1>
      <p class="edad">cumple <b>8</b> años</p>
      <p class="fecha-grande">Sáb 15 · 05 · 2027</p>
      <p class="invita">Preparen la varita y el sombrero: habrá pociones de colores, trucos imposibles y una torta encantada.</p>
    </div>
  </section>

{cuenta_regresiva("Falta poco para el hechizo", "Cuenta regresiva")}

  <section class="banda">
    <div class="wrap">
      <span class="lab" id="diaLab">Sábado 15 de mayo</span>
      <h2>El programa mágico</h2>
      <ol class="timeline">
        <li data-parte="cena"><span class="h">17:00</span><div class="t"><h3>Llegada de los magos</h3><p>Cada invitado recibe su varita</p></div></li>
        <li data-parte="cena"><span class="h">17:30</span><div class="t"><h3>Taller de pociones</h3><p>Jugos que cambian de color</p></div></li>
        <li data-parte="fiesta"><span class="h">18:15</span><div class="t"><h3>Show de magia</h3><p>Con un mago de verdad</p></div></li>
        <li data-parte="fiesta"><span class="h">19:00</span><div class="t"><h3>La torta encantada</h3><p>¡Y a soplar las velitas!</p></div></li>
      </ol>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="lab">Dónde</span>
      <h2>El salón de los hechizos</h2>
      <div class="card lugar">
        <span class="hora">17 a 20 h</span>
        <h3>Salón Luna Llena</h3>
        <p class="sub">Calle Mitre 456 · Marcos Paz</p>
        <a target="_blank" rel="noopener" href="{mapa('Marcos Paz, Buenos Aires')}">Cómo llegar</a>
      </div>
    </div>
  </section>

  <section class="banda">
    <div class="wrap">
      <span class="lab">Vestimenta</span>
      <h2>Vengan disfrazados</h2>
      <div class="card pergamino">
        <ul class="lista">
          <li>Capa, sombrero puntiagudo o túnica de mago.</li>
          <li>Si tenés varita, ¡traela!</li>
          <li>Premio al disfraz más mágico.</li>
        </ul>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="lab">Regalos</span>
      <h2>Si querés regalarme algo</h2>
      <p class="sub">Me encantan los libros de aventuras y los juegos de ciencia. También podés colaborar con este alias.</p>
      <div class="card">
        <div class="datos">
          <div class="dato"><span>Titular</span><b>Laura Pérez (mamá)</b></div>
          {dato_copia("Alias", "alias", "sofia.cumple8")}
        </div>
        <p class="err" id="copyMsg" role="status"></p>
      </div>
    </div>
  </section>

{confirmacion("Confirmá antes del 8 de mayo", "¿Venís a la fiesta?", "Reservamos 3 lugares para Familia Gómez.",
  "¡Ahí estaremos!", "No podemos",
  '', "Un mensaje para Sofía", "Los adultos que acompañan también cuentan como lugar.",
  menu_opciones=["Ninguno", "Sin TACC (celíaco)", "Vegetariano", "Alergia (la aclaramos en el mensaje)"])}
</main>

<footer>
  <p class="lab">Los espero</p>
  <p class="nombre">Sofía</p>
</footer>""",
  ribbon="Temática Magia · invitación de muestra con datos de ejemplo",
  inv=inv(fechaEvento="2027-05-15T17:00:00-03:00", fechaFin="2027-05-15T20:00:00-03:00",
          titulo="Cumple de Sofía · Una noche de magia", lugarAgenda="Salón Luna Llena, Marcos Paz, Buenos Aires", horaFiesta="18:15"),
  txt=txt(saludo="Querida", saludoGenerico="Querido mago", nota="les llega a los papás de Sofía",
          graciasSi="¡Que empiece la magia!", graciasNo="¡Te vamos a extrañar!", graciasNoP="Gracias por avisar. ¡Otra vez será!"),
  musica='{ onda:"sine", notas:[587.33,698.46,880,1174.66,1046.5,880,698.46,783.99,932.33,1174.66,1396.91,1174.66,932.33,880,698.46,587.33], paso:300, volumen:0.04, cola:1.4 }',
  deco=r"""(function(){
  const c = $("#deco"), x = c.getContext("2d");
  let W, H, estrellas = [], chispas = [];
  function armar(){
    const dpr = window.devicePixelRatio || 1; W = innerWidth; H = innerHeight;
    c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    estrellas = Array.from({length: Math.round(W * H / 5000)}, () => ({ x: Math.random() * W, y: Math.random() * H, r: .4 + Math.random() * 1.3, f: Math.random() * 6.28, v: .5 + Math.random() * 1.5 }));
  }
  function chispa(px, py, n){
    for(let i = 0; i < n; i++){ const a = Math.random() * 6.28, s = .6 + Math.random() * 2.4;
      chispas.push({ x: px, y: py, vx: Math.cos(a) * s, vy: Math.sin(a) * s - 1, vida: 1, r: 1 + Math.random() * 2, c: Math.random() > .5 ? "242,207,115" : "180,150,255" }); }
  }
  addEventListener("pointerdown", e => { if(!reduce) chispa(e.clientX, e.clientY, 22); });
  function luna(){
    const r = Math.min(W, H) * .07, cx = W - r * 1.8, cy = r * 1.9;
    const g = x.createRadialGradient(cx, cy, r * .2, cx, cy, r * 3); g.addColorStop(0, "rgba(246,213,122,.18)"); g.addColorStop(1, "rgba(246,213,122,0)");
    x.fillStyle = g; x.beginPath(); x.arc(cx, cy, r * 3, 0, 6.28); x.fill();
    x.fillStyle = "#F6E3A6"; x.beginPath(); x.arc(cx, cy, r, 0, 6.28); x.fill();
    x.globalCompositeOperation = "destination-out"; x.beginPath(); x.arc(cx + r * .45, cy - r * .2, r * .9, 0, 6.28); x.fill(); x.globalCompositeOperation = "source-over";
  }
  function dibujar(t){
    t = t || 0;
    const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#0B0820"); g.addColorStop(.6, "#1B1342"); g.addColorStop(1, "#2A1A5E");
    x.fillStyle = g; x.fillRect(0, 0, W, H);
    for(const e of estrellas){ x.globalAlpha = .35 + .65 * Math.abs(Math.sin(e.f + t / 1000 * e.v)); x.fillStyle = "#FFF6DA"; x.beginPath(); x.arc(e.x, e.y, e.r, 0, 6.28); x.fill(); }
    x.globalAlpha = 1; luna();
    if(!reduce && Math.random() < .25) chispas.push({ x: Math.random() * W, y: H + 5, vx: (Math.random() - .5) * .3, vy: -(.4 + Math.random() * .8), vida: 1, r: .8 + Math.random() * 1.6, c: "242,207,115", lenta: true });
    chispas = chispas.filter(p => p.vida > 0);
    for(const p of chispas){ p.x += p.vx; p.y += p.vy; if(!p.lenta) p.vy += .03; p.vida -= p.lenta ? .003 : .02;
      x.fillStyle = "rgba(" + p.c + "," + Math.max(0, p.vida) + ")"; x.beginPath(); x.arc(p.x, p.y, p.r, 0, 6.28); x.fill(); }
    if(!reduce) requestAnimationFrame(dibujar);
  }
  armar(); addEventListener("resize", () => { armar(); if(reduce) dibujar(); }); dibujar();
})();""")

CAMPO_VOTO = """          <div class="campo" data-si>
            <span class="votoForm" id="votoForm">Todavía no votaste: hacelo arriba, en "¿Vos qué decís?"</span>
            <input type="hidden" id="votoTxt" data-extra="Voto">
          </div>
"""

# ---------------------------------------------------------------- REVELACIÓN (gender reveal, con votación)
MODELOS["revelacion"] = dict(
  titulo="¿Nena o nene? · Revelación de Lucía y Martín",
  fuentes="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Quicksand:wght@400;500;600;700&display=swap",
  css=""":root{
  --bg:#FFF9F4; --banda:#FFF1F5; --card:#FFFFFF; --card-solid:#FFFFFF; --ink:#3B3350; --muted:#7D7590;
  --rosa:#F28DB2; --rosa-f:#D9568A; --celeste:#7CB7EC; --celeste-f:#3E86C9;
  --acc:#8C6BD9; --acc-ink:#FFFFFF; --acc-soft:#F1ECFF; --hl:#8C6BD9; --line:#EADFEF; --field:#FFFDFB;
  --f-title:"Fredoka", "Arial Rounded MT Bold", sans-serif; --title-w:700; --h2:2.4rem;
  --f-body:"Quicksand", "Segoe UI", sans-serif; --f-sans:"Quicksand", "Segoe UI", sans-serif; --f-num:"Fredoka", sans-serif; --num-w:600;
  --sub-style:normal; --r-btn:999px; --r-card:24px; --bullet:"♥"; --fs:18px;
  --sobre-bg:linear-gradient(90deg,#FFE3EE 50%,#E2F0FD 50%);
  --env-back:#E9DDF7; --env-front:#F6F0FD; --env-flap:#E2D3F5; --env-ink:#3B3350;
  --seal-bg:linear-gradient(90deg,#F28DB2 50%,#7CB7EC 50%); --seal-ink:#FFFFFF; --seal-font:"Fredoka", sans-serif; --seal-fs:2.8rem;
  --tap:#8C6BD9; --ribbon-bg:#3B3350; --ribbon-ink:#FFF9F4;
  color-scheme:light;
}""",
  css_extra=""".invitan{font-family:var(--f-sans);font-weight:600;font-size:1rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-top:46px}
.padres{font-family:var(--f-title);font-weight:600;font-size:clamp(2rem,9vw,2.8rem);line-height:1.1;margin-top:6px}
.pregunta{font-family:var(--f-title);font-weight:700;font-size:clamp(3.2rem,16vw,5.2rem);line-height:.98;margin-block:18px 14px;letter-spacing:-.01em}
.pregunta .n{display:block}
.pregunta .n{color:var(--rosa-f)} .pregunta .o{color:var(--muted);font-size:.55em;vertical-align:middle;margin-inline:.12em} .pregunta .m{color:var(--celeste-f)}
.globos{display:flex;justify-content:center;gap:14px;margin-top:30px}
.globos i{display:block;width:46px;height:56px;border-radius:50% 50% 48% 48%;position:relative;animation:subir 3.2s ease-in-out infinite}
.globos i::after{content:"";position:absolute;left:50%;top:100%;width:1px;height:34px;background:#C9BFD6}
.globos i:nth-child(1){background:var(--rosa)} .globos i:nth-child(2){background:#C9B5F2;animation-delay:.6s;margin-top:-10px} .globos i:nth-child(3){background:var(--celeste);animation-delay:1.2s}
@keyframes subir{50%{transform:translateY(-10px) rotate(3deg)}}
@media (prefers-reduced-motion: reduce){.globos i{animation:none}}
.timeline h3{font-family:var(--f-title);font-weight:600}
.timeline li.grande h3{font-size:1.35rem;background:linear-gradient(90deg,var(--rosa-f),var(--celeste-f));-webkit-background-clip:text;background-clip:text;color:transparent}
.lugar{display:grid;gap:4px} .lugar h3{font-family:var(--f-title);font-weight:600;font-size:1.4rem} .lugar .hora{font-family:var(--f-title);font-weight:700;font-size:1.8rem;color:var(--acc)}
.votar{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:22px}
.voto{border:0;border-radius:22px;padding:22px 10px 18px;cursor:pointer;font-family:var(--f-title);font-weight:700;font-size:1.6rem;color:#fff;display:grid;gap:6px;justify-items:center;transition:transform .2s, box-shadow .2s, opacity .2s;box-shadow:0 10px 0 -2px rgba(0,0,0,.08)}
.voto small{font-family:var(--f-sans);font-weight:600;font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;opacity:.9}
.voto.nena{background:linear-gradient(160deg,#F7A8C6,var(--rosa-f))} .voto.nene{background:linear-gradient(160deg,#9FCBF2,var(--celeste-f))}
.voto:active{transform:scale(.97)}
.votar.elegido .voto{opacity:.45} .votar.elegido .voto.si{opacity:1;transform:scale(1.04);box-shadow:0 0 0 4px #fff,0 0 0 7px var(--acc)}
.miVoto{margin-top:16px;font-family:var(--f-title);font-weight:600;font-size:1.2rem;min-height:1.5em}
.estallido{position:fixed;inset:0;pointer-events:none;z-index:70;overflow:hidden}
.estallido i{position:absolute;width:10px;height:14px;border-radius:3px;animation:caer 1.6s ease-out forwards}
@keyframes caer{to{transform:translate(var(--dx),var(--dy)) rotate(540deg);opacity:0}}
.votoForm{font-family:var(--f-title);font-weight:600;color:var(--acc)}
footer .padres{font-size:2rem}""",
  sello="?",
  cuerpo=f"""<main>
  <section class="portada">
    <div class="wrap">
      <p class="saludo" id="saludo">Querida Familia Gómez</p>
      <div class="globos" aria-hidden="true"><i></i><i></i><i></i></div>
      <p class="invitan">Te invitan a descubrir</p>
      <h1 class="pregunta"><span class="n">¿Nena</span><span class="o">o</span><span class="m">nene?</span></h1>
      <p class="padres">Lucía y Martín</p>
      <p class="fecha-grande" style="margin-top:16px">Dom 20 · 06 · 2027</p>
      <p class="invita">Queremos que estés con nosotros en el momento en que se revela el gran secreto.</p>
    </div>
  </section>

{cuenta_regresiva("Falta poco para saberlo", "Cuenta regresiva")}

  <section class="banda" id="votacion">
    <div class="wrap">
      <span class="lab">La gran apuesta</span>
      <h2>¿Vos qué decís?</h2>
      <p class="sub">Votá ahora. En la fiesta se revela quién acertó.</p>
      <div class="votar" id="votar">
        <button class="voto nena" type="button" data-voto="Nena">Nena<small>Team rosa</small></button>
        <button class="voto nene" type="button" data-voto="Nene">Nene<small>Team celeste</small></button>
      </div>
      <p class="miVoto" id="miVoto" role="status"></p>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="lab" id="diaLab">Domingo 20 de junio</span>
      <h2>Cómo será la tarde</h2>
      <ol class="timeline">
        <li data-parte="cena"><span class="h">16:00</span><div class="t"><h3>Llegada y merienda</h3><p>Mesa dulce para todos</p></div></li>
        <li data-parte="cena"><span class="h">16:45</span><div class="t"><h3>Juegos y adivinanzas</h3><p>¿Quién conoce mejor a los futuros papás?</p></div></li>
        <li data-parte="fiesta" class="grande"><span class="h">17:30</span><div class="t"><h3>¡La gran revelación!</h3><p>Globos, humo de colores y la respuesta</p></div></li>
        <li data-parte="fiesta"><span class="h">18:00</span><div class="t"><h3>Brindis</h3><p>Por la familia que crece</p></div></li>
      </ol>
    </div>
  </section>

  <section class="banda">
    <div class="wrap">
      <span class="lab">Dónde</span>
      <h2>Te esperamos en casa</h2>
      <div class="card lugar">
        <span class="hora">16 a 19 h</span>
        <h3>Casa de Lucía y Martín</h3>
        <p class="sub">Los Aromos 789 · Marcos Paz</p>
        <a target="_blank" rel="noopener" href="{mapa('Marcos Paz, Buenos Aires')}">Cómo llegar</a>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="lab">Regalos</span>
      <h2>Si querés regalarle algo al bebé</h2>
      <p class="sub">Pañales (talle 1 y 2) siempre suman. Si preferís, también podés colaborar con este alias.</p>
      <div class="card">
        <div class="datos">
          <div class="dato"><span>Titular</span><b>Lucía Fernández</b></div>
          {dato_copia("Alias", "alias", "bebe.lucia.martin")}
        </div>
        <p class="err" id="copyMsg" role="status"></p>
      </div>
    </div>
  </section>

{confirmacion("Confirmá antes del 13 de junio", "¿Venís?", "Reservamos 3 lugares para Familia Gómez.",
  "¡Ahí estaremos!", "No podemos",
  CAMPO_VOTO, "Un mensaje para los futuros papás", "Los chicos también cuentan como lugar.", menu=False)}
</main>

<footer>
  <p class="lab">Te esperamos</p>
  <p class="padres">Lucía y Martín</p>
</footer>""",
  ribbon="Modelo Revelación · invitación de muestra con datos de ejemplo",
  inv=inv(fechaEvento="2027-06-20T16:00:00-03:00", fechaFin="2027-06-20T19:00:00-03:00",
          titulo="Revelación de Lucía y Martín", lugarAgenda="Marcos Paz, Buenos Aires", horaFiesta="17:30"),
  txt=txt(nota="les llega a Lucía y Martín", graciasSi="¡Nos vemos ahí!", graciasNo="¡Te vamos a extrañar!", graciasNoP="Gracias por avisar. ¡Te contamos la respuesta!"),
  musica='{ onda:"triangle", notas:[783.99,987.77,1174.66,987.77,880,1046.5,1318.51,1046.5,783.99,987.77,1174.66,1567.98,1318.51,1174.66,987.77,880], paso:380, volumen:0.035, cola:1.1 }',
  extra_js=r"""/* Votación: nena o nene. El voto viaja con la confirmación y se ve en el panel */
(function(){
  const caja = $("#votar"), txt = $("#votoTxt"), msg = $("#miVoto"), enForm = $("#votoForm");
  let guardado = ""; try{ guardado = localStorage.getItem("evocard-voto") || ""; }catch(e){}
  function marcar(v, festejo){
    caja.classList.add("elegido");
    caja.querySelectorAll(".voto").forEach(b => b.classList.toggle("si", b.dataset.voto === v));
    txt.value = v;
    msg.textContent = "Votaste: Team " + (v === "Nena" ? "rosa" : "celeste") + ". Podés cambiarlo cuando quieras.";
    msg.style.color = v === "Nena" ? "var(--rosa-f)" : "var(--celeste-f)";
    enForm.textContent = "Tu voto: " + v + " (va junto con tu confirmación)";
    try{ localStorage.setItem("evocard-voto", v); }catch(e){}
    if(festejo && !reduce){
      const capa = document.createElement("div"); capa.className = "estallido";
      const cols = v === "Nena" ? ["#F28DB2","#D9568A","#FFD1E1","#FFFFFF"] : ["#7CB7EC","#3E86C9","#D4E9FB","#FFFFFF"];
      const r = caja.getBoundingClientRect();
      for(let i = 0; i < 46; i++){
        const p = document.createElement("i"); const a = Math.random() * 6.28, d = 120 + Math.random() * 220;
        p.style.left = (r.left + r.width / 2) + "px"; p.style.top = (r.top + r.height / 2) + "px";
        p.style.background = cols[i % cols.length];
        p.style.setProperty("--dx", Math.cos(a) * d + "px"); p.style.setProperty("--dy", Math.sin(a) * d + 160 + "px");
        capa.appendChild(p);
      }
      document.body.appendChild(capa); setTimeout(() => capa.remove(), 1800);
    }
  }
  caja.addEventListener("click", e => { const b = e.target.closest(".voto"); if(b) marcar(b.dataset.voto, true); });
  if(guardado) marcar(guardado, false);
})();""",
  deco=r"""(function(){
  const c = $("#deco"), x = c.getContext("2d");
  const cols = ["rgba(242,141,178,", "rgba(124,183,236,", "rgba(201,181,242,"];
  let W, H, globos = [];
  function armar(){
    const dpr = window.devicePixelRatio || 1; W = innerWidth; H = innerHeight;
    c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    globos = Array.from({length: Math.max(6, Math.round(W / 70))}, () => nuevo(Math.random() * H));
  }
  function nuevo(y){ return { x: Math.random() * W, y: y, r: 14 + Math.random() * 16, v: .25 + Math.random() * .45, f: Math.random() * 6.28, c: cols[Math.floor(Math.random() * 3)] }; }
  function dibujar(t){
    t = t || 0; x.clearRect(0, 0, W, H);
    for(const g of globos){
      if(!reduce){ g.y -= g.v; if(g.y < -g.r * 4) Object.assign(g, nuevo(H + g.r * 2)); }
      const gx = g.x + Math.sin(g.f + t / 1400) * 10;
      x.strokeStyle = "rgba(160,150,180,.35)"; x.lineWidth = 1; x.beginPath(); x.moveTo(gx, g.y + g.r * 1.15); x.quadraticCurveTo(gx + 6, g.y + g.r * 2, gx, g.y + g.r * 2.8); x.stroke();
      x.fillStyle = g.c + ".35)"; x.beginPath(); x.ellipse(gx, g.y, g.r * .86, g.r * 1.1, 0, 0, 6.28); x.fill();
      x.fillStyle = "rgba(255,255,255,.45)"; x.beginPath(); x.ellipse(gx - g.r * .3, g.y - g.r * .4, g.r * .18, g.r * .28, -.5, 0, 6.28); x.fill();
    }
    if(!reduce) requestAnimationFrame(dibujar);
  }
  armar(); addEventListener("resize", () => { armar(); if(reduce) dibujar(); }); dibujar();
})();""")

# ---------------------------------------------------------------- BRINDIS (fin de año de empresas)
CAMPO_SECTOR = """          <div class="campo" data-si>
            <label for="sector">Área o sector</label>
            <input type="text" id="sector" data-extra="Sector" maxlength="60" placeholder="Ej: Ventas, Depósito, Administración" autocomplete="off">
          </div>
"""
MODELOS["brindis"] = dict(
  titulo="Fiesta de fin de año 2026 · Tu empresa",
  fuentes="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Montserrat:wght@400;500;600&display=swap",
  css=""":root{
  --bg:#0C1120; --banda:rgba(255,255,255,.035); --card:rgba(255,255,255,.05); --card-solid:#161D33;
  --ink:#F5EFE2; --muted:#B5B0A4; --acc:#E3C27A; --acc-ink:#141414; --acc-soft:rgba(227,194,122,.14); --hl:#E3C27A; --line:rgba(227,194,122,.26); --field:#121933; --err:#F4A8A0;
  --f-title:"Playfair Display", Georgia, serif; --title-w:700; --h2:2.3rem;
  --f-body:"Montserrat", "Segoe UI", sans-serif; --f-sans:"Montserrat", "Segoe UI", sans-serif; --f-num:"Playfair Display", Georgia, serif; --num-w:700;
  --sub-style:normal; --r-btn:999px; --r-card:16px; --bullet:"✦"; --fs:17px;
  --sobre-bg:radial-gradient(ellipse at 50% 10%,#23305A,#080B16 70%);
  --env-back:#1A2340; --env-front:#222D52; --env-flap:#2B3866; --env-ink:#F5EFE2;
  --seal-bg:radial-gradient(circle at 35% 30%,#FBE7B0 0,#E3C27A 50%,#A9843B 100%); --seal-ink:#141414; --seal-font:"Playfair Display", serif; --seal-fs:1.9rem;
  --tap:#E3C27A; --ribbon-bg:#E3C27A; --ribbon-ink:#141414;
  color-scheme:dark;
}""",
  css_extra=""".empresa{font-family:var(--f-sans);font-weight:600;font-size:.85rem;letter-spacing:.3em;text-transform:uppercase;color:var(--hl);margin-top:20px}
.tulogo{width:118px;height:118px;margin:18px auto 0;border-radius:50%;border:2px dashed var(--acc);display:grid;place-items:center;background:var(--acc-soft)}
.tulogo span{font-family:var(--f-sans);font-weight:600;font-size:.82rem;letter-spacing:.2em;text-transform:uppercase;color:var(--hl)}
.tonos{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(52px + env(safe-area-inset-bottom,0px));z-index:44;display:flex;gap:8px;align-items:center;background:rgba(10,14,28,.82);border:1px solid var(--line);border-radius:999px;padding:7px 12px;font-family:var(--f-sans);font-size:.72rem;color:var(--muted);backdrop-filter:blur(6px)}
.tonos span{white-space:nowrap}
.tonos button{width:24px;height:24px;border-radius:50%;border:2px solid transparent;cursor:pointer;padding:0}
.tonos button[aria-pressed=true]{border-color:#fff}
.titulo{font-family:var(--f-title);font-weight:700;font-size:clamp(2.6rem,12vw,4rem);line-height:1.05;margin-block:10px 6px}
.titulo em{font-style:italic;font-weight:600;color:var(--hl)}
.anio{font-family:var(--f-title);font-weight:700;font-size:clamp(4.4rem,24vw,7rem);line-height:.9;letter-spacing:.02em;background:linear-gradient(180deg,#FFF3CF,#E3C27A 55%,#A9843B);-webkit-background-clip:text;background-clip:text;color:transparent;margin-bottom:18px}
.timeline h3{font-family:var(--f-sans);font-weight:600;font-size:1.02rem}
.timeline p{font-size:.92rem}
.lugar{display:grid;gap:4px} .lugar h3{font-family:var(--f-title);font-weight:700;font-size:1.5rem} .lugar .hora{font-family:var(--f-sans);font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--hl)}
.datos-utiles{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:22px;text-align:left}
.datos-utiles div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 14px}
.datos-utiles b{display:block;font-family:var(--f-title);font-size:1.12rem;color:var(--hl);margin-bottom:4px}
.datos-utiles span{font-size:.88rem;color:var(--muted);line-height:1.45}
footer .anio{font-size:3.4rem;margin:4px 0 0}
@media (max-width:360px){.datos-utiles{grid-template-columns:1fr}}""",
  sello="<span style=\"font-size:.42em;letter-spacing:.06em;line-height:1.1;text-align:center\">TU<br>LOGO</span>",
  cuerpo=f"""<main>
  <section class="portada">
    <div class="wrap">
      <p class="saludo" id="saludo">Hola Laura Méndez</p>
      <div class="tulogo" aria-label="Acá va el logo de la empresa"><span>Tu logo</span></div>
      <p class="empresa">Tu empresa</p>
      <h1 class="titulo">Brindemos por <em>un gran año</em></h1>
      <p class="anio">2026</p>
      <p class="fecha-grande">Vie 11 · 12 · 2026</p>
      <p class="invita">Este año lo hicimos entre todos. Te esperamos para celebrarlo como se merece: con buena comida, música y todo el equipo junto.</p>
    </div>
  </section>

{cuenta_regresiva("Falta poco para el brindis", "Cuenta regresiva")}

  <section class="banda">
    <div class="wrap">
      <span class="lab" id="diaLab">Viernes 11 de diciembre</span>
      <h2>La noche</h2>
      <ol class="timeline">
        <li data-parte="cena"><span class="h">20:30</span><div class="t"><h3>Recepción</h3><p>Tragos de bienvenida y entrada</p></div></li>
        <li data-parte="cena"><span class="h">21:30</span><div class="t"><h3>Cena</h3><p>Mesas por sector</p></div></li>
        <li data-parte="cena"><span class="h">23:00</span><div class="t"><h3>Palabras de la dirección</h3><p>Lo que logramos y lo que viene</p></div></li>
        <li data-parte="fiesta"><span class="h">23:20</span><div class="t"><h3>Reconocimientos del año</h3><p>Y sorteos para todos los presentes</p></div></li>
        <li data-parte="fiesta"><span class="h">00:00</span><div class="t"><h3>Brindis y fiesta</h3><p>DJ hasta las 3</p></div></li>
      </ol>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="lab">Dónde</span>
      <h2>El lugar</h2>
      <div class="card lugar">
        <span class="hora">Desde las 20:30</span>
        <h3>Salón Los Robles</h3>
        <p class="sub">Ruta 200 km 52 · Marcos Paz</p>
        <a target="_blank" rel="noopener" href="{mapa('Marcos Paz, Buenos Aires')}">Cómo llegar</a>
      </div>
      <div class="datos-utiles">
        <div><b>Vestimenta</b><span>Elegante sport. Nada de uniforme: esta noche es para festejar.</span></div>
        <div><b>Traslado</b><span>Combi desde la planta a las 20 h y vuelta a las 3 h.</span></div>
        <div><b>Acompañante</b><span>Podés venir con una persona. Avisanos al confirmar.</span></div>
        <div><b>Sorteos</b><span>Participan todos los presentes al momento del brindis.</span></div>
      </div>
    </div>
  </section>

{confirmacion("Confirmá antes del 1 de diciembre", "¿Venís a la fiesta?", "Reservamos 2 lugares para Laura Méndez.",
  "¡Sí, voy!", "No puedo ir",
  CAMPO_SECTOR, "Un mensaje para el equipo", "Es para organizar las mesas y el menú: confirmá aunque no puedas venir.")}
</main>

<footer>
  <p class="lab">Gracias por este año</p>
  <p class="anio">2026</p>
</footer>""",
  ribbon="Modelo Brindis · fin de año de empresas · con el logo y los colores de tu marca",
  inv=inv(invitado="Laura Méndez", lugares=2, fechaEvento="2026-12-11T20:30:00-03:00", fechaFin="2026-12-12T03:00:00-03:00",
          titulo="Fiesta de fin de año · Tu empresa", lugarAgenda="Salón Los Robles, Marcos Paz, Buenos Aires", horaFiesta="00:00"),
  txt=txt(saludo="Hola", saludoGenerico="¡Hola!", nota="le llega a la organización", graciasSi="¡Nos vemos en el brindis!",
          graciasNo="¡Te vamos a extrañar!", graciasNoP="Gracias por avisarnos. ¡Felices fiestas!"),
  musica='{ onda:"triangle", notas:[659.25,783.99,987.77,1318.51,1174.66,987.77,880,987.77,659.25,783.99,1046.5,1318.51,1567.98,1318.51,1174.66,987.77], paso:260, volumen:0.035, cola:0.9 }',
  extra_js=r"""/* Solo en la muestra: probar la invitación con distintos colores de marca */
(function(){
  if(INV.planilla || INV.whatsapp) return;
  const tonos = [["Dorado","227,194,122"],["Rojo","232,76,76"],["Verde","72,196,146"],["Azul","92,168,240"],["Violeta","170,130,240"]];
  const barra = document.createElement("div"); barra.className = "tonos"; barra.innerHTML = "<span>Probá con tu color:</span>";
  tonos.forEach(([n, rgb], i) => {
    const b = document.createElement("button"); b.type = "button"; b.title = n; b.setAttribute("aria-label", "Color " + n);
    b.style.background = "rgb(" + rgb + ")"; b.setAttribute("aria-pressed", i === 0 ? "true" : "false");
    b.addEventListener("click", () => {
      const r = document.documentElement.style;
      r.setProperty("--acc", "rgb(" + rgb + ")"); r.setProperty("--hl", "rgb(" + rgb + ")");
      r.setProperty("--acc-soft", "rgba(" + rgb + ",.14)"); r.setProperty("--line", "rgba(" + rgb + ",.28)"); r.setProperty("--ribbon-bg", "rgb(" + rgb + ")");
      document.querySelectorAll(".anio").forEach(e => e.style.backgroundImage = "linear-gradient(180deg,#FFFFFF,rgb(" + rgb + ") 60%)");
      window.TONO = rgb; barra.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b ? "true" : "false"));
    });
    barra.appendChild(b);
  });
  const mostrar = () => document.body.appendChild(barra);
  $("#sobre").addEventListener("click", () => setTimeout(mostrar, 800), { once: true });
})();""",
  deco=r"""(function(){
  const c = $("#deco"), x = c.getContext("2d");
  let W, H, burbujas = [], chispas = [], prox = 0;
  function armar(){
    const dpr = window.devicePixelRatio || 1; W = innerWidth; H = innerHeight;
    c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    burbujas = Array.from({length: Math.round(W / 22)}, () => ({ x: Math.random() * W, y: Math.random() * H, r: 1 + Math.random() * 2.6, v: .3 + Math.random() * .7, f: Math.random() * 6.28 }));
  }
  function fuego(){
    const cx = W * (.15 + Math.random() * .7), cy = H * (.08 + Math.random() * .35), n = 46, col = Math.random() > .5 ? (window.TONO || "227,194,122") : "255,243,207";
    for(let i = 0; i < n; i++){ const a = i / n * 6.28, s = 1.4 + Math.random() * 1.6; chispas.push({ x: cx, y: cy, vx: Math.cos(a) * s, vy: Math.sin(a) * s, v: 1, c: col }); }
  }
  function dibujar(t){
    t = t || 0;
    x.fillStyle = "rgba(12,17,32,.32)"; x.fillRect(0, 0, W, H);
    if(!reduce && t > prox){ fuego(); prox = t + 1800 + Math.random() * 2200; }
    chispas = chispas.filter(p => p.v > 0);
    for(const p of chispas){ p.x += p.vx; p.y += p.vy; p.vy += .025; p.vx *= .985; p.v -= .012;
      x.fillStyle = "rgba(" + p.c + "," + Math.max(0, p.v) + ")"; x.beginPath(); x.arc(p.x, p.y, 1.6, 0, 6.28); x.fill(); }
    for(const b of burbujas){ if(!reduce){ b.y -= b.v; if(b.y < -5){ b.y = H + 5; b.x = Math.random() * W; } }
      x.strokeStyle = "rgba(" + (window.TONO || "227,194,122") + ",.35)"; x.lineWidth = 1; x.beginPath(); x.arc(b.x + Math.sin(b.f + t / 900) * 3, b.y, b.r, 0, 6.28); x.stroke(); }
    if(!reduce) requestAnimationFrame(dibujar);
  }
  armar(); x.fillStyle = "#0C1120"; x.fillRect(0, 0, W, H);
  addEventListener("resize", () => { armar(); x.fillStyle = "#0C1120"; x.fillRect(0, 0, W, H); if(reduce) dibujar(); }); dibujar();
})();""")

if __name__ == "__main__":
    import sys
    from base import ESQUELETO
    destino, sitio = sys.argv[1], sys.argv[2]
    from album import agregar
    for nombre, m in MODELOS.items():
        if nombre == "gala":
            html = agregar(armar(m), sub="Durante la celebración, suba aquí sus fotos. Todas van a un mismo álbum del Club.").replace("Tu nombre (opcional)", "Su nombre (opcional)")
        elif nombre == "brindis":
            html = agregar(armar(m), sub="Durante la fiesta, subí acá tus fotos. Todas van a un mismo álbum para el equipo.")
        elif nombre == "agenda":
            html = agregar(armar(m), sub="Durante la jornada, suba aquí sus fotos. Todas van a un mismo álbum del evento.").replace("Tu nombre (opcional)", "Su nombre (opcional)")
            for a, b in [("<legend>¿Vienen?</legend>", "<legend>¿Asistirá?</legend>"), ("¿Cuántos van a ir?", "¿Cuántas personas asistirán?"),
                         ("Tu nombre y apellido", "Nombre y apellido"), ("Para Familia Gómez", "Para Laura Méndez"),
                         ('<div class="campo" data-si>\n            <label for="cant">', '<div class="campo" id="campoCant">\n            <label for="cant">'),
                         ("Compartí tus fotos", "Fotos de la jornada"), ("Álbum de la fiesta", "Álbum del evento"), ("Tocá para abrir", "Toque para abrir")]:
                assert a in html, a
                html = html.replace(a, b)
        else:
            html = agregar(armar(m))
        open(f"{destino}/{nombre}.html", "w", encoding="utf8").write(html)
        open(f"{sitio}/{nombre}.html", "w", encoding="utf8").write(ESQUELETO + html + "\n</body>\n</html>\n")
        print(nombre, len(html))
