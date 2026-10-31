# CLAUDE.md — Curs Repara i Roda 4t ESO (Bicicletes + Maker)

Material docent en **català** (optativa 4t ESO: taller de bicis 2h + aula maker 1h, LOMLOE).
El markdown és la font única; `build_web.py` genera la web que GitHub Pages publica a cada
push a `master`.

## REGLA D'OR: contingut generat per dades

- **Les unitats (`Classes/**/B*.md`, `M*.md` i les seves `Fitxa_alumnat.md`) es GENEREN amb
  `scripts/genera_sa_dobles.py`. MAI les editis a mà**: edita les llistes de dades del script
  i torna'l a executar. Una edició manual desapareix a la propera regeneració.
- **Els PDF imprimibles es generen amb els `scripts/genera_*.py` (reportlab)**, un script per
  document. No editis PDFs; edita el script. Truc conegut: reportlab no renderitza emojis de
  color — usa formes vectorials (triangle + ✓ U+2713).
- **`web/` és artefacte generat** amb `build_web.py`; no s'edita a mà.

## Regles

- **Tot en català**, ortografia completa.
- **RGPD**: cap dada d'alumnat real al repo.
- **Binaris**: `.gitattributes` marca `*.pdf`/`*.png` com a binaris — mantén-ho en afegir tipus nous.
- Si canvies el títol o producte d'una unitat: actualitza també `Programació didàctica/`
  (temporització + mapatge competencial), la targeta de `build_web.py`
  (`BIKE_CARDS`/`MAKER_CARDS`) i les referències creuades d'altres unitats
  (`grep -ri "nom antic"`). No renomenis carpetes ni slugs.

## Convencions

- Unitats `B0..B9` (bicis) i `M0..M9` (maker) a `Classes/{Bicicletes,Maker}/XN_Nom_snake/`.
- Diari del docent a `Memòria de treball/Diari_docent_sessions.md` (s'escriu després de classe).
- Commits en català, tipus Conventional Commits.
- Metodologia de canvis grans: spec + plan a `docs/superpowers/` (SDD).
