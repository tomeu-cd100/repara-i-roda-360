# Remodelació de l'aula maker per blocs (M0–M9)

**Data:** 2026-07-12
**Projecte:** Repara i Roda 360 — optativa anual 4t ESO (grup professionalitzador)
**Abast:** només l'hora de **maker** (M0–M9). L'hora de **bicicletes** (B0–B9) NO es toca.

## 1. Problema

Les unitats maker actuals (M0–M9) van néixer com a mirall setmanal de les de bicicletes
(cada M_x complementava el B_x de la mateixa setmana) i assumeixen coneixements de disseny
i fabricació que l'alumnat **no té**. El grup parteix de zero. Cal una progressió pròpia,
per blocs de tecnologia, que ensenyi cada eina des del no-res i que produeixi peces amb
sentit per al taller de bicicletes.

## 2. Objectius

- Reescriure les 10 unitats maker amb premissa **«no cal saber res abans: s'aprèn fent»**.
- Organitzar-les en **3 blocs** tecnològics seqüencials: 3D → làser → 360/VR.
- Mantenir el lligam **temàtic** amb la bici (les peces serveixen o decoren la bici),
  deixant el lligam setmanal estricte amb cada unitat de bicicletes.
- Respectar el límit de 35 h (1 h/setmana × 35 setmanes).

## 3. Decisions fixades (brainstorming 2026-07-12)

- **Estructura:** 3 blocs, es conserven els 10 espais M0–M9 re-temàtitzats i agrupats per
  bloc (mínim canvi a l'arquitectura web; es manté el paral·lelisme 10↔10 amb bicis).
- **360/VR:** bloc final de T3 «si queda temps» — flexible, es retalla o es fa parcial si
  el 3D o el làser s'allarguen.
- **Bicicletes:** intactes.
- **Constants del projecte que es mantenen:** sense rols rotatius de grup (treball en
  parella amb seguiment individual), avaluació qualitativa NA/AS/AN/AE sense exàmens,
  bloc «Com ho aprendràs avui» (demo → guiada → autònoma) a cada fitxa, vídeo verificat
  via oEmbed a cada unitat, drets d'autor (no baixar imatges/vídeos protegits; embed
  només via YouTube oficial).

## 4. Arc per blocs i calendari

1 h/setmana · 35 setmanes · 35 h. Trimestres aproximats: T1 = 3D, T2 = làser, T3 = 360.

### BLOC 3D — Tinkercad (T1, setmanes 1–17)

| Unitat | Setm. | Nom | Nucli |
|---|---|---|---|
| M0 | 1–2 | Benvinguda maker i seguretat | Conèixer làser i 3D; normes de màquines; **carnet de màquina** |
| M1 | 3–5 | Tinkercad des de zero | Registre (compte de classe), interfície, moure/girar/escalar, pla de treball, agrupar, **exportar STL** |
| M2 | 6–8 | Mesurar i dissenyar (el peu de rei) | Conceptes 3D (mides en mm, toleràncies) + **ús del peu de rei** per mesurar objectes reals i portar-los al disseny |
| M3 | 9–11 | Enginyeria inversa: la maneta de fre | Peça física real → **plànol 2D acotat** (a mà, amb peu de rei) → forma **3D a Tinkercad** → imprimir → provar encaix i iterar |
| M4 | 12–14 | Peces útils per a la bici (3D) | Cada parella tria una peça del catàleg, la dissenya, imprimeix i prova al taller |
| M5 | 15–17 | Peces decoratives temàtica bici (3D) | Objecte decoratiu propi (temàtica bici) dissenyat i imprès |

### BLOC LÀSER — Inkscape (T2, setmanes 18–27)

| Unitat | Setm. | Nom | Nucli |
|---|---|---|---|
| M6 | 18–21 | Inkscape al Chromebook | **Instal·lació** (Linux/Crostini; alternativa web de reserva), primers passos, treball en **mm**, **codis de color** (vermell = tall, negre = gravat, blau = marca), exportar per a la làser |
| M7 | 22–24 | Tallar peces útils | Placa identificativa, etiquetes-organitzador, regle de desgast de cadena, caixa-kit (MakerCase) |
| M8 | 25–27 | Peces decoratives i rètols | Siluetes/rètols del taller + preparació de material per a l'exposició |

### BLOC 360/VR — «si queda temps» (T3, setmanes 28–35)

| Unitat | Setm. | Nom | Nucli |
|---|---|---|---|
| M9 | 28–35 | Recorregut virtual 360/VR | **Suport de càmera 360** (imprès o tallat, per a manillar/casc) → captura a les sortides → muntatge del recorregut virtual → estació VR a l'exposició. Flexible segons temps |

## 5. Catàleg de peces (opcions; el docent i l'alumnat trien)

**3D útils per a la bici (M3/M4):**
maneta de fre (enginyeria inversa), tapa/final de puny del manillar (bar-end), clip
passacables / guia de cable de canvi, separador de pastilles de fre (transport), tapa de
vàlvula (Presta/Schrader), clip de suport de llum o reflectant, protector de beina
(chainstay), adaptador/guia per a la bomba.

