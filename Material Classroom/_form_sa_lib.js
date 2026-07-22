// Llibreria compartida per crear el Google Form d'una fitxa d'unitat (B/M) i
// penjar-lo com a tasca de Classroom (patró replicat del projecte Robòtica).
// - El Form es desa a la carpeta de Drive del curs (DRIVE_FOLDER_ID).
// - El tema es busca per l'etiqueta (p. ex. "B3", "M2") al nom; si no existeix, es crea.
// - maxPoints i state (PUBLISHED/DRAFT) venen de la definició.
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { google } from 'googleapis';
import { authenticate } from '@google-cloud/local-auth';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Àmbits mínims per publicar material: cap flux d'aquests scripts no llegeix
// llistes d'alumnat ni correus, així que classroom.rosters i
// classroom.profile.emails no s'inclouen (token compromès = menys dades exposades).
// Si es canvia aquesta llista: esborrar token.json i reautoritzar al navegador.
const SCOPES = [
  'https://www.googleapis.com/auth/forms.body',
  'https://www.googleapis.com/auth/drive.file',
  'https://www.googleapis.com/auth/classroom.courses',
  'https://www.googleapis.com/auth/classroom.coursework.students',
  'https://www.googleapis.com/auth/classroom.courseworkmaterials',
  'https://www.googleapis.com/auth/classroom.announcements',
  'https://www.googleapis.com/auth/classroom.topics'
];

const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');
const TOKEN_PATH = path.join(__dirname, 'token.json');

// La identitat del curs viu a config.js (un sol lloc per canviar de curs);
// es re-exporta aquí perquè els scripts existents no es trenquin.
export { COURSE_ID, DRIVE_FOLDER_ID, WEB_BASE } from './config.js';
import { COURSE_ID, DRIVE_FOLDER_ID } from './config.js';

// --- Helpers per escriure definicions compactes ---------------------------
export const AUTOAVAL_COLS = ['Insuficient', 'Suficient/Bé', 'Notable', 'Excel·lent'];

export const t = (titol, text) => ({ kind: 'text', titol, text });
export const p = (titol, desc) => ({ kind: 'q', titol, desc, paragraph: true, required: true });
export const pOpt = (titol, desc) => ({ kind: 'q', titol, desc, paragraph: true, required: false });
export const s = (titol, desc) => ({ kind: 'q', titol, desc, paragraph: false, required: true });
export const sOpt = (titol, desc) => ({ kind: 'q', titol, desc, paragraph: false, required: false });
export const radio = (titol, opcions, desc) => ({ kind: 'radio', titol, opcions, desc, required: true });
export const check = (titol, opcions, desc) => ({ kind: 'check', titol, opcions, desc, required: false });
export const grid = (titol, desc, rows, columns) => ({ kind: 'grid', titol, desc, rows, columns });
export const autoaval = (rows) => grid(
  'M’autoavaluo (la nota és 0-10)',
  'Marca el teu nivell a cada criteri.',
  rows, AUTOAVAL_COLS);

// ---------------------------------------------------------------------------
export async function getAuthClient() {
  if (fs.existsSync(TOKEN_PATH)) {
    const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
    return google.auth.fromJSON(token);
  }
  console.log('🔄 Autenticant per primera vegada amb Google...');
  const client = await authenticate({ scopes: SCOPES, keyfilePath: CREDENTIALS_PATH });
  if (client.credentials) {
    const keys = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
    const key = keys.installed || keys.web;
    fs.writeFileSync(TOKEN_PATH, JSON.stringify({
      type: 'authorized_user',
      client_id: key.client_id,
      client_secret: key.client_secret,
      refresh_token: client.credentials.refresh_token,
    }));
    console.log('✅ Token desat a token.json');
  }
  return client;
}

// Reintents amb espera exponencial per als errors transitoris de les APIs de
// Google (429 quota, 5xx). Els altres errors es rellancen de seguida.
export async function ambReintents(fn, etiqueta = 'crida API', intents = 4) {
  for (let i = 1; ; i++) {
    try {
      return await fn();
    } catch (e) {
      const codi = e?.code || e?.response?.status;
      const transitori = codi === 429 || (codi >= 500 && codi < 600);
      if (!transitori || i >= intents) throw e;
      const espera = 1000 * 2 ** (i - 1);
      console.log(`⏳ ${etiqueta}: error ${codi}, reintent ${i}/${intents - 1} d'aquí ${espera / 1000}s...`);
      await new Promise(r => setTimeout(r, espera));
    }
  }
}

function itemToRequest(it, index) {
  let item;
  if (it.kind === 'text') {
    item = { title: it.titol, description: it.text, textItem: {} };
  } else if (it.kind === 'grid') {
    item = {
      title: it.titol,
      description: it.desc,
      questionGroupItem: {
        grid: {
          columns: { type: 'RADIO', options: it.columns.map(c => ({ value: c })) }
        },
        questions: it.rows.map(r => ({ required: false, rowQuestion: { title: r } }))
      }
    };
  } else if (it.kind === 'radio' || it.kind === 'check') {
    item = {
      title: it.titol,
      description: it.desc,
      questionItem: {
        question: {
          required: !!it.required,
          choiceQuestion: {
            type: it.kind === 'radio' ? 'RADIO' : 'CHECKBOX',
            options: it.opcions.map(o => ({ value: o }))
          }
        }
      }
    };
  } else {
    item = {
      title: it.titol,
      description: it.desc,
      questionItem: {
        question: { required: !!it.required, textQuestion: { paragraph: !!it.paragraph } }
      }
    };
  }
  return { createItem: { item, location: { index } } };
}

