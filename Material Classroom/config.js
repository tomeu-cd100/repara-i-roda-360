// Configuració ÚNICA del curs per a tots els scripts de Material Classroom.
// EN CANVIAR DE CURS (setembre): actualitzar aquí i enlloc més.
//  - COURSE_ID: id numèric del curs (courses.list o la URL de l'API, NO la
//    forma base64 de la URL /c/... del web).
//  - DRIVE_FOLDER_ID: carpeta de Drive on van tots els Forms del curs.
//    ⚠️ Pendent d'omplir: crear una carpeta a Drive per als Forms d'aquest
//    curs i enganxar-hi l'id (l'últim tram de la URL drive.google.com/drive/folders/...).
//  - GRADE_CATEGORIES: ids de les categories de nota. ⚠️ Es regeneren amb
//    cada curs nou de Classroom: obtenir-los amb `node estat_classroom.js`
//    (llista les categories del curs) abans d'assignar-los aquí.
//  - WEB_BASE: arrel del web publicat (canvia si es fa fork del repo).

export const COURSE_ID = '870550239423';
export const DRIVE_FOLDER_ID = '1oL8qbjmVXpXNmM6r3p5aAIb2acdSRrrS'; // "Repara i Roda 360 - Forms"
export const WEB_BASE = 'https://tomeu-cd100.github.io/repara-i-roda-360/classes';

export const GRADE_CATEGORIES = {
  T1: { id: '870548911202', name: 'T1' },
  T2: { id: '870548911203', name: 'T2' },
  T3: { id: '870548911204', name: 'T3' },
};

// unitat -> trimestre, derivat de Programació didàctica/Temporitzacio_anual.md
// (taula "Resum per trimestres"). B4/M4 són frontera T1/T2 (surten a les dues
// files de la taula); s'assignen a T1 perquè hi és on tanca el trimestre 1.
export const UNITAT_TRIMESTRE = {
  B0: 'T1', B1: 'T1', B2: 'T1', B3: 'T1', B4: 'T1',
  B5: 'T2', B6: 'T2', B7: 'T2',
  B8: 'T3', B9: 'T3',
  M0: 'T1', M1: 'T1', M2: 'T1', M3: 'T1', M4: 'T1',
  M5: 'T2', M6: 'T2', M7: 'T2',
  M8: 'T3', M9: 'T3',
};