**3D decoratives temàtica bici (M5):**
clauer «baula de cadena» (o troç de cadena real encapsulat en marc imprès), tapes de
vàlvula decoratives, finals de tub/maneta amb logotip, imant de nevera silueta de bici,
pin/medalló «Mecànic Júnior» per als certificats, marcador de pàgina silueta de bici.

**Làser (M7/M8):**
placa identificativa, etiquetes-organitzador, regle de desgast de cadena (SVG ja existents
a `Recursos/plantilles_svg/`), caixa-kit / classificadora (MakerCase), silueta de bici
decorativa de paret, rètols del taller, suport de mòbil/tauleta, posagots temàtics,
diplomes de fusta per a l'exposició.

**360 (M9):** suport de càmera de manillar, suport de casc, adaptador de rosca ¼".

## 6. Workflow d'enginyeria inversa (M3, detall)

1. El docent lliura una **maneta de fre física** a cada parella.
2. **Mesura amb peu de rei** les cotes clau (llargada, gruix, diàmetre del pivot, forats).
3. **Plànol 2D acotat** a mà (vista superior + lateral) amb les mides.
4. **Modelatge 3D a Tinkercad** a partir del plànol.
5. **Impressió** i **prova d'encaix** a la bici; **iteració** si cal ajustar toleràncies.

Aquest és el patró que després es reutilitza a M4 (altres peces útils).

## 7. Inkscape al Chromebook (M6, detall)

- Via principal: activar **Linux (Crostini)** a ChromeOS i instal·lar Inkscape
  (`sudo apt install inkscape`), documentat pas a pas amb captures a la fitxa.
- **Alternativa de reserva** si Crostini no està disponible: editor SVG web
  (p. ex. Boxy SVG / SVG-Edit) mantenint la mateixa convenció de colors.
- Convenció de colors de la làser: 🔴 `#FF0000` tall · ⚫ negre gravat · 🔵 `#0000FF` marca.

## 8. Vídeos

Es **reassignen** els vídeos ja verificats (oEmbed) als nous temes:

- Tinkercad → M1–M5 (`csvBRWfgf1I`, `xvt7D38CYFQ`, `IVxa96tfey8`; se'n poden repartir).
- Inkscape/làser/MakerCase → M6–M8 (`n-eA69q_Gn0`, `QkOJrQtdGmU`, `ZTTJj4GlKJQ`, `i7H9dgyfM1Q`).
- Captura + edició 360 → M9 (`1uRtvs1_V5w`, `EaZrXTpGSkI`).
- M0 manté el vídeo en **català** (impressió 3D, Ajuntament de Girona, `wQZB0LrQ9-s`).

Cal **buscar i verificar 1–2 vídeos nous**: (a) ús del **peu de rei** / enginyeria inversa
(M2/M3), (b) impressió d'una peça decorativa (M5). Tots en castellà o català, verificats via
oEmbed, embed `youtube-nocookie`.

## 9. Canvis tècnics

- **`scripts/genera_sa_dobles.py`**: reescriure el bloc de dades `MAKER` (llista de 10
  diccionaris) amb els nous continguts. Cada diccionari manté l'esquema actual (code,
  folder, name, setm, producte, compl, desc, repte, visible[], exit[], sabers[],
  sessions[], dua[], materials[], fitxa[], imprimibles?, video, aval[]). Afegir clau nova
  `bloc` (`"3D"` | `"Làser"` | `"360"`) per a l'etiqueta de bloc.
- **`build_web.py`**: mostrar l'**etiqueta de bloc** a les targetes i/o capçalera de les
  unitats maker, llegint la clau `bloc` del diccionari (propagada al md com a metadada o
  com a text a la capçalera de la unitat). Sense trencar la navegació pas a pas ni el mapa.
- **Carpetes**: els codis M0–M9 es conserven; només canvia el `folder`/nom si el títol
  canvia gaire. Cal netejar carpetes antigues òrfenes si es reanomenen (git rm).
- **Documents a actualitzar** (taules maker): `Programació didàctica/Temporitzacio_anual.md`,
  `Programació didàctica/Mapatge_competencial_oficial.md`, i les taules maker de PD §6/§7
  (`Programacio_didactica_ReparaIRoda_4ESO.md`).
- **Regenerar** md (genera_sa_dobles) i web (build_web); verificar embeds i enllaços.

## 10. Fora d'abast (YAGNI)

- No es toquen les unitats de bicicletes, ni l'avaluació base, ni la normativa (el carnet
  de màquina segueix vàlid).
- No es crea programari ni plantilles noves més enllà de les SVG ja existents (se'n poden
  afegir de puntuals si una unitat ho demana, però no és objectiu).
- No es descarreguen imatges/vídeos amb drets.

## 11. Criteris d'èxit

- Les 10 fitxes maker parteixen de zero i segueixen demo → guiada → autònoma.
- Progressió clara en 3 blocs amb calendari que suma 35 h.
- Cada unitat té producte concret i vídeo verificat.
- Web regenerada sense enllaços trencats; etiqueta de bloc visible.
- Documents de programació (temporització, mapatge, PD §6/§7) coherents amb la nova
  estructura maker.
