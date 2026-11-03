/** @OnlyCurrentDoc */
/**
 * EVOCARD — Programa de la planilla (Google Apps Script) · versión Reunión Federativa: con envío de mails, sin álbum
 * Un archivo por evento: guarda la lista de invitados y sus confirmaciones.
 *
 * Cómo se usa (resumen; la guía tiene el paso a paso):
 *   1. Creá una planilla nueva en Google Sheets.
 *   2. Extensiones > Apps Script. Borrá lo que hay y pegá TODO este archivo.
 *   3. Elegí la función "configurar" arriba y tocá Ejecutar (la primera vez pide permisos).
 *   4. Implementar > Nueva implementación > Aplicación web.
 *      Ejecutar como: Yo. Quién tiene acceso: Cualquier persona.
 *   5. Copiá la dirección que termina en /exec: esa va en el panel y en la invitación.
 *
 * Las respuestas siempre son JSON: { ok: true, ... } o { ok: false, error: "..." }
 */

const HOJA_INVITADOS = 'Invitados';
const HOJA_CONFIG = 'Config';
const COLUMNAS = ['codigo', 'nombre', 'identificador', 'categoria', 'lugares', 'tipo',
  'estado', 'cantidad', 'menu', 'traslado', 'mensaje', 'respondido', 'enviada', 'email'];
// estado: pendiente | confirmado | no_asiste      tipo: completo | solo_fiesta

/* ---------- Puesta en marcha (se ejecuta una sola vez) ---------- */
function configurar() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let inv = ss.getSheetByName(HOJA_INVITADOS);
  if (!inv) inv = ss.insertSheet(HOJA_INVITADOS);
  if (inv.getLastRow() === 0) {
    inv.appendRow(COLUMNAS);
    inv.setFrozenRows(1);
    inv.getRange(1, 1, 1, COLUMNAS.length).setFontWeight('bold');
  }
  let cfg = ss.getSheetByName(HOJA_CONFIG);
  if (!cfg) cfg = ss.insertSheet(HOJA_CONFIG);
  if (cfg.getLastRow() === 0) {
    cfg.appendRow(['clave', 'valor']);
    cfg.appendRow(['evento', '3ra Reunión Federativa 2026']);
    cfg.appendRow(['clave_panel', crearCodigo(8)]);
    cfg.appendRow(['fecha_limite', '2026-09-10']);
    cfg.appendRow(['link_invitacion', 'https://evocard.com.ar/reunion-federativa.html']);
    cfg.appendRow(['remitente', 'Federación de Asociaciones de Bomberos Voluntarios de la Provincia de Buenos Aires']);
    cfg.appendRow(['respuestas_abiertas', 'si']);
    cfg.setFrozenRows(1);
  }
  const hoja1 = ss.getSheetByName('Hoja 1') || ss.getSheetByName('Sheet1');
  if (hoja1 && hoja1.getLastRow() === 0 && ss.getSheets().length > 2) ss.deleteSheet(hoja1);
  crearHojaMail();
  crearHojasReunion();
  Logger.log('Listo. La clave del panel está en la hoja Config: ' + leerConfig().clave_panel);
}

/* ---------- Entrada de pedidos ---------- */
function doGet(e) { return responder((e && e.parameter) || {}); }

function doPost(e) {
  let datos = {};
  try { datos = JSON.parse(e.postData.contents || '{}'); } catch (err) { datos = {}; }
  return responder(datos);
}

function responder(p) {
  let salida;
  try {
    salida = Object.assign({ ok: true }, atender(p));
  } catch (err) {
    salida = { ok: false, error: String((err && err.message) || err) };
  }
  return ContentService.createTextOutput(JSON.stringify(salida))
    .setMimeType(ContentService.MimeType.JSON);
}

