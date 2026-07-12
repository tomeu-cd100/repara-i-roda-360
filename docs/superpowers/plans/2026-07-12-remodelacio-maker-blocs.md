# Remodelació de l'aula maker per blocs — Pla d'implementació

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reescriure les 10 unitats de l'aula maker (M0–M9) partint de zero coneixements, organitzades en 3 blocs (3D → làser → 360), dins el límit de 35 h.

**Architecture:** Contingut generat per dades: `scripts/genera_sa_dobles.py` conté la llista de diccionaris `MAKER`; en executar-lo escriu `Classes/Maker/<carpeta>/<CODI>.md` i `Fitxa_alumnat.md`. `build_web.py` converteix els md a HTML i pinta les targetes des de `MAKER_CARDS`. No hi ha framework de tests: la verificació és determinista (regenerar + `grep`/recompte + validació d'enllaços + render puntual).

**Tech Stack:** Python 3.11 (`py -3.11`), reportlab/pymupdf/pypdf/markdown ja instal·lats. Vídeos YouTube via `youtube-nocookie`, verificats amb l'endpoint oEmbed.

## Global Constraints

- Idioma del material: **català** ortogràficament correcte (sense paraules inventades).
- **Sense rols rotatius de grup**: treball individual o en **parella** (CA6.1 = parella).
- Avaluació **qualitativa NA/AS/AN/AE**, sense exàmens.
- Cada fitxa manté el bloc **«Com ho aprendràs avui»** (demo → guiada → autònoma) — ja el genera `fitxa_md`.
- Cada unitat té **un vídeo** verificat via oEmbed, embed `youtube-nocookie`.
- **Drets d'autor**: no baixar imatges/vídeos protegits; embed només via YouTube oficial. El `Recursos/Llibre Manteniment Bici/` no es publica (gitignored).
- **Bicicletes B0–B9 NO es toquen.**
- Esquema de cada diccionari maker (claus): `code, folder, name, setm, producte, compl, desc, repte, visible[], exit[], sabers[], sessions[(titol,[bullets])], dua[], materials[], fitxa[(titol,linia)], video(titol,id), aval[(ev,ins,cr)]`, opcional `imprimibles[(txt,fitxer)]`, i **nova** clau `bloc` (`"🧊 3D"` | `"✂️ Làser"` | `"🎥 360"`).
- Executar sempre amb `py -3.11` (el `python` per defecte és el d'Inkscape, sense pip).

## File Structure

- `scripts/genera_sa_dobles.py` — Modify: la llista `MAKER` (línies ~473–776) es reescriu sencera; `sa_md` guanya una fila de taula «Bloc».
- `build_web.py` — Modify: `MAKER_CARDS` (línies 70–81) noms/icones/trimestre-amb-bloc/carpetes.
- `Classes/Maker/*` — Delete carpetes antigues + Create noves (les crea el generador).
- `Programació didàctica/Temporitzacio_anual.md` — Modify: columna maker.
- `Programació didàctica/Mapatge_competencial_oficial.md` — Modify: taula maker.
- `Programació didàctica/Programacio_didactica_ReparaIRoda_4ESO.md` — Modify: taules maker §6/§7.

Mapa de carpetes (renom): M0_Benvinguda_maker (igual) · M1_Placa→**M1_Tinkercad** · M2_Organitzadors→**M2_Peu_de_rei** · M3_Kit_reparacio→**M3_Enginyeria_inversa** · M4_Peces_de_fre→**M4_Peces_utils** · M5_Mesurador→**M5_Decoratives** · M6_Classificadora→**M6_Inkscape** · M7_Confort→**M7_Tallar_utils** · M8_Suports_i_360→**M8_Retols_laser** · M9_Rutes_VR→**M9_Recorregut_360**.

Assignació de vídeos (verificats): M0 `wQZB0LrQ9-s` (català) · M1 `csvBRWfgf1I` · M2 **NOU peu de rei** · M3 `xvt7D38CYFQ` · M4 `IVxa96tfey8` · M5 **NOU impressió decorativa** · M6 `n-eA69q_Gn0` · M7 `ZTTJj4GlKJQ` · M8 `QkOJrQtdGmU` · M9 `1uRtvs1_V5w`.

---

### Task 1: Obtenir i verificar els 2 vídeos nous

**Files:** cap (tasca de recerca; produeix 2 IDs verificats).

**Interfaces:**
- Produeix: `VIDEO_M2` (id + títol, tema «peu de rei / calibre») i `VIDEO_M5` (id + títol, tema «impressió 3D d'un objecte decoratiu, p. ex. clauer»). Consumits per Task 3 i Task 4.

- [ ] **Step 1: Cercar candidats**

Executar dues cerques web:
- «tutorial peu de rei calibre com s'usa mesurar mil·límetres» (i variant en castellà «cómo usar un calibre pie de rey milímetros tutorial»).
- «impresión 3D llavero personalizado tutorial» (objecte decoratiu senzill).

- [ ] **Step 2: Verificar existència via oEmbed**

Per a cada ID candidat, verificar amb WebFetch:
`https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=<ID>&format=json`
Esperat: JSON amb `title` i `author_name` (no error). Descartar els que retornin error.

- [ ] **Step 3: Fixar l'assignació**

Escollir un vídeo per M2 (peu de rei) i un per M5 (decoratiu). Anotar `(titol, id)` de cadascun amb el sufix d'idioma «(en castellà)» o «(en català)». Aquests valors s'usen literalment als diccionaris de Task 3 i Task 4.

- [ ] **Step 4: Commit** — no aplica (cap fitxer). Continuar a Task 2.

---

### Task 2: Infra `bloc` + generador i targetes

**Files:**
- Modify: `scripts/genera_sa_dobles.py` (funció `sa_md`)
- Modify: `build_web.py` (`MAKER_CARDS`)

**Interfaces:**
- Produeix: fila «Bloc» a la unitat quan el diccionari té `bloc`; `MAKER_CARDS` amb noms/carpetes nous. Consumit per totes les tasques següents.

- [ ] **Step 1: Afegir la fila «Bloc» a `sa_md`**

A `scripts/genera_sa_dobles.py`, dins `sa_md`, després de la línia del Producte, afegir:

```python
    out.append(f"| **Producte** | {s['producte']} |")
    if s.get("bloc"):
        out.append(f"| **Bloc** | {s['bloc']} |")
    out.append("")
```

- [ ] **Step 2: Reescriure `MAKER_CARDS` a `build_web.py`**

Substituir el bloc `MAKER_CARDS = [...]` (línies 70–81) per:

```python
MAKER_CARDS = [
    ("M0", "Benvinguda maker", "🧊 3D · setm. 1-2", "🔒", "Maker/M0_Benvinguda_maker"),
    ("M1", "Tinkercad des de zero", "🧊 3D · setm. 3-5", "🧊", "Maker/M1_Tinkercad"),
    ("M2", "Mesurar amb el peu de rei", "🧊 3D · setm. 6-8", "📐", "Maker/M2_Peu_de_rei"),
    ("M3", "Enginyeria inversa: maneta", "🧊 3D · setm. 9-11", "🔧", "Maker/M3_Enginyeria_inversa"),
    ("M4", "Peces útils per a la bici", "🧊 3D · setm. 12-14", "🖨️", "Maker/M4_Peces_utils"),
    ("M5", "Peces decoratives", "🧊 3D · setm. 15-17", "✨", "Maker/M5_Decoratives"),
    ("M6", "Inkscape al Chromebook", "✂️ Làser · setm. 18-21", "🖥️", "Maker/M6_Inkscape"),
    ("M7", "Tallar peces útils", "✂️ Làser · setm. 22-24", "🧰", "Maker/M7_Tallar_utils"),
    ("M8", "Rètols i decoració", "✂️ Làser · setm. 25-27", "🪧", "Maker/M8_Retols_laser"),
    ("M9", "Recorregut virtual 360", "🎥 360 · setm. 28-35", "🥽", "Maker/M9_Recorregut_360"),
]
```

- [ ] **Step 3: Commit**

```bash
git add scripts/genera_sa_dobles.py build_web.py
git commit -m "feat: infra bloc maker (fila Bloc + MAKER_CARDS per blocs)"
```

---

### Task 3: Bloc 3D — reescriure M0–M5

**Files:**
- Modify: `scripts/genera_sa_dobles.py` (diccionaris M0–M5 dins `MAKER`)
- Delete: `Classes/Maker/M1_Placa`, `M2_Organitzadors`, `M3_Kit_reparacio`, `M4_Peces_de_fre`, `M5_Mesurador`
- Create (via generador): `Classes/Maker/M1_Tinkercad`, `M2_Peu_de_rei`, `M3_Enginyeria_inversa`, `M4_Peces_utils`, `M5_Decoratives`

**Interfaces:**
- Consumeix: `VIDEO_M2` de Task 1; infra `bloc` de Task 2.
- Produeix: 6 unitats del bloc 3D.

- [ ] **Step 1: Comprovar que a `Classes/Maker/` no hi ha fitxers no generats**

Run: `find "Classes/Maker" -type f ! -name "M?.md" ! -name "Fitxa_alumnat.md"`
Esperat: cap resultat (si n'hi ha, no esborrar aquells fitxers; avisar).

- [ ] **Step 2: Substituir els diccionaris M0–M5**

A `scripts/genera_sa_dobles.py`, dins la llista `MAKER`, substituir els diccionaris de M0 a M5 pels següents (M0 conserva codi/carpeta; M1–M5 canvien `folder` i `name`). Copiar literalment:

```python
 {"video": ("Vídeo càpsula: la impressió 3D (en català, Ajuntament de Girona)", "wQZB0LrQ9-s"),
  "bloc": "🧊 3D",
  "code": "M0", "folder": "M0_Benvinguda_maker", "name": "Benvinguda maker i seguretat",
  "setm": "1–2", "producte": "**Carnet de màquina** (làser i 3D)",
  "compl": "el taller de bicicletes (les peces que farem serviran per a les bicis)",
  "desc": "L'aula maker fabrica peces i eines reals per al taller de bicicletes. Aquest curs treballem en tres blocs: primer impressió 3D, després tall làser i, si hi ha temps, un recorregut 360. Primer de tot: conèixer l'aula i treballar-hi amb seguretat.",
  "repte": "Guanya't el carnet de màquina: demostra que saps operar la 3D i la làser amb seguretat.",
  "visible": ["Conèixer la impressora 3D i la làser i què fabricarem tot el curs.",
              "Saber les normes de seguretat de les màquines."],
  "exit": ["Sé què fabricarem: peces 3D, després peces a làser i, si hi ha temps, el 360.",
           "Tinc el carnet de màquina (nivell làser i nivell 3D)."],
  "sabers": ["L'aula maker: impressora 3D Bambu Lab P2S i làser xTool S1.",
             "Els tres blocs del curs: 3D, làser i 360.",
             "Seguretat de màquines: materials, ventilació, parts calentes."],
  "sessions": [("Setmana 1 — L'aula i el pla del curs",
                ["Què fabricarem: exemples de peces per a la bici (20').",
                 "Les màquines i les normes de seguretat; demostració (30').",
                 "Diari (cara B) (10')."]),
               ("Setmana 2 — Carnet de màquina",
                ["Repàs de seguretat (15').",
                 "Checkpoint del carnet de màquina (`Normativa/Carnet_de_maquina.md`) (35').",
                 "Diari (10')."])],
  "dua": ["Demostració física de les màquines.",
          "El checkpoint es supera fent (posar material, aturada d'emergència).",
          "Carnet 🔵 amb variant «guia» per a qui no operi."],
  "materials": ["Impressora 3D i làser (demostració).",
                "Imprimible: `Normativa/Passaport_alumne.pdf`."],
  "fitxa": [("La norma de seguretat més important de les màquines:", "________________"),
            ("Una peça que vull fabricar aquest curs:", "________________")],
  "imprimibles": [("Contracte d'aula i carnet de màquina (PDF)", "Contracte_carnet_maker.pdf"),
                  ("Diari setmanal (PDF)", "Diari_setmanal_paper.pdf")],
  "aval": [("Carnet de màquina", "Checkpoint pràctic", "CA1.4"),
           ("Seguretat a l'aula maker", "Observació", "CA1.4, CA6.1"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Tinkercad: primers passos de disseny 3D (en castellà)", "csvBRWfgf1I"),
  "bloc": "🧊 3D",
  "code": "M1", "folder": "M1_Tinkercad", "name": "Tinkercad des de zero", "setm": "3–5",
  "producte": "**Primer objecte 3D propi** (imprès)",
  "compl": "el taller de bicicletes (aviat dissenyaràs peces per a la bici)",
  "desc": "Aprens a fer servir Tinkercad des de zero: com s'hi entra, com és per dins i com fer el primer disseny en 3D.",
  "repte": "Dissenya el teu primer objecte 3D i imprimeix-lo.",
  "visible": ["Entrar a Tinkercad amb el compte de classe.",
              "Moure, girar i escalar formes al pla de treball.",
              "Exportar el disseny a STL per imprimir."],
  "exit": ["Sé entrar a Tinkercad i moure'm per la interfície.",
           "He fet un disseny senzill combinant formes.",
           "He exportat l'STL i s'ha imprès."],
  "sabers": ["Tinkercad: compte de classe, interfície, formes, forats, agrupar.",
             "Pla de treball i mides en mm.",
             "Exportació a STL i enviament a impressió."],
  "sessions": [("Setmana 3 — Entrar i moure's",
                ["Registre amb el codi de classe; tour de la interfície (20').",
                 "Arrossegar formes; moure, girar i escalar (30').", "Diari (10')."]),
               ("Setmana 4 — Primer disseny",
                ["Combinar formes plenes i forats; agrupar (30').",
                 "Disseny lliure senzill (p. ex. una placa amb la teva inicial) (20').", "Diari (10')."]),
               ("Setmana 5 — Imprimir",
                ["Exportar STL; com es prepara la impressió (25').",
                 "Impressió per tandes; observar la màquina (25').", "Diari (10')."])],
  "dua": ["Fitxa visual pas a pas de Tinkercad.",
          "Plantilla d'inici amb formes ja posades.",
          "Producte personal i immediat."],
  "materials": ["Chromebooks amb Tinkercad (web); impressora 3D; material d'impressió."],
  "fitxa": [("El meu usuari de Tinkercad:", "________________"),
            ("Què he dissenyat:", "________________")],
  "aval": [("Ús bàsic de Tinkercad", "Observació + criteris d'èxit", "CA3.1"),
           ("Primer objecte imprès", "El disseny imprès", "CA3.1, CA3.2"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("<TÍTOL VIDEO_M2 de Task 1>", "<ID VIDEO_M2 de Task 1>"),
  "bloc": "🧊 3D",
  "code": "M2", "folder": "M2_Peu_de_rei", "name": "Mesurar amb el peu de rei", "setm": "6–8",
  "producte": "**Peça senzilla** dissenyada a mida real",
  "compl": "el taller de bicicletes (mesuraràs peces reials de la bici)",
  "desc": "Per fabricar peces que encaixin cal mesurar bé. Aprens a fer servir el peu de rei i a passar les mides al disseny.",
  "repte": "Mesura un objecte real amb el peu de rei i reprodueix-lo a mida a Tinkercad.",
  "visible": ["Llegir mides amb el peu de rei (en mm).",
              "Dibuixar un plànol 2D senzill acotat.",
              "Reproduir les mides a Tinkercad."],
  "exit": ["Sé mesurar amb el peu de rei.",
           "He fet un plànol 2D amb les mides.",
           "He reproduït la peça a mida a Tinkercad."],
  "sabers": ["El peu de rei: parts i lectura en mm.",
             "Cotes bàsiques i toleràncies (l'encaix).",
             "Del plànol 2D al model 3D."],
  "sessions": [("Setmana 6 — El peu de rei",
                ["Com es llegeix el peu de rei; pràctica amb objectes (30').",
                 "Plànol 2D acotat d'un objecte senzill (20').", "Diari (10')."]),
               ("Setmana 7 — Al Tinkercad",
                ["Reproduir les mides al pla de treball (40').", "Diari (10' + revisió de mides)."]),
               ("Setmana 8 — Imprimir i comparar",
                ["Imprimir i comparar amb l'original amb el peu de rei (40').", "Diari (10')."])],
  "dua": ["Peu de rei digital si costa la lectura de l'escala.",
          "Plantilla de plànol acotat.",
          "Es valida comparant amb l'original (visual)."],
  "materials": ["Peus de rei; objectes de mostra; Chromebooks; impressora 3D."],
  "fitxa": [("La mida més gran que he mesurat:", "______ mm"),
            ("La meva peça encaixa amb l'original?", "sí / cal ajustar")],
  "aval": [("Lectura del peu de rei", "Observació", "CA3.1"),
           ("Peça a mida real", "Comparació amb l'original", "CA3.1, CA3.2"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Tinkercad: modelatge 3D de peces (en castellà)", "xvt7D38CYFQ"),
  "bloc": "🧊 3D",
  "code": "M3", "folder": "M3_Enginyeria_inversa", "name": "Enginyeria inversa: la maneta de fre",
  "setm": "9–11", "producte": "**Rèplica 3D d'una maneta de fre**",
  "compl": "el taller de bicicletes (la maneta és una peça real del fre)",
  "desc": "A partir d'una maneta de fre real, en fem el plànol i la reproduïm en 3D per imprimir-la.",
  "repte": "Copia una maneta de fre real: plànol 2D, model 3D i impressió que encaixi.",
  "visible": ["Mesurar la maneta amb el peu de rei.",
              "Fer-ne el plànol 2D acotat.",
              "Modelar-la a Tinkercad i imprimir-la."],
  "exit": ["He mesurat i dibuixat la maneta.",
           "L'he modelada a Tinkercad.",
           "L'he impresa i he provat l'encaix."],
  "sabers": ["Enginyeria inversa: de l'objecte al model.",
             "Cotes crítiques (pivot, forats).",
             "Iteració segons la prova d'encaix."],
  "sessions": [("Setmana 9 — Mesurar i dibuixar",
                ["El docent lliura una maneta; mesura amb el peu de rei (25').",
                 "Plànol 2D acotat (vista superior i lateral) (25').", "Diari (10')."]),
               ("Setmana 10 — Modelar",
                ["Model 3D a Tinkercad a partir del plànol (40').", "Diari (10' + revisió de mides)."]),
               ("Setmana 11 — Imprimir i ajustar",
                ["Impressió i prova d'encaix; iteració (40').", "Diari (10')."])],
  "dua": ["Plànol amb algunes cotes ja marcades per a qui ho necessiti.",
          "Es valida fent (prova d'encaix real).",
          "Treball en parella."],
  "materials": ["Manetes de fre reials; peus de rei; Chromebooks; impressora 3D."],
  "fitxa": [("La cota crítica de la maneta:", "______ mm"),
            ("Encaixa a la bici?", "sí / cal ajustar")],
  "aval": [("Plànol i model", "Criteris d'èxit + rúbrica", "CA3.1"),
           ("Impressió i encaix", "La peça provada", "CA3.2, CA3.3"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Tinkercad: modelatge i disseny 3D per a principiants (en castellà)", "IVxa96tfey8"),
  "bloc": "🧊 3D",
  "code": "M4", "folder": "M4_Peces_utils", "name": "Peces útils per a la bici (3D)", "setm": "12–14",
  "producte": "**Peça útil** impresa i provada al taller",
  "compl": "el taller de bicicletes (la peça ajuda en una reparació o millora)",
  "desc": "Cada parella tria una peça útil del catàleg, la dissenya i la prova a la bici.",
  "repte": "Fabrica una peça útil per a la bici i comprova que funciona.",
  "visible": ["Triar una peça del catàleg i mesurar-ne les mides.",
              "Dissenyar-la a Tinkercad.",
              "Provar-la al taller i millorar-la."],
  "exit": ["He triat i dissenyat una peça útil.",
           "L'he impresa.",
           "L'he provada a la bici i millorada si calia."],
  "sabers": ["Disseny de peces funcionals a mida.",
             "Tria segons la necessitat del taller.",
             "Prova i iteració."],
  "sessions": [("Setmana 12 — Tria i disseny",
                ["Triar del catàleg (tapa de puny, clip passacables, separador de pastilles, "
                 "tapa de vàlvula, clip de llum, protector de beina) i mesurar (30').",
                 "Disseny a Tinkercad (20').", "Diari (10')."]),
               ("Setmana 13 — Impressió i prova",
                ["Impressió i primera prova a la bici (40').", "Diari (10')."]),
               ("Setmana 14 — Millora",
                ["Ajust i reimpressió si cal; acabats (40').", "Diari (10')."])],
  "dua": ["Catàleg amb imatges i nivell de dificultat.",
          "Es valida fent (a la bici real).",
          "L'error és informació: es millora."],
  "materials": ["Chromebooks; impressora 3D; bicis del taller; peus de rei."],
  "fitxa": [("Quina peça he triat:", "________________"),
            ("Funciona a la bici?", "sí / cal millorar")],
  "aval": [("Peça útil fabricada", "Criteris d'èxit", "CA3.2"),
           ("Prova i millora", "Peça provada a la bici", "CA3.3"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("<TÍTOL VIDEO_M5 de Task 1>", "<ID VIDEO_M5 de Task 1>"),
  "bloc": "🧊 3D",
  "code": "M5", "folder": "M5_Decoratives", "name": "Peces decoratives temàtica bici (3D)", "setm": "15–17",
  "producte": "**Objecte decoratiu** propi (temàtica bici)",
  "compl": "el taller de bicicletes (temàtica ciclista; per a l'exposició i els certificats)",
  "desc": "Dissenyem objectes decoratius amb temàtica de bici per a l'exposició i els records del curs.",
  "repte": "Dissenya i imprimeix un objecte decoratiu amb temàtica de bici.",
  "visible": ["Triar un objecte decoratiu (clauer baula, tapa de vàlvula, imant silueta, pin «Mecànic Júnior», marcador).",
              "Dissenyar-lo a Tinkercad.",
              "Imprimir-lo i acabar-lo."],
  "exit": ["He triat i dissenyat un objecte decoratiu.",
           "L'he imprès.",
           "Té bon acabat per a l'exposició."],
  "sabers": ["Disseny 3D creatiu (estètica).",
             "Text i relleu a Tinkercad.",
             "Acabats."],
  "sessions": [("Setmana 15 — Idea i disseny",
                ["Triar l'objecte i dissenyar-lo (text/relleu) (40').", "Diari (10')."]),
               ("Setmana 16 — Impressió",
                ["Impressió per tandes (40').", "Diari (10')."]),
               ("Setmana 17 — Acabats",
                ["Neteja, poliment i preparació per a l'exposició (40').", "Diari (10')."])],
  "dua": ["Galeria d'exemples per inspirar-se.",
          "Plantilla amb el text ja posat.",
          "Producte personal (motivador)."],
  "materials": ["Chromebooks; impressora 3D; material d'acabats."],
  "fitxa": [("El meu objecte decoratiu:", "________________"),
            ("On el posaré / a qui el donaré:", "________________")],
  "aval": [("Objecte decoratiu", "Criteris d'èxit", "CA3.2"),
           ("Acabat i presentació", "L'objecte per a l'exposició", "CA4.2"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},
```

- [ ] **Step 3: Esborrar les carpetes maker antigues renombrades del bloc 3D**

```bash
git rm -r "Classes/Maker/M1_Placa" "Classes/Maker/M2_Organitzadors" "Classes/Maker/M3_Kit_reparacio" "Classes/Maker/M4_Peces_de_fre" "Classes/Maker/M5_Mesurador"
```

- [ ] **Step 4: Regenerar i verificar**

Run: `py -3.11 scripts/genera_sa_dobles.py`
Esperat: «Generades 10 SA de Bicicletes i 10 SA de Maker.»

Run: `ls Classes/Maker` → esperat que hi siguin `M0_Benvinguda_maker M1_Tinkercad M2_Peu_de_rei M3_Enginyeria_inversa M4_Peces_utils M5_Decoratives` (i encara les de làser/360 antigues, que es tracten a Task 4/5).

Run (embeds bloc 3D): `grep -l "youtube-nocookie" Classes/Maker/M0_Benvinguda_maker/Fitxa_alumnat.md Classes/Maker/M1_Tinkercad/Fitxa_alumnat.md Classes/Maker/M2_Peu_de_rei/Fitxa_alumnat.md Classes/Maker/M3_Enginyeria_inversa/Fitxa_alumnat.md Classes/Maker/M4_Peces_utils/Fitxa_alumnat.md Classes/Maker/M5_Decoratives/Fitxa_alumnat.md | wc -l`
Esperat: `6`.

Run (fila Bloc): `grep -c "**Bloc**" Classes/Maker/M1_Tinkercad/M1.md` → esperat `1`.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: bloc 3D maker M0-M5 (Tinkercad de zero, peu de rei, enginyeria inversa, peces utils i decoratives)"
```

---

### Task 4: Bloc Làser — reescriure M6–M8

**Files:**
- Modify: `scripts/genera_sa_dobles.py` (diccionaris M6–M8)
- Delete: `Classes/Maker/M6_Classificadora`, `M7_Confort` (M8 antic `M8_Suports_i_360` es tracta a Task 5)
- Create (via generador): `Classes/Maker/M6_Inkscape`, `M7_Tallar_utils`, `M8_Retols_laser`

**Interfaces:**
- Consumeix: infra `bloc` de Task 2.
- Produeix: 3 unitats del bloc làser.

- [ ] **Step 1: Substituir els diccionaris M6–M8**

A `scripts/genera_sa_dobles.py`, substituir els diccionaris M6, M7 i M8 per:

```python
 {"video": ("Preparar text per a tall/gravat làser amb Inkscape (en castellà)", "n-eA69q_Gn0"),
  "bloc": "✂️ Làser",
  "code": "M6", "folder": "M6_Inkscape", "name": "Inkscape al Chromebook", "setm": "18–21",
  "producte": "**Primer disseny 2D** preparat per a la làser",
  "compl": "el taller de bicicletes (aviat tallaràs peces per al taller)",
  "desc": "Comencem el bloc de làser: instal·lem Inkscape al Chromebook i aprenem a preparar un disseny per tallar.",
  "repte": "Prepara el teu primer disseny 2D amb els codis de color correctes per a la làser.",
  "visible": ["Tenir Inkscape funcionant al Chromebook (o l'alternativa web).",
              "Dibuixar formes i text en mm.",
              "Aplicar els codis de color (tall / gravat / marca)."],
  "exit": ["Tinc Inkscape al Chromebook o he usat l'alternativa web.",
           "He fet un disseny senzill en mm.",
           "He aplicat els codis de color correctes."],
  "sabers": ["Instal·lació d'Inkscape al Chromebook (Linux/Crostini) o editor SVG web de reserva.",
             "Inkscape: formes, text, mides en mm.",
             "Codis de color de la làser: vermell = tall, negre = gravat, blau = marca."],
  "sessions": [("Setmana 18 — Instal·lar",
                ["Activar Linux (Crostini) i instal·lar Inkscape; alternativa web si cal (40').", "Diari (10')."]),
               ("Setmana 19 — Primers passos",
                ["Interfície, formes, text i mides en mm (40').", "Diari (10')."]),
               ("Setmana 20 — Codis de color",
                ["Aplicar vermell/negre/blau a un disseny (40').", "Diari (10')."]),
               ("Setmana 21 — Preparar per tallar",
                ["Exportar/enviar a la làser; prova en material de mostra (40').", "Diari (10')."])],
  "dua": ["Guia il·lustrada d'instal·lació pas a pas.",
          "Alternativa web si Crostini no està disponible.",
          "Plantilles amb els colors ja definits (`Recursos/plantilles_svg/`)."],
  "materials": ["Chromebooks (Linux/Crostini) o editor SVG web; làser xTool S1; material de prova.",
                "Plantilles: `Recursos/plantilles_svg/`."],
  "fitxa": [("Inkscape instal·lat?", "sí / he usat l'alternativa web"),
            ("Els tres colors i què fan:", "________________")],
  "aval": [("Inkscape a punt", "Observació", "CA3.1"),
           ("Disseny amb codis de color", "Criteris d'èxit", "CA3.1"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Dissenyar una caixa amb encaix per a tall làser (en castellà)", "ZTTJj4GlKJQ"),
  "bloc": "✂️ Làser",
  "code": "M7", "folder": "M7_Tallar_utils", "name": "Tallar peces útils", "setm": "22–24",
  "producte": "**Peça útil** tallada a làser per al taller",
  "compl": "el taller de bicicletes (organitza i manté el taller)",
  "desc": "Tallem peces útils per al taller: plaques, etiquetes, el regle de desgast de cadena i la caixa-kit.",
  "repte": "Fabrica a làser una peça útil que el taller faci servir.",
  "visible": ["Triar una peça útil (placa, etiqueta, regle, caixa-kit).",
              "Preparar-ne el disseny amb els codis de color.",
              "Tallar-la i muntar-la."],
  "exit": ["He triat i preparat una peça útil.",
           "L'he tallada correctament.",
           "Ja s'usa al taller."],
  "sabers": ["Ús de les plantilles SVG (`Recursos/plantilles_svg/`).",
             "Caixes amb encaix amb MakerCase.",
             "Tall i muntatge."],
  "sessions": [("Setmana 22 — Triar i preparar",
                ["Triar la peça i obrir/adaptar la plantilla (40').", "Diari (10')."]),
               ("Setmana 23 — Tallar",
                ["Tall a làser per tandes (40').", "Diari (10')."]),
               ("Setmana 24 — Muntar",
                ["Muntatge i posada en ús al taller (40').", "Diari (10')."])],
  "dua": ["Plantilles ja fetes per començar (`Recursos/plantilles_svg/`).",
          "El que es fabrica queda a la vista al taller (reconeixement).",
          "Treball en parella."],
  "materials": ["Chromebooks amb Inkscape; làser; MakerCase (per a les caixes); material de fabricació."],
  "fitxa": [("Quina peça he tallat:", "________________"),
            ("On s'usa al taller:", "________________")],
  "aval": [("Peça útil tallada", "Criteris d'èxit", "CA3.2"),
           ("Ús al taller", "La peça en ús", "CA3.3"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Preparar dissenys per a tall làser amb Inkscape (en castellà)", "QkOJrQtdGmU"),
  "bloc": "✂️ Làser",
  "code": "M8", "folder": "M8_Retols_laser", "name": "Rètols i decoració a làser", "setm": "25–27",
  "producte": "**Rètols i decoració** per al taller i l'exposició",
  "compl": "el taller de bicicletes (retolació del taller i material d'exposició)",
  "desc": "Tallem i gravem rètols, siluetes i decoració per al taller i per a l'exposició final.",
  "repte": "Fabrica a làser un rètol o una decoració per al taller o l'exposició.",
  "visible": ["Dissenyar un rètol o una silueta amb text/gravat.",
              "Tallar-lo i gravar-lo.",
              "Preparar-lo per a l'exposició."],
  "exit": ["He dissenyat un rètol o una decoració.",
           "L'he tallat i gravat.",
           "Està llest per a l'exposició o el taller."],
  "sabers": ["Combinació de tall i gravat en una mateixa peça.",
             "Tipografia i siluetes.",
             "Preparació de material d'exposició."],
  "sessions": [("Setmana 25 — Disseny",
                ["Disseny del rètol/silueta amb gravat i tall (40').", "Diari (10')."]),
               ("Setmana 26 — Fabricació",
                ["Tall i gravat per tandes (40').", "Diari (10')."]),
               ("Setmana 27 — Muntatge",
                ["Muntatge i preparació per a l'exposició (40').", "Diari (10')."])],
  "dua": ["Biblioteca de siluetes i tipografies.",
          "Es mostra al públic (reconeixement).",
          "Treball en parella."],
  "materials": ["Chromebooks amb Inkscape; làser; material (fusta/metacrilat); diplomes de fusta per a l'exposició."],
  "fitxa": [("Què he fet (rètol / silueta):", "________________"),
            ("On anirà:", "________________")],
  "aval": [("Rètol o decoració", "Criteris d'èxit", "CA3.2"),
           ("Material d'exposició", "El resultat exposat", "CA4.2, CA4.3"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},
```

- [ ] **Step 2: Esborrar carpetes antigues del bloc làser**

```bash
git rm -r "Classes/Maker/M6_Classificadora" "Classes/Maker/M7_Confort"
```

- [ ] **Step 3: Regenerar i verificar**

Run: `py -3.11 scripts/genera_sa_dobles.py` → esperat «Generades 10 SA … Maker.»
Run: `grep -l "youtube-nocookie" Classes/Maker/M6_Inkscape/Fitxa_alumnat.md Classes/Maker/M7_Tallar_utils/Fitxa_alumnat.md Classes/Maker/M8_Retols_laser/Fitxa_alumnat.md | wc -l` → esperat `3`.
Run: `grep -c "Làser" Classes/Maker/M6_Inkscape/M6.md` → esperat `>=1` (fila Bloc).

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: bloc laser maker M6-M8 (Inkscape al Chromebook, tallar peces utils, retols)"
```

---

### Task 5: Bloc 360 — reescriure M9 + neteja carpeta M8 antiga

**Files:**
- Modify: `scripts/genera_sa_dobles.py` (diccionari M9)
- Delete: `Classes/Maker/M8_Suports_i_360`, `Classes/Maker/M9_Rutes_VR`
- Create (via generador): `Classes/Maker/M9_Recorregut_360`

**Interfaces:**
- Consumeix: infra `bloc` de Task 2.
- Produeix: la unitat del bloc 360.

- [ ] **Step 1: Substituir el diccionari M9**

A `scripts/genera_sa_dobles.py`, substituir el diccionari M9 per:

```python
 {"video": ("Càmera 360 Insta360 X3: guia d'iniciació (en castellà)", "1uRtvs1_V5w"),
  "bloc": "🎥 360",
  "code": "M9", "folder": "M9_Recorregut_360", "name": "Recorregut virtual 360/VR", "setm": "28–35",
  "producte": "**Suport de càmera 360** + recorregut virtual + estació VR",
  "compl": "les sortides de bicicletes (B9) i l'exposició final",
  "desc": "Aquest bloc es fa **si queda temps** després del 3D i el làser. Fabriquem el suport de la càmera 360, gravem les sortides i muntem un recorregut virtual per a l'exposició.",
  "repte": "Fabrica el suport de la càmera, grava en 360 i munta un recorregut virtual.",
  "visible": ["Fabricar (imprès o tallat) un suport per a la càmera 360 (manillar o casc).",
              "Fer una captura 360 i visualitzar-la.",
              "Muntar un recorregut i preparar l'estació VR."],
  "exit": ["He fabricat el suport de la càmera 360.",
           "He fet una captura 360 i l'he visualitzada.",
           "He col·laborat en el recorregut i l'estació VR."],
  "sabers": ["Impressió/tall de suports funcionals (rosca ¼\").",
             "Captura 360 i visor VR (protocol).",
             "Muntatge d'un recorregut i comunicació a l'exposició."],
  "sessions": [("Setmanes 28–30 — Suport de la càmera",
                ["Disseny i fabricació del suport (manillar o casc).",
                 "Prova de subjecció a la bici o al casc.", "Diari."]),
               ("Setmanes 31–33 — Captura i muntatge",
                ["Captura 360 a les sortides; muntatge del recorregut.",
                 "Visionat VR (protocol `Normativa/Protocol_us_VR.md`).", "Diari."]),
               ("Setmanes 34–35 — Estació VR i exposició",
                ["Muntatge de l'estació VR de l'exposició.",
                 "Exposició oberta: els visitants «roden» les rutes. Tancament de curs."])],
  "dua": ["El visionat VR previ ajuda a anticipar la sortida (clau per a NEE).",
          "Cadascú aporta des del que se li dona millor.",
          "Producte que es mostra al públic."],
  "materials": ["Impressora 3D i/o làser; càmera 360; ulleres VR.",
                "`Normativa/Protocol_us_VR.md`, `Normativa/Autoritzacio_families_VR_360.md`."],
  "fitxa": [("El suport aguanta bé la càmera?", "sí / cal millorar-lo"),
            ("Què faré a l'estació VR de l'exposició:", "________________")],
  "aval": [("Suport de càmera 360", "Criteris d'èxit", "CA3.2"),
           ("Captura i recorregut", "El recorregut muntat", "CA4.2"),
           ("Estació VR a l'exposició", "Rúbrica de producte final", "CA4.3, CA6.3")]},
```

- [ ] **Step 2: Esborrar carpetes antigues M8/M9**

```bash
git rm -r "Classes/Maker/M8_Suports_i_360" "Classes/Maker/M9_Rutes_VR"
```

- [ ] **Step 3: Regenerar i verificar el conjunt sencer**

Run: `py -3.11 scripts/genera_sa_dobles.py`
Run: `ls Classes/Maker` → esperat exactament: `M0_Benvinguda_maker M1_Tinkercad M2_Peu_de_rei M3_Enginyeria_inversa M4_Peces_utils M5_Decoratives M6_Inkscape M7_Tallar_utils M8_Retols_laser M9_Recorregut_360` (cap carpeta antiga).
Run: `grep -rl "youtube-nocookie" Classes/Maker/*/Fitxa_alumnat.md | wc -l` → esperat `10`.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: bloc 360 maker M9 (recorregut virtual, si queda temps) + neteja carpetes antigues"
```

---

### Task 6: Documents de programació

**Files:**
- Modify: `Programació didàctica/Temporitzacio_anual.md`
- Modify: `Programació didàctica/Mapatge_competencial_oficial.md`
- Modify: `Programació didàctica/Programacio_didactica_ReparaIRoda_4ESO.md`

**Interfaces:**
- Consumeix: la nova estructura maker M0–M9.

- [ ] **Step 1: Localitzar les taules maker**

Run: `grep -n "M0\|M1\|M2\|M3\|M4\|M5\|M6\|M7\|M8\|M9\|Maker\|maker" "Programació didàctica/Temporitzacio_anual.md" "Programació didàctica/Mapatge_competencial_oficial.md" "Programació didàctica/Programacio_didactica_ReparaIRoda_4ESO.md"`
Identificar les files/columnes que anomenen les unitats maker antigues (Placa, Organitzadors, Kit de reparació, Peces de fre, Mesurador, Caixa classificadora, Peces de confort, Suports 360, Rutes VR).

- [ ] **Step 2: Actualitzar els noms i els blocs**

Reemplaçar els noms antics pels nous, respectant les setmanes noves:
M1 Tinkercad des de zero (3–5) · M2 Mesurar amb el peu de rei (6–8) · M3 Enginyeria inversa: la maneta de fre (9–11) · M4 Peces útils per a la bici (12–14) · M5 Peces decoratives (15–17) · M6 Inkscape al Chromebook (18–21) · M7 Tallar peces útils (22–24) · M8 Rètols i decoració (25–27) · M9 Recorregut virtual 360/VR (28–35). Afegir, on hi hagi capçalera de bloc o columna de fase, la indicació 🧊 3D (T1) / ✂️ Làser (T2) / 🎥 360 (T3, si queda temps).

- [ ] **Step 3: Verificar coherència**

Run: `grep -n "Organitzadors\|Kit de reparació\|Peces de fre\|Mesurador\|Classificadora\|Confort\|Rutes VR\|Suports i captura" "Programació didàctica/"*.md`
Esperat: cap resultat (cap nom antic maker viu).

- [ ] **Step 4: Commit**

```bash
git add "Programació didàctica"
git commit -m "docs: programacio (temporitzacio, mapatge, PD) coherent amb el maker per blocs"
```

---

### Task 7: Construcció web, verificació final i push

**Files:** cap canvi de codi; genera `web/` (ignorat) i puja.

- [ ] **Step 1: Construir la web**

Run: `py -3.11 build_web.py` → esperat «Web generada … pàgines de contingut.»

- [ ] **Step 2: Verificar embeds i targetes**

Run: `grep -rl "youtube-nocookie" web/classes/maker/*/fitxa_alumnat.html | wc -l` → esperat `10`.
Run: `grep -o "🧊 3D\|✂️ Làser\|🎥 360" web/classes/maker/index.html | sort | uniq -c` → esperat que apareguin els tres blocs.

- [ ] **Step 3: Verificar que no queden carpetes maker antigues a la web**

Run: `ls web/classes/maker` → esperat només les 10 slugs noves (m0_benvinguda_maker, m1_tinkercad, m2_peu_de_rei, m3_enginyeria_inversa, m4_peces_utils, m5_decoratives, m6_inkscape, m7_tallar_utils, m8_retols_laser, m9_recorregut_360).

- [ ] **Step 4: Validar enllaços interns de les fitxes maker**

Run un script que, per a cada `web/classes/maker/*/fitxa_alumnat.html`, comprovi que els `href` locals (no http) resolen a un fitxer existent sota `web/`. Esperat: cap enllaç trencat. (Reutilitzar el patró de validació ja usat per a `Recursos/LLEGEIX-ME.md`.)

- [ ] **Step 5: Push i confirmar CI**

```bash
git push
```
Comprovar que l'última execució del workflow de Pages acaba en verd i que la web mostra les noves unitats.

---

## Self-Review

**Spec coverage:**
- §4 blocs i calendari → Tasks 3/4/5 (M0–M9) + Task 6 (docs). ✓
- §5 catàleg de peces → integrat a M4 (útils) i M5 (decoratives) sessions/desc. ✓
- §6 enginyeria inversa → M3 sessions detallen mesura→plànol→model→impressió→iteració. ✓
- §7 Inkscape Chromebook → M6 sabers/sessions (Crostini + alternativa web) + DUA. ✓
- §8 vídeos → Task 1 (2 nous) + assignació a cada unitat. ✓
- §9 canvis tècnics → Task 2 (infra) + Tasks 3/4/5 (dades) + Task 6 (docs) + Task 7 (web). ✓
- §10 YAGNI: no es toquen bicis/avaluació/normativa. Cap tasca ho fa. ✓

**Placeholder scan:** els únics `<...>` són `VIDEO_M2`/`VIDEO_M5`, resolts a Task 1 abans d'usar-se a Task 3. No hi ha TODO/TBD.

**Type consistency:** totes les claus dels diccionaris coincideixen amb l'esquema que consumeix `sa_md`/`fitxa_md` (`code, folder, name, setm, producte, compl, desc, repte, visible, exit, sabers, sessions, dua, materials, fitxa, video, aval`, opcional `imprimibles`, nova `bloc`). Els `folder` nous coincideixen amb les carpetes de `MAKER_CARDS` de Task 2.
