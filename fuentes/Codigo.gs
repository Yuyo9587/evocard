/** @OnlyCurrentDoc */
/**
 * EVOCARD — Programa de la planilla (Google Apps Script)
 * Un archivo por evento: guarda la lista de invitados y sus confirmaciones.
 *
 * Cómo se usa (resumen; la guía tiene el paso a paso):
 *   1. Creá una planilla nueva en Google Sheets.
 *   2. Extensiones > Apps Script. Borrá lo que hay y pegá TODO este archivo.
 *   3. Elegí la función "configurar" arriba y tocá Ejecutar (la primera vez pide permisos).
 *      Después elegí "autorizarAlbum" y tocá Ejecutar (permiso de Google Drive para el álbum de fotos).
 *   4. Implementar > Nueva implementación > Aplicación web.
 *      Ejecutar como: Yo. Quién tiene acceso: Cualquier persona.
 *   5. Copiá la dirección que termina en /exec: esa va en el panel y en la invitación.
 *
 * Las respuestas siempre son JSON: { ok: true, ... } o { ok: false, error: "..." }
 */

const HOJA_INVITADOS = 'Invitados';
const HOJA_CONFIG = 'Config';
const COLUMNAS = ['codigo', 'nombre', 'identificador', 'categoria', 'lugares', 'tipo',
  'estado', 'cantidad', 'menu', 'traslado', 'mensaje', 'respondido', 'enviada'];
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
    cfg.appendRow(['evento', 'Casamiento de Lucía y Tomás']);
    cfg.appendRow(['clave_panel', crearCodigo(8)]);
    cfg.appendRow(['fecha_limite', '2027-02-14']);
    cfg.appendRow(['respuestas_abiertas', 'si']);
    cfg.appendRow(['album_abierto', 'si']);
    cfg.setFrozenRows(1);
  }
  const hoja1 = ss.getSheetByName('Hoja 1') || ss.getSheetByName('Sheet1');
  if (hoja1 && hoja1.getLastRow() === 0 && ss.getSheets().length > 2) ss.deleteSheet(hoja1);
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
  if (accion === 'subirFoto') return subirFoto(p);

  // Acciones del panel: necesitan la clave
  const cfg = leerConfig();
  if (!p.clave || String(p.clave) !== String(cfg.clave_panel)) throw new Error('La clave del panel no es correcta.');
  if (accion === 'lista') return { evento: datosPublicosEvento(), invitados: leerInvitados() };
  if (accion === 'guardar') return { invitado: guardar(p.invitado || {}) };
  if (accion === 'borrar') { borrar(p.codigo); return {}; }
  if (accion === 'importar') return { agregados: importar(p.invitados || []) };
  if (accion === 'enviada') { marcar(p.codigo, { enviada: 'si' }); return {}; }
  if (accion === 'fotos') return listarFotos();
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
    respuestas_abiertas: String(c.respuestas_abiertas || 'si').toLowerCase() !== 'no',
    album_abierto: String(c.album_abierto || 'si').toLowerCase() !== 'no'
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

/* ---------- Álbum de fotos (carpeta de Google Drive del evento) ---------- */
const MAX_FOTO_BYTES = 6 * 1024 * 1024;   // 6 MB por foto (la invitación ya las achica antes de mandarlas)
const MAX_FOTOS = 3000;                   // tope de fotos por evento

function guardarConfig(clave, valor) {
  const hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_CONFIG);
  const filas = hoja.getDataRange().getValues();
  for (let i = 1; i < filas.length; i++) {
    if (String(filas[i][0]) === clave) { hoja.getRange(i + 1, 2).setValue(valor); return; }
  }
  hoja.appendRow([clave, valor]);
}

function carpetaFotos() {
  const cfg = leerConfig();
  if (cfg.carpeta_fotos) {
    try { return DriveApp.getFolderById(String(cfg.carpeta_fotos)); } catch (e) { /* la borraron: se crea otra */ }
  }
  const nombre = 'Evocard - Fotos - ' + (cfg.evento || SpreadsheetApp.getActiveSpreadsheet().getName());
  const carpeta = DriveApp.createFolder(nombre);
  // Cualquiera con el link puede VER (sirve para mostrar las miniaturas en el panel); nadie puede editar ni borrar.
  try { carpeta.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW); } catch (e) {}
  guardarConfig('carpeta_fotos', carpeta.getId());
  return carpeta;
}

function subirFoto(p) {
  if (!datosPublicosEvento().album_abierto) throw new Error('El álbum de fotos está cerrado.');
  const tipo = String(p.tipo || 'image/jpeg');
  if (!/^image\/(jpeg|png|webp|heic|heif)$/.test(tipo)) throw new Error('Solo se pueden subir fotos.');
  const datos = String(p.datos || '');
  if (!datos) throw new Error('No llegó ninguna foto.');
  const bytes = Utilities.base64Decode(datos);
  if (bytes.length > MAX_FOTO_BYTES) throw new Error('La foto es demasiado grande.');
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const carpeta = carpetaFotos();
    const cuenta = Number(leerConfig().fotos_subidas) || 0;
    if (cuenta >= MAX_FOTOS) throw new Error('El álbum ya está lleno.');
    const autor = limpiar(p.autor, 60).replace(/^'/, '');
    const ext = tipo === 'image/png' ? 'png' : tipo === 'image/webp' ? 'webp' : 'jpg';
    const nombre = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd HH.mm.ss') +
      (autor ? ' - ' + autor.replace(/[\\/:*?"<>|]/g, '') : '') + '.' + ext;
    const archivo = carpeta.createFile(Utilities.newBlob(bytes, tipo, nombre));
    if (autor) archivo.setDescription('Subida por ' + autor);
    guardarConfig('fotos_subidas', cuenta + 1);
    return { foto: { id: archivo.getId() } };
  } finally {
    lock.releaseLock();
  }
}

function listarFotos() {
  const cfg = leerConfig();
  if (!cfg.carpeta_fotos) return { fotos: [], carpeta: '' };
  let carpeta;
  try { carpeta = DriveApp.getFolderById(String(cfg.carpeta_fotos)); } catch (e) { return { fotos: [], carpeta: '' }; }
  const fotos = [];
  const it = carpeta.getFiles();
  while (it.hasNext() && fotos.length < MAX_FOTOS) {
    const f = it.next();
    fotos.push({ id: f.getId(), nombre: f.getName(), autor: String(f.getDescription() || '').replace(/^Subida por /, ''), fecha: f.getDateCreated().toISOString() });
  }
  fotos.sort(function (a, b) { return a.fecha < b.fecha ? 1 : -1; });
  return { fotos: fotos, carpeta: carpeta.getUrl() };
}

/* Ejecutar una vez desde el editor para dar el permiso de Google Drive (crea la carpeta del álbum). */
function autorizarAlbum() {
  const carpeta = carpetaFotos();
  Logger.log('Listo. Carpeta del álbum: ' + carpeta.getUrl());
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