function atender(p) {
  const accion = String(p.accion || '');
  // Acciones públicas: las usa la invitación
  if (accion === 'evento') return { evento: datosPublicosEvento() };
  if (accion === 'invitado') return { invitado: publico(buscarPorCodigo(p.codigo)) };
  if (accion === 'confirmar') return { invitado: publico(confirmar(p)) };
  if (accion === 'reunion') return leerReunion();

  // Acciones del panel: necesitan la clave
  const cfg = leerConfig();
  if (!p.clave || String(p.clave) !== String(cfg.clave_panel)) throw new Error('La clave del panel no es correcta.');
  if (accion === 'lista') return { evento: datosPublicosEvento(), invitados: leerInvitados() };
  if (accion === 'guardar') return { invitado: guardar(p.invitado || {}) };
  if (accion === 'borrar') { borrar(p.codigo); return {}; }
  if (accion === 'importar') return { agregados: importar(p.invitados || []) };
  if (accion === 'enviada') { marcar(p.codigo, { enviada: 'si' }); return {}; }
  throw new Error('Acción desconocida: ' + accion);
}

/* ---------- Lógica ---------- */
function leerConfig() {
  const hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_CONFIG);
  const cfg = {};
  if (!hoja) return cfg;
  hoja.getDataRange().getValues().slice(1).forEach(function (r) { if (r[0]) cfg[String(r[0])] = r[1]; });
  return cfg;
}

function datosPublicosEvento() {
  const c = leerConfig();
  return {
    nombre: c.evento || '',
    fecha_limite: formatoFecha(c.fecha_limite),
    respuestas_abiertas: String(c.respuestas_abiertas || 'si').toLowerCase() !== 'no'
  };
}

function hojaInvitados() {
  const h = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_INVITADOS);
  if (!h) throw new Error('Falta la hoja Invitados. Ejecutá la función configurar.');
  return h;
}

function leerInvitados() {
  const valores = hojaInvitados().getDataRange().getValues();
  const cab = valores[0];
  return valores.slice(1).filter(function (r) { return r[0]; }).map(function (r) {
    const o = {};
    cab.forEach(function (c, i) { o[c] = r[i] instanceof Date ? r[i].toISOString() : r[i]; });
    o.lugares = Number(o.lugares) || 1;
    o.cantidad = Number(o.cantidad) || 0;
    o.estado = o.estado || 'pendiente';
    return o;
  });
}

function filaDe(codigo) {
  const cod = String(codigo || '').trim().toUpperCase();
  if (!cod) return -1;
  const col = hojaInvitados().getRange(1, 1, Math.max(1, hojaInvitados().getLastRow()), 1).getValues();
  for (let i = 1; i < col.length; i++) if (String(col[i][0]).toUpperCase() === cod) return i + 1;
  return -1;
}

function buscarPorCodigo(codigo) {
  const fila = filaDe(codigo);
  if (fila < 0) throw new Error('No encontramos esta invitación. Revisá el link.');
  const cab = COLUMNAS;
  const r = hojaInvitados().getRange(fila, 1, 1, cab.length).getValues()[0];
  const o = {};
  cab.forEach(function (c, i) { o[c] = r[i]; });
  o.lugares = Number(o.lugares) || 1;
  o.cantidad = Number(o.cantidad) || 0;
  o.estado = o.estado || 'pendiente';
  return o;
}

function publico(inv) {
  return { codigo: inv.codigo, nombre: inv.nombre, lugares: inv.lugares, tipo: inv.tipo || 'completo',
    estado: inv.estado, cantidad: inv.cantidad, menu: inv.menu, traslado: inv.traslado };
}

function confirmar(p) {
  const ev = datosPublicosEvento();
  if (!ev.respuestas_abiertas) throw new Error('Las confirmaciones ya están cerradas. Escribiles a los anfitriones.');
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const inv = buscarPorCodigo(p.codigo);
    const asiste = String(p.asiste) === 'si';
    let cantidad = asiste ? Math.round(Number(p.cantidad) || 1) : 0;
    if (cantidad > inv.lugares) cantidad = inv.lugares;
    if (asiste && cantidad < 1) cantidad = 1;
    marcar(inv.codigo, {
      estado: asiste ? 'confirmado' : 'no_asiste',
      cantidad: cantidad,
      menu: asiste ? limpiar(p.menu, 80) : '',
      traslado: asiste ? (String(p.traslado) === 'si' ? 'si' : 'no') : '',
      mensaje: limpiar(p.mensaje, 500),
      respondido: new Date()
    });
    return buscarPorCodigo(inv.codigo);
  } finally {
    lock.releaseLock();
  }
}

