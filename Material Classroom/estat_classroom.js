/*
 * Estat global del Classroom del curs: la font de veritat és l'API, no els
 * resultats_*.json locals. Llista temes, tasques (títol, estat, punts, tema,
 * categoria) i les CATEGORIES DE NOTA amb els seus ids (necessaris a config.js
 * quan es crea el curs nou de setembre).
 *
 * Només lectura: no crea ni modifica res.
 *
 * Ús:
 *   node estat_classroom.js              # taula per pantalla
 *   node estat_classroom.js > estat.txt  # desar-ne una còpia
 * A més escriu estat_classroom.json (local, ignorat per git) amb el detall.
 */
import fs from 'fs';
import { google } from 'googleapis';
import { getAuthClient, ambReintents } from './_form_sa_lib.js';
import { COURSE_ID } from './config.js';

async function main() {
  const auth = await getAuthClient();
  const classroom = google.classroom({ version: 'v1', auth });

  const curs = await ambReintents(
    // Compte: courses.get vol el parametre "id" (courseWork/topics volen "courseId")
    () => classroom.courses.get({ id: COURSE_ID }), 'llegir curs');
  console.log(`\n=== ${curs.data.name} (${COURSE_ID}) · ${curs.data.courseState} ===`);

  const cats = curs.data.gradebookSettings?.gradeCategories || [];
  console.log('\n— Categories de nota (ids per a config.js) —');
  if (!cats.length) console.log('  (cap categoria definida)');
  for (const c of cats) console.log(`  ${c.name}: ${c.id} (pes ${c.weight ?? '-'})`);

  const topicsRes = await ambReintents(
    () => classroom.courses.topics.list({ courseId: COURSE_ID, pageSize: 100 }),
    'llistar temes');
  const temes = Object.fromEntries(
    (topicsRes.data.topic || []).map(t => [t.topicId, t.name]));

  const feines = [];
  let pageToken;
  do {
    const res = await ambReintents(
      () => classroom.courses.courseWork.list({
        courseId: COURSE_ID,
        courseWorkStates: ['PUBLISHED', 'DRAFT'],
        pageSize: 100,
        pageToken,
      }), 'llistar courseWork');
    feines.push(...(res.data.courseWork || []));
    pageToken = res.data.nextPageToken;
  } while (pageToken);

  console.log(`\n— Tasques (${feines.length}) —`);
  for (const w of feines) {
    const cat = cats.find(c => c.id === w.gradeCategory?.id)?.name || '-';
    console.log(`  [${w.state}] ${w.title} · ${w.maxPoints ?? '-'} punts · ` +
                `tema: ${temes[w.topicId] || '-'} · categoria: ${cat}`);
  }

  const estat = {
    consultat: new Date().toISOString(),
    curs: { id: COURSE_ID, nom: curs.data.name, estat: curs.data.courseState },
    categories: cats,
    temes,
    tasques: feines.map(w => ({
      id: w.id, titol: w.title, estat: w.state, punts: w.maxPoints ?? null,
      tema: temes[w.topicId] || null, categoria: w.gradeCategory?.id || null,
      enllac: w.alternateLink,
    })),
  };
  fs.writeFileSync('estat_classroom.json', JSON.stringify(estat, null, 2));
  console.log('\n💾 Detall desat a estat_classroom.json');
}

main().catch(e => { console.error('❌', e.message); process.exit(1); });
