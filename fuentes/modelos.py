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

if __name__ == "__main__":
    import sys
    from base import ESQUELETO
    destino, sitio = sys.argv[1], sys.argv[2]
    from album import agregar
    for nombre, m in MODELOS.items():
        if nombre == "gala":
            html = agregar(armar(m), sub="Durante la celebración, suba aquí sus fotos. Todas van a un mismo álbum del Club.").replace("Tu nombre (opcional)", "Su nombre (opcional)")
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