function marcar(codigo, cambios) {
  const fila = filaDe(codigo);
  if (fila < 0) throw new Error('No existe el invitado ' + codigo);
  const h = hojaInvitados();
  Object.keys(cambios).forEach(function (k) {
    const col = COLUMNAS.indexOf(k);
    if (col >= 0) h.getRange(fila, col + 1).setValue(cambios[k]);
  });
}

function guardar(d) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const nombre = limpiar(d.nombre, 120);
    if (!nombre) throw new Error('El invitado necesita un nombre.');
    const base = {
      nombre: nombre,
      identificador: limpiar(d.identificador, 60),
      categoria: limpiar(d.categoria, 60),
      lugares: Math.max(1, Math.min(30, Math.round(Number(d.lugares) || 1))),
      tipo: d.tipo === 'solo_fiesta' ? 'solo_fiesta' : 'completo'
    };
    if (d.codigo && filaDe(d.codigo) > 0) {
      marcar(d.codigo, base);
      return buscarPorCodigo(d.codigo);
    }
    const codigo = codigoNuevo();
    hojaInvitados().appendRow(COLUMNAS.map(function (c) {
      if (c === 'codigo') return codigo;
      if (c === 'estado') return 'pendiente';
      if (c === 'cantidad') return 0;
      return base[c] !== undefined ? base[c] : '';
    }));
    return buscarPorCodigo(codigo);
  } finally {
    lock.releaseLock();
  }
}

function importar(lista) {
  if (!Array.isArray(lista)) throw new Error('La lista para importar no es válida.');
  if (lista.length > 1000) throw new Error('Se pueden importar hasta 1000 invitados por vez.');
  let n = 0;
  lista.forEach(function (d) { if (d && d.nombre) { guardar({ nombre: d.nombre, identificador: d.identificador, categoria: d.categoria, lugares: d.lugares, tipo: d.tipo }); n++; } });
  return n;
}

function borrar(codigo) {
  const fila = filaDe(codigo);
  if (fila < 0) throw new Error('No existe el invitado ' + codigo);
  hojaInvitados().deleteRow(fila);
}

/* ---------- Utilidades ---------- */
function codigoNuevo() {
  let c;
  do { c = crearCodigo(6); } while (filaDe(c) > 0);
  return c;
}

function crearCodigo(largo) {
  const letras = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // sin 0, O, 1, I para que no se confundan
  let s = '';
  for (let i = 0; i < largo; i++) s += letras.charAt(Math.floor(Math.random() * letras.length));
  return s;
}

function limpiar(v, max) {
  let s = String(v == null ? '' : v).replace(/[\u0000-\u001F]/g, ' ').trim().slice(0, max);
  // Evita que un texto escrito por un invitado se interprete como fórmula en la planilla
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}

function formatoFecha(v) {
  if (v instanceof Date) return Utilities.formatDate(v, Session.getScriptTimeZone(), 'yyyy-MM-dd');
  return v ? String(v) : '';
}

/* ---------- Envío de invitaciones por mail ---------- */
/* Menú propio en la planilla: aparece arriba como "Invitaciones" */
function onOpen() {
  SpreadsheetApp.getUi().createMenu('Invitaciones')
    .addItem('Enviar una prueba a mi correo', 'enviarPrueba')
    .addItem('Enviar a los que todavía no recibieron', 'enviarPendientes')
    .addSeparator()
    .addItem('Empezar una reunión nueva…', 'reunionNueva')
    .addToUi();
}