// Deduplicació real contra Classroom: retorna la tasca existent amb aquest
// títol (esborranys inclosos), o null. Així la idempotència no depèn dels
// resultats_*.json locals.
export async function trobaTascaPerTitol(classroom, titol) {
  const res = await ambReintents(
    () => classroom.courses.courseWork.list({
      courseId: COURSE_ID,
      courseWorkStates: ['PUBLISHED', 'DRAFT'],
      pageSize: 200,
      fields: 'courseWork(id,title,alternateLink,state)'
    }),
    'llistar courseWork');
  return (res.data.courseWork || []).find(w => w.title === titol) || null;
}

export async function crearIPenjar(def) {
  const auth = await getAuthClient();
  const forms = google.forms({ version: 'v1', auth });
  const drive = google.drive({ version: 'v3', auth });
  const classroom = google.classroom({ version: 'v1', auth });

  console.log(`\n=== ${def.sa.toUpperCase()} · ${def.titol} ===`);

  // Idempotència: si la tasca ja existeix a Classroom, no es crea res de nou.
  const existent = await trobaTascaPerTitol(classroom, def.titol);
  if (existent) {
    console.log(`⏭️ Ja existeix a Classroom (${existent.state}): ${existent.alternateLink} — no es duplica.`);
    return {
      sa: def.sa, formId: null, formUrl: null,
      taskUrl: existent.alternateLink, state: existent.state, jaExistia: true
    };
  }

  console.log('📝 Creant el Google Form...');
  const createRes = await ambReintents(
    () => forms.forms.create({
      requestBody: { info: { title: def.titol, documentTitle: def.titol } }
    }), 'crear Form');
  const formId = createRes.data.formId;

  // A partir d'aquí, si alguna crida falla el Form quedaria orfe al Drive:
  // s'esborra abans de rellançar l'error perquè re-executar no dupliqui.
  try {
    const requests = [{
      updateFormInfo: {
        info: { title: def.titol, description: def.descripcioForm },
        updateMask: 'description'
      }
    }];
    def.items.forEach((it, i) => requests.push(itemToRequest(it, i)));

    console.log(`⚙️ Afegint ${def.items.length} elements al formulari...`);
    await ambReintents(
      () => forms.forms.batchUpdate({ formId, requestBody: { requests } }),
      'batchUpdate del Form');

    console.log('📁 Movent el Form a la carpeta del curs a Drive...');
    const fileMeta = await ambReintents(
      () => drive.files.get({ fileId: formId, fields: 'parents' }), 'llegir parents');
    await ambReintents(
      () => drive.files.update({
        fileId: formId,
        addParents: DRIVE_FOLDER_ID,
        removeParents: (fileMeta.data.parents || []).join(','),
        fields: 'id, parents'
      }), 'moure a la carpeta');

    const getRes = await ambReintents(() => forms.forms.get({ formId }), 'llegir Form');
    const responderUri = getRes.data.responderUri;

    // Tema de Classroom: cerca l'etiqueta (p. ex. "B3") al nom, crea'l si no hi és.
    const saTag = def.sa.toUpperCase();
    let topicId = null;
    const topicsRes = await ambReintents(
      () => classroom.courses.topics.list({ courseId: COURSE_ID }), 'llistar temes');
    const topics = topicsRes.data.topic || [];
    const found = topics.find(tp => tp.name && tp.name.toUpperCase().startsWith(saTag));
    if (found) {
      topicId = found.topicId;
      console.log(`✅ Tema trobat: "${found.name}"`);
    } else {
      const newTopic = await ambReintents(
        () => classroom.courses.topics.create({
          courseId: COURSE_ID, requestBody: { name: def.topicName }
        }), 'crear tema');
      topicId = newTopic.data.topicId;
      console.log(`✅ Tema creat: "${def.topicName}"`);
    }

    console.log(`🚀 Creant la tasca (${def.state}, ${def.maxPoints} punts)...`);
    const body = {
      title: def.titol,
      description: def.descripcioTasca,
      maxPoints: def.maxPoints,
      workType: 'ASSIGNMENT',
      state: def.state,
      topicId,
      materials: [
        { link: { url: responderUri, title: `${def.titol} (Google Form)` } },
        ...(def.materials || [])
      ]
    };
    const cw = await ambReintents(
      () => classroom.courses.courseWork.create({ courseId: COURSE_ID, requestBody: body }),
      'crear la tasca');

    const result = {
      sa: def.sa,
      formId,
      formUrl: responderUri,
      taskUrl: cw.data.alternateLink,
      state: def.state
    };
    console.log(`🏆 Fet. Tasca: ${result.taskUrl}`);
    return result;
  } catch (e) {
    console.log(`🧹 Error a mig fer: esborrant el Form orfe ${formId}...`);
    try { await drive.files.delete({ fileId: formId }); }
    catch (e2) { console.log(`⚠️ No s'ha pogut esborrar el Form orfe: ${e2.message}`); }
    throw e;
  }
}
