# Repara i Roda 360 — Pla d'implementació Fase 1

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crear la programació didàctica completa (4 documents) i l'esquelet de carpetes de l'optativa «Repara i Roda 360» de 4t d'ESO, curs 2026-2027.

**Architecture:** Documents Markdown en català, seguint la plantilla i l'estil del projecte `Curs 2627 1 ESO Maker`. Repositori git nou. Spec font de veritat: `docs/superpowers/specs/2026-07-11-repara-i-roda-360-design.md`.

**Tech Stack:** Markdown, git, PowerShell (verificacions).

## Global Constraints

- Idioma dels documents: **català** (ortografia completa, com els projectes Maker i Robotica).
- Dades fixes del spec (copiar exactes): 4t ESO grup professionalitzador, ~10-12 alumnes, 1 docent, 3h/setmana (2h taller + 1h maker), 35 setmanes, **105 hores** (70 taller + 35 maker), 10 SA (SA0-SA9), suma de setmanes 2+2+3+3+4+3+4+3+3+8 = 35.
- Ponderacions d'avaluació: C6 35% · C3 25% · C8 25% · C5 15%.
- Marc normatiu: Decret 175/2022. **No inventar text oficial**: el redactat de CE oficials i competències clau s'adapta de `Curs 2627 1 ESO Maker\Programació didàctica\Mapatge_competencial_oficial.md` i `...\Normativa\Marc_normatiu_curricular.md` (llegir-los abans de redactar la Tasca 4).
- Trimestres orientatius: T1 = SA0-SA4 · T2 = SA4-SA7 · T3 = SA8-SA9.
- Sessió tipus: acollida 10' → demostració guiada 20' → pràctica guiada 30' → microrepte/pausa activa 10' → pràctica autònoma 25' → tancament 5'.
- Commits en català, missatge curt tipus `feat: programació didàctica base`.

---

### Task 1: Repositori git i esquelet de carpetes

**Files:**
- Create: `.gitignore`, `README.md`
- Create (carpetes amb `.gitkeep`): `Classes\SA0` … `Classes\SA9`, `Avaluació`, `Normativa`, `Memòria de treball`, `Programació didàctica`