const HOJA_MAIL = 'Mail';
function crearHojaMail() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let h = ss.getSheetByName(HOJA_MAIL);
  if (h && String(h.getRange('B2').getValue()).indexOf('{texto}') >= 0) return;
  if (!h) h = ss.insertSheet(HOJA_MAIL);
  h.getRange('A1:B1').setValues([['Asunto', '{numero} Reunión Federativa {anio} · {ciudad} · {fecha}']]);
  h.getRange('A2:B2').setValues([['Texto', [
    'Estimados {cuartel}:',
    '',
    'La Federación de Asociaciones de Bomberos Voluntarios de la Provincia de Buenos Aires los invita a participar de la {numero} Reunión Federativa del año {anio}, el próximo {fecha}.',
    '',
    '{texto}',
    '',
    'Los esperamos en {lugar}, {direccion}, a partir de las {hora} hs.',
    '',
    'En la invitación encontrarán el cronograma completo, los lugares y la confirmación de asistencia de su delegación:',
    '{boton}',
    '{aviso}. Los esperamos.'
  ].join('\n')]]);
  h.getRange('A3:B3').setValues([['Texto del botón', 'Ver la invitación y confirmar asistencia']]);
  h.getRange('A1:A3').setFontWeight('bold');
  h.setColumnWidth(1, 140); h.setColumnWidth(2, 640);
  h.getRange('B2').setWrap(true).setVerticalAlignment('top');
  h.getRange('A5').setValue('Podés cambiar el asunto y el texto. {cuartel} se reemplaza por el nombre de cada cuartel y {boton} por el botón con su link personal. Los datos de la reunión salen de la hoja Reunión: {numero} {anio} {fecha} {ciudad} {region} {anfitrion} {lugar} {direccion} {hora} {texto} {aviso}');
}

function armarMail(nombre, codigo) {
  const cfg = leerConfig();
  const h = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_MAIL);
  if (!h) throw new Error('Falta la hoja Mail. Ejecutá la función configurar.');
  const asunto = completar(String(h.getRange('B1').getValue()));
  const texto = completar(String(h.getRange('B2').getValue()));
  const textoBoton = String(h.getRange('B3').getValue() || 'Ver la invitación');
  const link = String(cfg.link_invitacion || '') + '?i=' + encodeURIComponent(codigo);
  const esc = function (t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); };
  const boton = '<div style="margin:22px 0"><a href="' + link + '" style="display:inline-block;background:#C9A24A;color:#111;text-decoration:none;font-weight:bold;padding:12px 22px;border-radius:4px;font-family:Arial,sans-serif">' + esc(textoBoton) + '</a></div>';
  const html = '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.55;color:#222;max-width:600px">' +
    esc(texto.replace(/\{cuartel\}/g, nombre)).split('{boton}').join('\u0000').replace(/\n/g, '<br>').replace('\u0000', boton) +
    '</div>';
  const plano = texto.replace(/\{cuartel\}/g, nombre).replace('{boton}', textoBoton + ': ' + link);
  return { asunto: asunto, html: html, plano: plano, link: link };
}

function enviarA(email, nombre, codigo) {
  const m = armarMail(nombre, codigo);
  MailApp.sendEmail({ to: email, subject: m.asunto, body: m.plano, htmlBody: m.html, name: String(leerConfig().remitente || 'Federación') });
}

function enviarPrueba() {
  const ui = SpreadsheetApp.getUi();
  const yo = Session.getActiveUser().getEmail();
  const primero = leerInvitados()[0];
  if (!primero) { ui.alert('Primero cargá al menos un cuartel en la hoja Invitados.'); return; }
  enviarA(yo, primero.nombre, primero.codigo);
  ui.alert('Listo: te mandé una prueba a ' + yo + ' como si fueras "' + primero.nombre + '". No se marcó como enviada.');
}

