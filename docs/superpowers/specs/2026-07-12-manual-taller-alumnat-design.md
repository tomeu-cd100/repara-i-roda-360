# Manual de taller per a l'alumnat (PDF)

**Data:** 2026-07-12
**Projecte:** Repara i Roda 360 — optativa anual 4t ESO (grup professionalitzador, NEE)
**Abast:** nou material imprimible per a l'**hora de bicicletes**. No toca les unitats ni la web
existent més enllà d'afegir-hi l'enllaç de descàrrega.

## 1. Problema

L'alumnat no té cap referència ràpida de com fer les tasques bàsiques de taller que el docent
els ensenya. En un grup que parteix de zero i amb NEE, cal un **manual visual i textual**,
consultable mentre treballen, amb passos curts i predictibles.

## 2. Objectius

- Un **manual PDF A4** (~12 pàgines), una tasca per full, per plastificar/arxivar a cada estació.
- Llenguatge adaptat a NEE: frases imperatives curtes numerades, lletra gran, pictogrames,
  avisos ⚠️ i criteri d'èxit ✅ sempre al mateix lloc (estructura predictible).
- Il·lustració **100 % original** (esquemes vectorials dibuixats amb reportlab): sense fotos ni
  imatges amb drets d'autor. Imprimeix bé en blanc i negre.
- Reutilitzar l'estil de casa dels scripts reportlab existents (paleta, capçaleres, helpers).

## 3. Decisions fixades (brainstorming 2026-07-12)

- **Abast:** guia essencial de 9 tasques (una fitxa cadascuna) + portada + pàgina d'eines i
  seguretat + contraportada.
- **Visual:** dibuixos vectorials propis + pictogrames (esquemàtics, no realistes).
- **Format:** A4 vertical, 1 tasca per full.
- **Branca:** es fa a `remodelacio-maker` (tot pendent de push conjunt).

## 4. Contingut (ordre de pàgines)

1. **Portada** — títol «El teu manual ràpid de taller», silueta de bici, subtítol, curs.
2. **Eines i seguretat** — eines bàsiques (pictograma + nom), recordatori del carnet de màquina
   i normes de seguretat clau.
3. **M-check de seguretat** (ref. B2)
4. **Neteja i lubricació** (B2)
5. **Treure i posar la roda** (B3)
6. **Reparar una punxada** (B3)
7. **Frens de sabata** (B4)
8. **Frens de disc** (B4)
9. **Cadena: desgast i unió** (B5)
10. **Canvi posterior (topalls H/L)** (B6)
11. **Seient i manillar** (B7)
12. **Contraportada** — «semàfor» de com deixar la bici (verd/groc/vermell) + on demanar ajuda.

## 5. Plantilla de cada fitxa de tasca

Estructura fixa (mateix ordre a totes, per predictibilitat NEE):

- **Capçalera:** número + icona + TÍTOL gran + (⏱ temps orientatiu · unitat Bx de referència).
- **🧰 Abans de començar:** eines necessàries (pictogrames) + comprovació de seguretat.
- **Esquema** vectorial de la tasca (columna dreta o requadre destacat).
- **Passos numerats:** frases imperatives curtes; els passos clau tenen un mini-esquema al costat.
- **⚠️ Compte:** 1–2 avisos (error típic o risc de seguretat).
- **✅ Com sé que està bé:** criteri d'èxit observable.

## 6. Esquemes per fitxa (vectorial, reportlab)

- **M-check:** silueta de bici amb recorregut numerat 1→6 (roda davantera → frens → direcció →
  seient → transmissió → roda posterior).
- **Neteja i lubricació:** llaç de cadena amb punts de goteig i fletxa «pedala enrere».
- **Treure/posar roda:** palanca de tancament ràpid (obert/tancat) i eix, amb fletxes de sentit.
- **Punxada:** secció del pneumàtic amb desmuntadors, pegat i vàlvula.
- **Frens de sabata:** pinça i sabata a la llanta, separació 2–3 mm i «toe-in».
- **Frens de disc:** disc i pinça, folgança de pastilla, avís de no tocar el disc.
- **Cadena:** regle/mesurador sobre la cadena (marques 0,5 % / 0,75 %) i baula ràpida.
- **Canvi posterior:** desviador amb els cargols **H** i **L** retolats i el sentit del tensor.
- **Seient i manillar:** alçada del seient (referència de cama) i brida de la potència, amb avís
  de no passar-se de força.

Els esquemes són funcions de dibuix independents (una per tasca) que reben el `canvas` i una
posició; així es poden provar i ajustar per separat.

## 7. Arquitectura tècnica

- **`scripts/genera_manual_taller.py`** (reportlab): un script autònom, com la resta de
  `scripts/genera_*.py`. Estructura:
  - Constants de paleta i helpers de dibuix (reutilitzats de l'estil de casa: capçalera
    arrodonida, línies, pictogrames, requadres).
  - Una llista de dades `TASQUES` (títol, icona, temps, unitat, eines, passos, avisos, criteri,
    funció d'esquema) — *content-as-data*, com `genera_sa_dobles.py`.
  - Un dibuixant genèric `fitxa(c, tasca)` que renderitza la plantilla de la §5.
  - Portada, pàgina d'eines/seguretat i contraportada com a funcions pròpies.
  - Sortida: `Recursos/Manual_taller_bicicletes.pdf`.
- **`build_web.py`:** estendre `copy_assets` perquè copiï `Recursos/Manual_taller_bicicletes.pdf`
  a la web, i afegir un **enllaç de descàrrega** destacat a l'**índex de Bicicletes**
  (`web/classes/bicicletes/index.html`), que és on l'alumnat entra a buscar el material.
- **Ubicació del PDF:** `Recursos/` (material d'alumnat, al costat de les altres plantilles).

## 8. Verificació

- `py -3.11 scripts/genera_manual_taller.py` genera el PDF sense errors.
- Recompte de pàgines amb pypdf = 12.
- Render de totes les pàgines a PNG amb pymupdf per revisar visualment que text i esquemes no se
  solapen ni es tallen.
- Revisió de **català** del contingut (constant del projecte: sense faltes ni castellanismes).
- `build_web.py` copia el PDF i l'enllaç resol (validació d'enllaços com a `Recursos/LLEGEIX-ME`).

## 9. Fora d'abast (YAGNI)

- No fotos reals ni marcs per enganxar-les (decisió: només vectorial).
- No codis QR als vídeos (es pot afegir més endavant si es vol).
- No es reescriuen les unitats de bici ni la seva avaluació; el manual només **resumeix** el que
  ja s'ensenya.
- No es tradueix a altres idiomes.

## 10. Criteris d'èxit

- PDF A4 de 12 pàgines, una tasca per full, amb la plantilla fixa de la §5.
- Cada fitxa té esquema vectorial original, passos curts, avís ⚠️ i criteri ✅.
- Llegible en blanc i negre i adaptat a NEE.
- Descarregable des de la web sense enllaços trencats.
- Català correcte.
