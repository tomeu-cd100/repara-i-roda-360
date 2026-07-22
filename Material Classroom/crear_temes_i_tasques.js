// Crea, per a cada unitat B0-9/M0-9, un tema de Classroom i una tasca
// ASSIGNMENT en DRAFT que enllaça la fitxa d'alumnat de la unitat al web
// publicat. Sense punts (avaluació qualitativa NA/AS/AN/AE, sense examens):
// la tasca serveix perquè l'alumnat tingui accés digital a la fitxa, no per
// recollir lliuraments ni posar nota numèrica.
// Idempotent per títol (temes i tasques): re-executar no duplica.
//
// Ús: node crear_temes_i_tasques.js   (des de Material Classroom/)
import { google } from 'googleapis';
import { getAuthClient, ambReintents, trobaTascaPerTitol } from './_form_sa_lib.js';
import { COURSE_ID, GRADE_CATEGORIES, UNITAT_TRIMESTRE, WEB_BASE } from './config.js';

const UNITATS = [
  { codi: 'B0', assignatura: 'bicicletes', slug: 'b0_punt_de_partida', titol: 'Punt de partida' },
  { codi: 'B1', assignatura: 'bicicletes', slug: 'b1_la_bici_per_dins', titol: 'La bici per dins' },
  { codi: 'B2', assignatura: 'bicicletes', slug: 'b2_posada_a_punt', titol: 'Posada a punt' },
  { codi: 'B3', assignatura: 'bicicletes', slug: 'b3_rodes_i_punxades', titol: 'Rodes i punxades' },
  { codi: 'B4', assignatura: 'bicicletes', slug: 'b4_frens', titol: 'Frens' },
  { codi: 'B5', assignatura: 'bicicletes', slug: 'b5_transmissio_i', titol: 'Transmissió I: cadena i pedals' },
  { codi: 'B6', assignatura: 'bicicletes', slug: 'b6_transmissio_ii', titol: 'Transmissió II: canvis i desviadors' },
  { codi: 'B7', assignatura: 'bicicletes', slug: 'b7_punts_de_contacte', titol: 'Punts de contacte' },
  { codi: 'B8', assignatura: 'bicicletes', slug: 'b8_seguretat_viaria', titol: 'Seguretat i normativa viària' },
  { codi: 'B9', assignatura: 'bicicletes', slug: 'b9_repara_i_roda', titol: 'Repara i Roda (sortides)' },
  { codi: 'M0', assignatura: 'maker', slug: 'm0_benvinguda_maker', titol: 'Benvinguda maker i seguretat' },
  { codi: 'M1', assignatura: 'maker', slug: 'm1_tinkercad', titol: 'Tinkercad des de zero' },
  { codi: 'M2', assignatura: 'maker', slug: 'm2_peu_de_rei', titol: 'Mesurar amb el peu de rei' },
  { codi: 'M3', assignatura: 'maker', slug: 'm3_enginyeria_inversa', titol: 'Enginyeria inversa: la maneta de fre' },
  { codi: 'M4', assignatura: 'maker', slug: 'm4_peces_utils', titol: 'Peces útils per a la bici (3D)' },
  { codi: 'M5', assignatura: 'maker', slug: 'm5_decoratives', titol: 'Peces decoratives temàtica bici (3D)' },
  { codi: 'M6', assignatura: 'maker', slug: 'm6_inkscape', titol: 'Inkscape al Chromebook' },
  { codi: 'M7', assignatura: 'maker', slug: 'm7_tallar_utils', titol: 'Tallar peces útils' },
  { codi: 'M8', assignatura: 'maker', slug: 'm8_retols_laser', titol: 'Rètols i decoració a làser' },
  { codi: 'M9', assignatura: 'maker', slug: 'm9_recorregut_360', titol: 'Recorregut virtual 360/VR' },
];

async function trobaOCreaTema(classroom, nom) {
  const res = await ambReintents(
    () => classroom.courses.topics.list({ courseId: COURSE_ID, pageSize: 100 }),
    'llistar temes');
  const topics = res.data.topic || [];
  const found = topics.find(tp => tp.name === nom);
  if (found) return found.topicId;
  const created = await ambReintents(
    () => classroom.courses.topics.create({ courseId: COURSE_ID, requestBody: { name: nom } }),
    `crear tema "${nom}"`);
  return created.data.topicId;
}

async function main() {
  const auth = await getAuthClient();
  const classroom = google.classroom({ version: 'v1', auth });

  for (const u of UNITATS) {
    const nom = `${u.codi} · ${u.titol}`;
    console.log(`\n=== ${nom} ===`);

    const topicId = await trobaOCreaTema(classroom, nom);
    console.log(`✅ Tema: "${nom}"`);

    const existent = await trobaTascaPerTitol(classroom, nom);
    if (existent) {
      console.log(`⏭️ Tasca ja existent (${existent.state}): ${existent.alternateLink}`);
      continue;
    }

    const base = `${WEB_BASE}/${u.assignatura}/${u.slug}`;
    const trimestre = UNITAT_TRIMESTRE[u.codi];
    const categoria = GRADE_CATEGORIES[trimestre]?.id;

    console.log('🚀 Creant la tasca (DRAFT, sense punts)...');
    const res = await ambReintents(() => classroom.courses.courseWork.create({
      courseId: COURSE_ID,
      requestBody: {
        title: nom,
        description: `Fitxa d'alumnat de la unitat ${u.codi} («${u.titol}»). `
          + 'Avaluació qualitativa (diari + observació): aquesta tasca dona accés '
          + 'digital a la fitxa, no recull lliurament ni nota numèrica.',
        workType: 'ASSIGNMENT',
        state: 'DRAFT',
        topicId,
        ...(categoria ? { gradeCategory: { id: categoria } } : {}),
        materials: [
          { link: { url: `${base}/fitxa_alumnat.html`, title: `Fitxa d'alumnat ${u.codi}` } },
          { link: { url: `${base}/`, title: `Pàgina de la unitat ${u.codi}` } },
        ],
      },
    }), nom);
    console.log(`✅ id=${res.data.id} · ${res.data.alternateLink}`);
  }

  console.log('\nFet. Totes les tasques són en DRAFT: publica-les des del Classroom quan toqui.');
}

main().catch(e => { console.error('❌', e.message); process.exit(1); });