function enviarPendientes() {
  const ui = SpreadsheetApp.getUi();
  const lista = leerInvitados().filter(function (g) { return g.email && String(g.enviada) !== 'si'; });
  const sinMail = leerInvitados().filter(function (g) { return !g.email; }).length;
  if (!lista.length) { ui.alert('No hay cuarteles pendientes de envío' + (sinMail ? ' (hay ' + sinMail + ' sin mail cargado).' : '.')); return; }
  const cupo = MailApp.getRemainingDailyQuota();
  const r = ui.alert('Enviar invitaciones', 'Se van a mandar ' + lista.length + ' mails, uno por cuartel, con su link personal.' +
    (sinMail ? '\n' + sinMail + ' cuarteles no tienen mail y se saltean.' : '') +
    '\nHoy se pueden mandar ' + cupo + ' mails más desde esta cuenta.\n\n¿Enviar ahora?', ui.ButtonSet.YES_NO);
  if (r !== ui.Button.YES) return;
  let ok = 0; const fallas = [];
  for (let i = 0; i < lista.length; i++) {
    if (ok >= cupo) { fallas.push('Se llegó al límite diario: el resto se manda mañana con el mismo menú.'); break; }
    const g = lista[i];
    try { enviarA(String(g.email).trim(), g.nombre, g.codigo); marcar(g.codigo, { enviada: 'si' }); ok++; }
    catch (e) { fallas.push(g.nombre + ': ' + e.message); }
  }
  ui.alert('Se enviaron ' + ok + ' invitaciones.' + (fallas.length ? '\n\nNo se pudieron enviar:\n' + fallas.join('\n') : ''));
}

/* ---------- Datos de la reunión (hojas "Reunión" y "Cronograma") ---------- */
const HOJA_REUNION = 'Reunión';
const HOJA_CRONO = 'Cronograma';
const CAMPOS = [
  ['numero', 'Número de reunión', '3ra', 'Ej: 1ra, 2da, 3ra, 4ta'],
  ['anio', 'Año', '2026', ''],
  ['fecha', 'Fecha', '12/09/2026', 'Día/mes/año'],
  ['hora', 'Hora de inicio', '8:00', 'Ej: 8:00'],
  ['hora_fin', 'Hora de fin', '13:00', 'Para agendar en el calendario'],
  ['ciudad', 'Ciudad', 'Saladillo', ''],
  ['region', 'Región', 'Región Centro Centro', ''],
  ['anfitrion', 'Cuartel anfitrión', 'Bomberos Voluntarios de Saladillo', ''],
  ['lugar', 'Lugar', 'Escuela Secundaria N° 2 Manuel Pardal', 'Dónde se hace la reunión'],
  ['direccion', 'Dirección del lugar', 'Av. Pereyra 3046, Saladillo, Provincia de Buenos Aires', 'Se usa para el mapa'],
  ['lugar2', 'Otro lugar (opcional)', 'Cuartel de Bomberos Voluntarios de Saladillo', 'Ej: donde es el desayuno. Vacío = no se muestra'],
  ['direccion2', 'Dirección del otro lugar', 'Rivadavia N° 2852, Saladillo, Provincia de Buenos Aires', ''],
  ['detalle2', 'Detalle del otro lugar', 'Desayuno a las 7:00 h', ''],
  ['texto', 'Texto del encuentro', 'En esta oportunidad, la Región Centro Centro y en particular los Bomberos Voluntarios de Saladillo nos recibirán para debatir propuestas y sentar las bases del progreso de nuestras entidades asociadas.', 'El párrafo principal de la invitación y del mail'],
  ['presentes', 'Quiénes estarán', 'Comisión Directiva, Presidentes de Regiones, Directores de Sistemas, Fondo Federativo', 'Separados por coma. Vacío = no se muestra'],
  ['aviso', 'Aviso importante', 'No olviden realizar su inscripción en el GIB', 'Se destaca en la invitación y va al final del mail'],
  ['aviso_detalle', 'Aclaración del aviso', 'La inscripción oficial se hace en el GIB. La confirmación de esta invitación nos ayuda a organizar la recepción de las delegaciones.', ''],
  ['foto1', 'Foto de la ciudad (link)', 'https://evocard.com.ar/fed/saladillo-plaza.jpg', 'Link de Drive compartido o de una imagen. Vacío = sin foto'],
  ['foto1_pie', 'Texto sobre la foto de la ciudad', 'Ciudad de Saladillo', ''],
  ['foto2', 'Foto del lugar (link)', 'https://evocard.com.ar/fed/saladillo-escuela.jpg', 'Vacío = sin foto']
];
const CRONO_INICIAL = [
  ['07:00', 'Desayuno en el Cuartel', 'Rivadavia N° 2852, Saladillo', 'no', 'si', 'Rivadavia 2852, Saladillo, Provincia de Buenos Aires'],
  ['08:00', 'Recibimiento de delegaciones y acreditación', 'Escuela Secundaria N° 2 Manuel Pardal', 'no', 'no', ''],
  ['08:30', 'Reunión Sistemas de Operaciones, Capacitación y Escuela de Cadetes', '', 'no', 'si', ''],
  ['08:30', 'Reunión del Fondo Federativo', '', 'no', 'si', ''],
  ['08:30', 'Capacitación Administrativa, Rendición de Subsidios Nacionales y Provinciales, TAD, Documentación Administrativa', '', 'no', 'si', ''],
  ['08:30', 'Capacitación Ley 13.802 y Documentación Bomberil Básica', '', 'no', 'si', ''],
  ['08:30', 'Capacitación GIB', '', 'no', 'si', ''],
  ['08:30', 'Capacitación para Regionales de Género y Ética', '', 'no', 'si', ''],
  ['10:00', 'Acto Protocolar por Apertura de la 3ra Reunión Federativa', 'Todas las personas de las Reuniones y Capacitaciones deben participar en el acto, por lo que se pide culminar o interrumpir las mismas durante este horario.', 'si', 'no', ''],
  ['11:30', 'Reunión de Comisión Directiva FABVPBA', '', 'no', 'no', '']
];