**Interfaces:**
- Produces: repo git inicialitzat; carpeta `Programació didàctica\` on les tasques 2-5 creen documents.

- [ ] **Step 1: git init + .gitignore**

```powershell
git init
```

`.gitignore` (copiar del Maker si existeix; si no, mínim):

```
~$*
*.tmp
Thumbs.db
desktop.ini
```

- [ ] **Step 2: README.md**

Contingut: títol «Repara i Roda 360 — Optativa 4t ESO · Curs 2026-2027», un paràgraf de descripció (taller de bicicletes 2h + aula maker 1h, grup professionalitzador, ABP+ApS, certificat Mecànic/a Júnior), mapa de carpetes (el del §8 del spec), enllaç al spec i al pla.

- [ ] **Step 3: Esquelet de carpetes**

```powershell
$dirs = @('Programació didàctica','Avaluació','Normativa','Memòria de treball') + (0..9 | ForEach-Object { "Classes\SA$_" })
foreach ($d in $dirs) { New-Item -ItemType Directory -Force $d | Out-Null; New-Item -ItemType File -Force "$d\.gitkeep" | Out-Null }
```

- [ ] **Step 4: Verificar**

Run: `git status --short` — han d'aparèixer README, .gitignore, spec, pla i els .gitkeep. `(Get-ChildItem Classes -Directory).Count` ha de donar 10.

- [ ] **Step 5: Commit**

```powershell
git add -A
git commit -m "feat: esquelet del projecte Repara i Roda 360 + spec i pla"
```

---

### Task 2: Programacio_didactica_ReparaIRoda_4ESO.md

**Files:**
- Create: `Programació didàctica\Programacio_didactica_ReparaIRoda_4ESO.md`
- Referència d'estil: `C:\Users\briera2\Documents\Curs 2627 1 ESO Maker\Programació didàctica\Programacio_didactica_AulaMaker_1ESO.md` (llegir-la sencera abans de redactar)

**Interfaces:**
- Consumes: spec §1-§7.
- Produces: document mestre; les CE pròpies que s'hi defineixin (CE1-CE6, vegeu Step 1) les reutilitzen les tasques 3 i 4 amb noms idèntics.

- [ ] **Step 1: Redactar el document amb les 12 seccions de la plantilla Maker**

1. **Introducció i justificació** — perfil del grup professionalitzador (desmotivació acadèmica, aprenentatge pràctic i funcional), la bici com a fil narratiu únic taller+maker, ApS amb bicis de donacions, adaptar del §2 del borrador (spec §9).
2. **Marc normatiu** — Decret 175/2022, optativa de 4t amb competències triades de diverses matèries; ancoratge: CE de Tecnologia de 4t + transversals C3/C5/C6/C8 (spec §2).
3. **Objectius de la matèria** — adaptar els 5 objectius generals del borrador (habilitats tècniques, responsabilitat/cooperació, mobilitat sostenible, autoestima, transversals).
4. **Competències específiques pròpies i criteris d'avaluació** — definir 6 CE pròpies amb 2-3 criteris cadascuna:
   - CE1. Diagnosticar i reparar sistemes mecànics de la bicicleta amb eines adequades i de manera segura.
   - CE2. Executar rutines de manteniment preventiu seguint protocols pautats.
   - CE3. Dissenyar i fabricar peces i eines auxiliars amb tecnologies maker (làser, 3D) al servei del taller.
   - CE4. Documentar el treball tècnic (diari setmanal en paper, captura 360, memòria digital).
   - CE5. Circular i actuar amb seguretat i responsabilitat viària en entorns urbans reals.
   - CE6. Cooperar en equip amb rols rotatius i contribuir a la comunitat (ApS).
5. **Sabers bàsics** — agrupats per blocs: mecànica de la bici (anatomia, rodes, frens, transmissió, punts de contacte), fabricació digital (2D làser, 3D FDM, captura 360/VR), seguretat i salut (taller, viària), mobilitat sostenible i ciutadania.
6. **Metodologia** — ABP+ApS, sessió tipus fixa (Global Constraints), rols rotatius (mecànic, ajudant, encarregat d'eines, supervisor), subapartat DUA (pictogrames, fitxes plastificades passos numerats, llenguatge segmentat, ritmes flexibles, reforç positiu).
7. **Temporització anual (visió de conjunt)** — taula de 10 SA del spec §4 (copiar exacta, amb columnes SA/Títol/Setm./Taller/Maker) + trimestres orientatius.
8. **Avaluació i qualificació** — taula de ponderacions del spec §7 (exacta), instruments (diari setmanal, rúbriques d'observació, carnet d'eines/màquina, microprojectes, exposició final), sense exàmens, recuperació per millora contínua, autoavaluació i coavaluació trimestrals.
9. **Atenció a la diversitat** — grup professionalitzador com a destinatari primari: mesures universals (sessió predictible, DUA) + addicionals (segmentació de tasques, temps flexible, suport visual); coordinació amb tutoria i orientació.
10. **Continguts transversals i ODS** — ODS 3 (salut), 11 (ciutats sostenibles), 12 (consum responsable, reutilització de bicis), 13 (clima); perspectiva de gènere al taller.
11. **Recursos i materials** — taller de bicis (eines, recanvis, bicis donades, suports de treball), aula maker (làser, impressores 3D, càmera 360, ulleres VR), llibre de manteniment (Recursos), fitxes visuals plastificades.
12. **Avaluació de la pràctica docent** — indicadors senzills + diari docent de sessions (model Maker).

Capçalera del document: títol + subtítol «Optativa de 4t d'ESO · Curs 2026-2027 · 3 hores setmanals (2h taller + 1h aula maker) · anual · 105 hores».

- [ ] **Step 2: Verificar coherència**

Comprovar dins el document: 105 hores, 35 setmanes, ponderacions 35/25/25/15 sumen 100, 10 SA a la taula, els noms CE1-CE6 coincideixen amb el Step 1.

- [ ] **Step 3: Commit**

```powershell
git add "Programació didàctica/Programacio_didactica_ReparaIRoda_4ESO.md"
git commit -m "feat: programació didàctica Repara i Roda 360 4t ESO"
```

---

### Task 3: Temporitzacio_anual.md

**Files:**
- Create: `Programació didàctica\Temporitzacio_anual.md`
- Referència d'estil: `C:\Users\briera2\Documents\Curs 2627 1 ESO Maker\Programació didàctica\Temporitzacio_anual.md` (llegir abans)

**Interfaces:**
- Consumes: taula SA del spec §4; noms CE1-CE6 de la Tasca 2.

- [ ] **Step 1: Redactar**

Contingut:
1. Taula resum per trimestres (T1 setmanes 1-12: SA0-SA4 · T2 setmanes 13-24: SA4-SA7 · T3 setmanes 25-35: SA8-SA9), amb hores per trimestre (12×3=36h, 12×3=36h, 11×3=33h; total 105h).
2. Taula setmana a setmana (35 files): columnes Setmana / SA / Taller (2h) / Maker (1h). Desglossar cada SA en continguts setmanals concrets. Exemple del format (setmanes 1-2, SA0):

| Setm. | SA | Taller (2h) | Maker (1h) |
|---|---|---|---|
| 1 | SA0 | Acollida, presentació del curs, normes del taller | Presentació aula maker, normes de seguretat làser/3D |
| 2 | SA0 | Gimcana d'eines i seguretat, avaluació inicial pràctica | Carnet de màquina: prova pràctica |

3. Secció «Sortides del 3r trimestre»: 8 setmanes de SA9 amb sortides urbanes setmanals dins les 2h de taller; cicle preparació (visionat VR de la ruta) → execució (sortida amb captura 360) → reflexió (diari); última setmana: exposició pública amb estació VR, certificat, donació ApS.
4. Nota de flexibilitat: calendari orientatiu, ajustable segons festius i ritme del grup.

- [ ] **Step 2: Verificar**

Run: `(Select-String -Path "Programació didàctica/Temporitzacio_anual.md" -Pattern '^\| \d+ \|').Count`
Expected: `35` (una fila per setmana).

- [ ] **Step 3: Commit**

```powershell
git add "Programació didàctica/Temporitzacio_anual.md"
git commit -m "feat: temporització anual 35 setmanes"
```

---

### Task 4: Mapatge_competencial_oficial.md

**Files:**
- Create: `Programació didàctica\Mapatge_competencial_oficial.md`
- Llegir abans (fonts del redactat oficial, NO inventar): `C:\Users\briera2\Documents\Curs 2627 1 ESO Maker\Programació didàctica\Mapatge_competencial_oficial.md` i `C:\Users\briera2\Documents\Curs 2627 1 ESO Maker\Normativa\Marc_normatiu_curricular.md`

**Interfaces:**
- Consumes: CE1-CE6 pròpies de la Tasca 2; ponderacions C3/C5/C6/C8 del spec §7.

- [ ] **Step 1: Redactar**

Seccions (mirall de l'estructura Maker):
1. Fonts oficials (Decret 175/2022; naturalesa de les optatives de 4t: el centre pot triar competències de diverses matèries).
2. CE oficials de referència de *Tecnologia* de 4t (redactat adaptat de les fonts Maker; si la font de 1r-3r «Tecnologia i Digitalització» difereix de la matèria de 4t, indicar-ho honestament com fa la secció «Cobertura i límits» del Maker).
3. Mapatge CE pròpia (CE1-CE6) ↔ CE oficial + competències transversals C3/C5/C6/C8, amb taula SA per SA: quines CE treballa cada SA0-SA9 i amb quin instrument s'avalua.
4. Contribució a les competències clau del perfil de sortida (LOMLOE).
5. Secció «Cobertura i límits (per a la inspecció)»: què cobreix bé el projecte i què no.
6. Nota per a l'aprovació de centre.

- [ ] **Step 2: Verificar**

Cada CE1-CE6 apareix almenys un cop al mapatge; cada SA0-SA9 té almenys una CE assignada; ponderacions coincideixen amb la programació.

- [ ] **Step 3: Commit**

```powershell
git add "Programació didàctica/Mapatge_competencial_oficial.md"
git commit -m "feat: mapatge competencial oficial Decret 175/2022"
```

---

### Task 5: Diari_setmanal_paper.md

**Files:**
- Create: `Programació didàctica\Diari_setmanal_paper.md`
- Referència: `C:\Users\briera2\Documents\Curs 2627 1 ESO Maker\Avaluació\Diari_de_taller.md` (llegir abans) i extreure `Recursos\fitxa taller bicicleta.docx` si cal (script d'extracció ja al scratchpad)

**Interfaces:**
- Consumes: spec §6 (full únic dues cares, cara A taller / cara B maker).

- [ ] **Step 1: Redactar**

Contingut:
1. Propòsit i ús (s'omple al tancament de sessió, dossier personal, instrument de C3 25%).
2. Disseny de la fitxa — maqueta en Markdown de les dues cares:
   - **Cara A (taller):** data i setmana · SA i tasca de la setmana · «Què he fet avui» (3 línies pautades) · eines usades (checklist amb icones) · passos seguits (numerats) · dificultats i com les he resolt · esquema/foto (requadre) · semàfor d'autoavaluació (🟢🟡🔴) · rol de la setmana.
   - **Cara B (maker):** què he dissenyat/fabricat · màquina usada (làser/3D/360, checklist) · croquis o captura (requadre) · resultat (funciona? cal repetir?) · una cosa que he après.
3. Adaptacions DUA: pictogrames als encapçalaments, camps amb línies pautades, versió amb menys text per a qui ho necessiti.
4. Pla de producció: impressió per trimestres (model `diari_taller_T1/T2/T3` del Maker, fase web); nota que el format es refinarà amb l'alumnat durant el curs.

- [ ] **Step 2: Verificar**

Les dues cares hi són; els camps cobreixen el que demana el spec §6 (què he fet, eines, passos, dificultats, foto/esquema | disseny, màquina, resultat).

- [ ] **Step 3: Commit**

```powershell
git add "Programació didàctica/Diari_setmanal_paper.md"
git commit -m "feat: disseny del diari setmanal en paper"
```

---

### Task 6: Revisió creuada final

**Files:**
- Modify (si cal): els 4 documents de `Programació didàctica\` + `README.md`

- [ ] **Step 1: Comprovacions creuades**

Entre els 4 documents: mateixes hores (105 = 70+35), mateixes setmanes (35), mateixa taula SA (títols i setmanes idèntics), mateixes ponderacions (35/25/25/15), mateixos noms CE1-CE6, sessió tipus idèntica. Corregir desviacions.

Run: `Select-String -Path "Programació didàctica/*.md" -Pattern '105|35 setmanes' | Select-Object Filename, LineNumber, Line`

- [ ] **Step 2: Commit final**

```powershell
git add -A
git commit -m "fix: coherència creuada documents fase 1"
```

(Si no hi ha res a corregir, ometre el commit.)