function crearHojasReunion() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss.getSheetByName(HOJA_REUNION)) {
    const h = ss.insertSheet(HOJA_REUNION, 0);
    h.getRange(1, 1, CAMPOS.length + 1, 3).setNumberFormat('@');
    h.getRange(1, 1, 1, 3).setValues([['Dato', 'Valor', 'Ayuda']]).setFontWeight('bold');
    h.getRange(2, 1, CAMPOS.length, 3).setValues(CAMPOS.map(function (c) { return [c[1], c[2], c[3]]; }));
    h.getRange(2, 1, CAMPOS.length, 1).setFontWeight('bold');
    h.getRange(2, 3, CAMPOS.length, 1).setFontColor('#777777');
    h.setColumnWidth(1, 230); h.setColumnWidth(2, 520); h.setColumnWidth(3, 330);
    h.getRange(2, 2, CAMPOS.length, 1).setWrap(true);
    h.setFrozenRows(1);
  }
  if (!ss.getSheetByName(HOJA_CRONO)) {
    const c = ss.insertSheet(HOJA_CRONO, 1);
    c.getRange(1, 1, 60, 6).setNumberFormat('@');
    c.getRange(1, 1, 1, 6).setValues([['Hora', 'Actividad', 'Aclaración (opcional)', 'Destacar (si/no)', 'Se marca al confirmar (si/no)', 'Dirección para el mapa (opcional)']]).setFontWeight('bold');
    c.getRange(2, 1, CRONO_INICIAL.length, 6).setValues(CRONO_INICIAL);
    c.setColumnWidth(1, 70); c.setColumnWidth(2, 420); c.setColumnWidth(3, 380); c.setColumnWidth(4, 120); c.setColumnWidth(5, 190); c.setColumnWidth(6, 300);
    c.getRange(2, 2, 59, 2).setWrap(true);
    c.setFrozenRows(1);
  }
}

function aTexto(v) {
  if (v instanceof Date) {
    if (v.getFullYear() < 1901) return Utilities.formatDate(v, Session.getScriptTimeZone(), 'HH:mm');
    return Utilities.formatDate(v, Session.getScriptTimeZone(), 'dd/MM/yyyy');
  }
  return String(v == null ? '' : v).trim();
}

function datosReunion() {
  const h = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_REUNION);
  if (!h) throw new Error('Falta la hoja Reunión.');
  const filas = h.getDataRange().getValues();
  const r = {};
  CAMPOS.forEach(function (c) {
    const f = filas.filter(function (x) { return String(x[0]).trim() === c[1]; })[0];
    r[c[0]] = f ? aTexto(f[1]) : '';
  });
  return r;
}

const MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
const DIAS = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
function fechaLarga(f) {
  const m = String(f).match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
  if (!m) return String(f);
  const d = new Date(Number(m[3]), Number(m[2]) - 1, Number(m[1]));
  return DIAS[d.getDay()] + ' ' + Number(m[1]) + ' de ' + MESES[Number(m[2]) - 1] + ' de ' + m[3];
}

function leerReunion() {
  const r = datosReunion();
  const c = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_CRONO);
  const crono = c ? c.getDataRange().getValues().slice(1).filter(function (x) { return aTexto(x[1]); }).map(function (x) {
    return { hora: aTexto(x[0]), titulo: aTexto(x[1]), detalle: aTexto(x[2]),
      destacar: aTexto(x[3]).toLowerCase() === 'si', marcar: aTexto(x[4]).toLowerCase() === 'si', mapa: aTexto(x[5]) };
  }) : [];
  return { reunion: r, cronograma: crono };
}

function completar(t) {
  const r = datosReunion();
  const v = { numero: r.numero, anio: r.anio, fecha: fechaLarga(r.fecha), ciudad: r.ciudad, region: r.region, anfitrion: r.anfitrion,
    lugar: r.lugar, direccion: r.direccion, hora: r.hora, texto: r.texto, aviso: r.aviso };
  return String(t).replace(/\{(numero|anio|fecha|ciudad|region|anfitrion|lugar|direccion|hora|texto|aviso)\}/g, function (_, k) { return v[k] || ''; });
}

/* Guarda las respuestas de la reunión actual en una hoja aparte y deja a todos los cuarteles listos para la próxima */
function reunionNueva() {
  const ui = SpreadsheetApp.getUi();
  const r = datosReunion();
  const nombre = 'Archivo ' + (r.numero || '') + ' ' + (r.anio || '') + ' ' + (r.ciudad || '');
  const ok = ui.alert('Empezar una reunión nueva',
    'Se van a guardar las respuestas actuales en la hoja "' + nombre.trim() + '" y todos los cuarteles quedan "sin responder" y "sin enviar".\n' +
    'La lista de cuarteles y sus mails se mantiene.\n\nDespués completá la hoja Reunión y la hoja Cronograma con los datos nuevos.\n\n¿Continuar?', ui.ButtonSet.YES_NO);
  if (ok !== ui.Button.YES) return;
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const inv = hojaInvitados();
  let n = nombre.trim(), k = 2;
  while (ss.getSheetByName(n)) n = nombre.trim() + ' (' + (k++) + ')';
  inv.copyTo(ss).setName(n);
  const filas = inv.getLastRow() - 1;
  if (filas > 0) {
    const limpiar1 = { estado: 'pendiente', cantidad: 0, menu: '', traslado: '', mensaje: '', respondido: '', enviada: '' };
    Object.keys(limpiar1).forEach(function (col) {
      const i = COLUMNAS.indexOf(col);
      inv.getRange(2, i + 1, filas, 1).setValue(limpiar1[col]);
    });
  }
  ui.alert('Listo. Las respuestas anteriores quedaron en la hoja "' + n + '". Ahora actualizá las hojas Reunión y Cronograma.');
}
