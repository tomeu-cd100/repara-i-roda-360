# Manual de taller per a l'alumnat — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generar un manual PDF A4 de 12 pàgines, visual i adaptat a NEE, amb les 9 tasques bàsiques de taller de bicicletes, i fer-lo descarregable des de la web.

**Architecture:** Un script autònom `scripts/genera_manual_taller.py` (reportlab), amb el contingut com a dades (`TASQUES`), una plantilla de fitxa genèrica, funcions d'esquema vectorial per tasca, i pàgines especials (portada, eines/seguretat, contraportada). `build_web.py` copia el PDF i hi afegeix un enllaç.

**Tech Stack:** Python 3.11 (`py -3.11`), reportlab (generació), pypdf (recompte de pàgines), pymupdf/fitz (render PNG per revisió visual).

## Global Constraints

- Executar sempre amb `py -3.11` (el `python` per defecte és el d'Inkscape, sense pip).
- Català IMPECABLE: sense faltes, sense castellanismes, sense paraules inventades. Dígraf `ll` (lligam, llanta) ≠ ela geminada `l·l` (col·locar, allen no porta accent).
- Il·lustració 100 % original (dibuix vectorial reportlab). CAP foto ni imatge amb drets.
- Reutilitzar l'estil de casa (`scripts/genera_fitxa_sortida.py`): paleta INDIGO `#5b5bd6`, CIAN `#0e9aa1`, GRIS `#5a6079`, TINTA `#14172a`, LINIA `#c3c7d9`; fonts Helvetica; capçalera arrodonida.
- Sortida: `Recursos/Manual_taller_bicicletes.pdf`. 12 pàgines A4 vertical.
- Branca: `remodelacio-maker` (tot pendent de push conjunt).
- Mètode de tuning visual: després de cada canvi de dibuix, generar el PDF i renderitzar les pàgines a PNG amb pymupdf; ajustar coordenades fins que res se solapi ni es talli.

---

### Task 1: Esquelet del script, helpers d'estil i portada

**Files:**
- Create: `scripts/genera_manual_taller.py`

**Interfaces:**
- Produeix: helpers `pagina_nova(c)`, `capsalera_fitxa(c, num, icona, titol, temps, unitat)`, `blocs de dibuix` (`liniah`, `requadre`, `pictograma`), i `portada(c)`. Constants de paleta. `W, H, M`. Funció `main()` que crea el canvas i, de moment, només dibuixa la portada.

- [ ] **Step 1: Crear el fitxer amb capçalera, imports, paleta i helpers**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manual ràpid de taller de bicicletes per a l'alumnat (PDF A4, 12 pàgines).

Guia visual i textual de les 9 tasques bàsiques que el docent ensenya, adaptada
a un grup que parteix de zero (NEE): passos curts, pictogrames, avisos i criteri
d'èxit sempre al mateix lloc. Il·lustració vectorial original (sense drets).

Sortida: Recursos/Manual_taller_bicicletes.pdf
Ús:  py -3.11 scripts/genera_manual_taller.py   ·   Requereix: reportlab
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

AQUI = os.path.dirname(os.path.abspath(__file__))
SORTIDA = os.path.normpath(os.path.join(AQUI, "..", "Recursos", "Manual_taller_bicicletes.pdf"))
W, H = A4
M = 16 * mm
INDIGO = colors.HexColor("#5b5bd6")
CIAN = colors.HexColor("#0e9aa1")
GRIS = colors.HexColor("#5a6079")
TINTA = colors.HexColor("#14172a")
LINIA = colors.HexColor("#c3c7d9")
GROC = colors.HexColor("#e0a90b")
VERMELL = colors.HexColor("#d64545")
VERD = colors.HexColor("#2e9e5b")


def liniah(c, x, y, ample, color=LINIA, gruix=0.6):
    c.setStrokeColor(color)
    c.setLineWidth(gruix)
    c.line(x, y, x + ample, y)


def requadre(c, x, y, ample, alt, color=LINIA, fons=None, radi=3):
    if fons is not None:
        c.setFillColor(fons)
    c.setStrokeColor(color)
    c.setLineWidth(0.9)
    c.roundRect(x, y, ample, alt, radi, fill=(fons is not None), stroke=1)


def text_ajustat(c, x, y, text, font="Helvetica", mida=10.5, color=TINTA, ample_max=None, interlineat=5 * mm):
    """Escriu text amb ajust de línia simple per amplada màxima. Retorna la y final."""
    c.setFillColor(color)
    c.setFont(font, mida)
    if ample_max is None:
        c.drawString(x, y, text)
        return y - interlineat
    paraules = text.split()
    linia = ""
    for p in paraules:
        prova = (linia + " " + p).strip()
        if c.stringWidth(prova, font, mida) <= ample_max:
            linia = prova
        else:
            c.drawString(x, y, linia)
            y -= interlineat
            linia = p
    if linia:
        c.drawString(x, y, linia)
        y -= interlineat
    return y
```

- [ ] **Step 2: Afegir la capçalera de fitxa i la portada**

```python
def capsalera_fitxa(c, num, icona, titol, temps, unitat):
    """Barra superior de cada fitxa de tasca."""
    y = H - M - 12 * mm
    c.setFillColor(INDIGO)
    c.roundRect(M, y, W - 2 * M, 12 * mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(M + 5 * mm, y + 3.7 * mm, f"{num}. {icona}  {titol}")
    c.setFont("Helvetica", 8.5)
    c.drawRightString(W - M - 5 * mm, y + 3.7 * mm, f"{temps} · {unitat}")
    return y - 6 * mm  # y de partida del cos


def portada(c):
    c.setFillColor(INDIGO)
    c.rect(0, H - 95 * mm, W, 95 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(W / 2, H - 55 * mm, "El teu manual")
    c.drawCentredString(W / 2, H - 70 * mm, "ràpid de taller")
    c.setFont("Helvetica", 13)
    c.setFillColor(colors.HexColor("#dfe0fb"))
    c.drawCentredString(W / 2, H - 84 * mm, "Com fer les feines bàsiques de la bici, pas a pas")
    # silueta de bici simple (dos cercles + quadre)
    dibuixa_bici(c, W / 2, H - 150 * mm, escala=1.4, color=INDIGO)
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 10)
    c.drawCentredString(W / 2, 30 * mm, "Repara i Roda 360 · Taller de bicicletes · 4t ESO")
    c.drawCentredString(W / 2, 24 * mm, "Institut Consell de Cent")
    c.showPage()
```

- [ ] **Step 3: Afegir un dibuix de bici reutilitzable i el `main()` provisional**

```python
def dibuixa_bici(c, cx, cy, escala=1.0, color=TINTA, gruix=1.6):
    """Silueta lateral esquemàtica: dues rodes, quadre triangular, manillar i seient."""
    c.setStrokeColor(color)
    c.setLineWidth(gruix)
    r = 15 * mm * escala
    d = 34 * mm * escala  # distància entre eixos
    xr = cx - d / 2   # centre roda darrere
    xf = cx + d / 2   # centre roda davant
    c.circle(xr, cy, r, stroke=1, fill=0)
    c.circle(xf, cy, r, stroke=1, fill=0)
    # quadre
    ped = (cx - 2 * mm * escala, cy)           # eix pedaler
    seient = (cx - 6 * mm * escala, cy + r + 6 * mm * escala)
    manillar = (xf - 6 * mm * escala, cy + r + 7 * mm * escala)
    c.line(*ped, *seient)
    c.line(*ped, xr, cy)
    c.line(*seient, xr, cy)
    c.line(*seient, *manillar)
    c.line(*ped, *manillar)
    c.line(xf, cy, *manillar)
    # seient i manillar
    c.line(seient[0] - 4 * mm * escala, seient[1], seient[0] + 4 * mm * escala, seient[1])
    c.line(manillar[0] - 1 * mm * escala, manillar[1], manillar[0] + 6 * mm * escala, manillar[1])


def main():
    c = canvas.Canvas(SORTIDA, pagesize=A4)
    c.setTitle("Manual ràpid de taller de bicicletes")
    portada(c)
    c.save()
    print(f"Manual generat a {SORTIDA}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Generar i verificar la portada**

Run: `py -3.11 scripts/genera_manual_taller.py`
Expected: `Manual generat a ...Recursos/Manual_taller_bicicletes.pdf`

Run (recompte + render):
```bash
py -3.11 -c "import pypdf; print('pagines', len(pypdf.PdfReader(r'Recursos/Manual_taller_bicicletes.pdf').pages))"
py -3.11 -c "import fitz; d=fitz.open(r'Recursos/Manual_taller_bicicletes.pdf'); d[0].get_pixmap(dpi=110).save(r'.superpowers/sdd/manual_p1.png'); print('render ok')"
```
Expected: `pagines 1` i `render ok`. Obrir el PNG i comprovar que la portada es veu bé (títol, bici, peu), sense text tallat.

- [ ] **Step 5: Commit**

```bash
git add scripts/genera_manual_taller.py
git commit -m "feat: manual taller alumnat - esquelet, estil de casa i portada"
```

---

### Task 2: Dades de les 9 tasques, plantilla de fitxa i pàgines d'eines i contraportada

**Files:**
- Modify: `scripts/genera_manual_taller.py`

**Interfaces:**
- Consumeix: helpers de Task 1 (`capsalera_fitxa`, `requadre`, `text_ajustat`, `dibuixa_bici`, paleta).
- Produeix: llista `TASQUES` (9 dicts amb claus `num, icona, titol, temps, unitat, eines[list], passos[list], compte[str], criteri[str], esquema[callable|None]`), funció `fitxa(c, t)`, `pagina_eines(c)`, `contraportada(c)`. `main()` recorre portada → eines → 9 fitxes → contraportada.

- [ ] **Step 1: Afegir la llista `TASQUES` amb el contingut complet**

```python
TASQUES = [
    {"num": 1, "icona": "🔍", "titol": "M-check de seguretat", "temps": "⏱ 10 min", "unitat": "B2",
     "eines": ["Les mans", "Bomba"],
     "passos": [
        "Aixeca la bici i fes girar les dues rodes: han de girar rectes i sense fregar.",
        "Prem cada fre: la maneta no ha d'arribar al puny i la roda s'ha d'aturar.",
        "Agafa el manillar i mou-lo: la direcció ha de girar suau, sense joc.",
        "Prova el seient: ben fixat, no gira ni baixa.",
        "Mira la cadena i els pedals: nets, greixats i sense peces fluixes.",
        "Comprova la pressió de les dues rodes amb els dits: dures, no toves."],
     "compte": "Si algun punt falla, no facis servir la bici: marca-la i avisa.",
     "criteri": "Els 6 punts correctes = bici segura per rodar.",
     "esquema": None},

    {"num": 2, "icona": "🧽", "titol": "Neteja i lubricació", "temps": "⏱ 15 min", "unitat": "B2",
     "eines": ["Drap", "Raspall", "Desengreixant", "Oli de cadena"],
     "passos": [
        "Posa la bici al suport o de manera que la roda del darrere giri lliure.",
        "Amb el raspall i el desengreixant, neteja la cadena, els plats i els pinyons.",
        "Eixuga bé amb un drap fins que la cadena quedi neta i seca.",
        "Posa una gota d'oli a cada baula mentre pedales enrere a poc a poc.",
        "Deixa actuar l'oli un minut i eixuga l'oli que sobra amb el drap."],
     "compte": "No posis oli als discos ni a les llantes de fre: perdries frenada.",
     "criteri": "Cadena neta, greixada i sense oli degotant.",
     "esquema": None},

    {"num": 3, "icona": "🛞", "titol": "Treure i posar la roda", "temps": "⏱ 10 min", "unitat": "B3",
     "eines": ["Tancament ràpid", "Clau del 15 (si té femelles)"],
     "passos": [
        "Si és la roda del darrere, posa la cadena al pinyó més petit.",
        "Obre el fre (o afluixa'l) perquè el pneumàtic pugui passar.",
        "Obre la palanca de tancament ràpid (o afluixa les femelles).",
        "Treu la roda cap avall; al darrere, guia la cadena i el desviador.",
        "Per posar-la: encaixa l'eix al fons, tanca la palanca amb força justa i torna a tancar el fre."],
     "compte": "La palanca ha de quedar dura de tancar; si es tanca sola, no subjecta prou.",
     "criteri": "Roda centrada, ben subjecta i el fre torna a funcionar.",
     "esquema": None},

    {"num": 4, "icona": "🔧", "titol": "Reparar una punxada", "temps": "⏱ 20 min", "unitat": "B3",
     "eines": ["Desmuntadors", "Pegats o cambra nova", "Bomba"],
     "passos": [
        "Treu la roda i, amb els desmuntadors, treu la cambra de dins del pneumàtic.",
        "Infla una mica la cambra i busca per on surt l'aire (a l'oïda o amb aigua).",
        "Marca el forat, ratlla la zona i enganxa el pegat ben premut.",
        "Revisa l'interior del pneumàtic i treu allò que hagi punxat.",
        "Torna a muntar la cambra i el pneumàtic sense pinçar-la, i infla."],
     "compte": "Comprova sempre què ha punxat abans de tancar, o tornaràs a punxar.",
     "criteri": "La roda aguanta la pressió i no perd aire.",
     "esquema": None},

    {"num": 5, "icona": "🛑", "titol": "Frens de sabata", "temps": "⏱ 15 min", "unitat": "B4",
     "eines": ["Clau allen", "Tercera mà (opcional)"],
     "passos": [
        "Mira les sabates: si estan gastades més enllà de la marca, canvia-les.",
        "Afluixa el cargol de la sabata i col·loca-la centrada a la llanta (sense tocar el pneumàtic).",
        "Deixa una separació de 2 a 3 mm entre la sabata i la llanta.",
        "Dona una mica de «toe-in»: la punta del davant toca primer.",
        "Tensa el cable si la maneta va molt fluixa i prova de frenar."],
     "compte": "La sabata no ha de tocar mai el pneumàtic: el rebentaria.",
     "criteri": "Frena fort, no frega en repòs i la maneta no arriba al puny.",
     "esquema": None},

    {"num": 6, "icona": "⚙️", "titol": "Frens de disc", "temps": "⏱ 15 min", "unitat": "B4",
     "eines": ["Clau allen"],
     "passos": [
        "No toquis mai el disc amb els dits: el greix redueix la frenada.",
        "Mira el gruix de les pastilles; si són molt fines, canvia-les.",
        "Afluixa els cargols de la pinça i prem la maneta a fons.",
        "Amb la maneta premuda, torna a collar la pinça: així queda centrada.",
        "Deixa anar la maneta i comprova que el disc gira lliure, sense fregar."],
     "compte": "Si el disc frega o va tort, no forcis: avisa el docent.",
     "criteri": "Frena bé, el disc gira net i no frega.",
     "esquema": None},

    {"num": 7, "icona": "🔗", "titol": "Cadena: desgast i unió", "temps": "⏱ 15 min", "unitat": "B5",
     "eines": ["Mesurador de cadena", "Alicates de baula ràpida"],
     "passos": [
        "Posa el mesurador sobre la cadena: si entra fins a la marca de 0,75 %, està gastada.",
        "Si l'has de canviar, obre la baula ràpida amb els alicates (o el tronçador).",
        "Compta que la cadena nova tingui els mateixos baules que la vella.",
        "Passa la cadena pels plats i els pinyons seguint el desviador.",
        "Tanca la baula ràpida i estira fort perquè encaixi bé."],
     "compte": "Una cadena molt gastada desgasta plats i pinyons: no esperis massa a canviar-la.",
     "criteri": "La baula queda fixa i la cadena passa suau per tots els canvis.",
     "esquema": None},

    {"num": 8, "icona": "🔩", "titol": "Canvi posterior (topalls H i L)", "temps": "⏱ 20 min", "unitat": "B6",
     "eines": ["Clau allen", "Tornavís"],
     "passos": [
        "Posa la cadena al pinyó més petit i localitza el cargol marcat amb «H».",
        "Gira «H» fins que la roldana quedi alineada amb el pinyó petit.",
        "Posa la cadena al pinyó més gran i ajusta el cargol «L» igual, sense passar-te.",
        "Amb el tensor (barrilet), afina fins que canviï net cap amunt i cap avall.",
        "Prova tots els canvis pedalejant: han d'entrar suaus i sense saltar."],
     "compte": "«H» és el pinyó petit i «L» el pinyó gran. No forcis els topalls.",
     "criteri": "Canvia a tots els pinyons sense saltar ni fer soroll.",
     "esquema": None},

    {"num": 9, "icona": "🪑", "titol": "Seient i manillar", "temps": "⏱ 10 min", "unitat": "B7",
     "eines": ["Clau allen"],
     "passos": [
        "Alçada del seient: amb el taló al pedal a baix, la cama queda gairebé recta.",
        "Afluixa la brida, ajusta l'alçada i torna a collar amb força justa.",
        "El seient ha de quedar recte i horitzontal (o gairebé).",
        "Comprova que el manillar està alineat amb la roda del davant.",
        "Colla la potència en creu, poc a poc, sense passar-te de força."],
     "compte": "No passis la marca màxima de la tija del seient ni de la potència.",
     "criteri": "Seient a l'alçada bona, ferm, i manillar recte i ben collat.",
     "esquema": None},
]
```

- [ ] **Step 2: Afegir la plantilla `fitxa(c, t)`**

```python
def bloc_titol(c, x, y, text, color=CIAN):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y, text)
    return y - 6 * mm


def fitxa(c, t):
    """Renderitza una fitxa de tasca segons la plantilla fixa (§5 de l'spec)."""
    y0 = capsalera_fitxa(c, t["num"], t["icona"], t["titol"], t["temps"], t["unitat"])
    col_dreta_x = W - M - 62 * mm  # inici columna de l'esquema
    ample_esq = col_dreta_x - M - 6 * mm

    # --- Abans de començar (eines) ---
    y = bloc_titol(c, M, y0, "🧰 ABANS DE COMENÇAR")
    y = text_ajustat(c, M, y, "Eines: " + ", ".join(t["eines"]) + ".",
                     mida=10, ample_max=ample_esq, interlineat=5 * mm)
    y -= 2 * mm

    # --- Passos ---
    y = bloc_titol(c, M, y, "PASSOS")
    for i, pas in enumerate(t["passos"], 1):
        c.setFillColor(INDIGO)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M, y, f"{i}.")
        y = text_ajustat(c, M + 7 * mm, y, pas, mida=10.5, ample_max=ample_esq - 7 * mm,
                         interlineat=5 * mm)
        y -= 1.5 * mm

    # --- Esquema (columna dreta) ---
    requadre(c, col_dreta_x, 60 * mm, 62 * mm, H - M - 12 * mm - 6 * mm - 60 * mm,
             color=LINIA, fons=colors.HexColor("#f4f5fb"))
    if t["esquema"]:
        t["esquema"](c, col_dreta_x + 31 * mm, 60 * mm + (H - M - 78 * mm - 60 * mm) / 2 + 30 * mm)
    else:
        c.setFillColor(GRIS)
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(col_dreta_x + 31 * mm, 120 * mm, "(esquema)")

    # --- Compte i criteri (peu, a tota l'amplada) ---
    yb = 40 * mm
    requadre(c, M, yb, W - 2 * M, 12 * mm, color=GROC, fons=colors.HexColor("#fbf3dd"))
    c.setFillColor(GROC); c.setFont("Helvetica-Bold", 10)
    c.drawString(M + 4 * mm, yb + 6.5 * mm, "⚠️ COMPTE")
    text_ajustat(c, M + 4 * mm, yb + 2.5 * mm, t["compte"], mida=9.5, color=TINTA,
                 ample_max=W - 2 * M - 8 * mm, interlineat=4 * mm)
    requadre(c, M, yb - 15 * mm, W - 2 * M, 12 * mm, color=VERD, fons=colors.HexColor("#e6f4ec"))
    c.setFillColor(VERD); c.setFont("Helvetica-Bold", 10)
    c.drawString(M + 4 * mm, yb - 15 * mm + 6.5 * mm, "✅ COM SÉ QUE ESTÀ BÉ")
    text_ajustat(c, M + 4 * mm, yb - 15 * mm + 2.5 * mm, t["criteri"], mida=9.5, color=TINTA,
                 ample_max=W - 2 * M - 8 * mm, interlineat=4 * mm)
    c.showPage()
```

Nota: les coordenades verticals són un punt de partida; s'ajusten al Step 5 amb el render PNG perquè els passos llargs no trepitgin el bloc de peu. Si un text de passos s'acosta a `yb`, reduir `interlineat` a 4.5 mm o la mida a 10.

- [ ] **Step 3: Afegir `pagina_eines(c)` i `contraportada(c)`**

```python
def pagina_eines(c):
    y = capsalera_fitxa(c, 0, "🧰", "Eines i seguretat", "", "Carnet de màquina")
    y = bloc_titol(c, M, y, "LES EINES QUE FARÀS SERVIR")
    eines = ["Joc de claus allen", "Clau fixa del 15", "Tornavís pla i d'estrella",
             "Desmuntadors de pneumàtic", "Bomba d'inflar", "Mesurador de cadena",
             "Drap i raspall", "Oli de cadena i desengreixant", "Tercera mà (frens)"]
    for e in eines:
        c.setFillColor(INDIGO); c.setFont("Helvetica-Bold", 11); c.drawString(M, y, "•")
        c.setFillColor(TINTA); c.setFont("Helvetica", 11); c.drawString(M + 6 * mm, y, e)
        y -= 6.5 * mm
    y -= 4 * mm
    y = bloc_titol(c, M, y, "SEGURETAT (RECORDA EL CARNET DE MÀQUINA)")
    normes = ["Treballa amb la bici ben subjecta i estable.",
              "Mans netes i cabells/roba recollits a prop de màquines.",
              "Fes servir cada eina per a la seva feina.",
              "Si dubtes o alguna cosa no va, atura't i avisa el docent.",
              "Deixa l'espai net i les eines al seu lloc."]
    for n in normes:
        c.setFillColor(CIAN); c.setFont("Helvetica-Bold", 11); c.drawString(M, y, "✓")
        y = text_ajustat(c, M + 6 * mm, y, n, mida=10.5, ample_max=W - 2 * M - 6 * mm,
                         interlineat=5.5 * mm)
        y -= 1 * mm
    c.showPage()


def contraportada(c):
    c.setFillColor(INDIGO)
    c.roundRect(M, H - M - 12 * mm, W - 2 * M, 12 * mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 15)
    c.drawString(M + 5 * mm, H - M - 8.3 * mm, "Abans de deixar la bici: el semàfor")
    files = [(VERD, "VERD — Llesta per rodar", "Frens bé, rodes dures i rectes, tot ben collat."),
             (GROC, "GROC — Falta un últim ajust", "Acaba l'ajust pendent abans de fer-la servir."),
             (VERMELL, "VERMELL — No la facis servir", "Fre o roda insegurs: marca-la i avisa el docent.")]
    y = H - M - 26 * mm
    for col, tit, desc in files:
        c.setFillColor(col); c.circle(M + 6 * mm, y - 2 * mm, 4 * mm, fill=1, stroke=0)
        c.setFillColor(TINTA); c.setFont("Helvetica-Bold", 12); c.drawString(M + 14 * mm, y - 3 * mm, tit)
        c.setFillColor(GRIS); c.setFont("Helvetica", 10.5); c.drawString(M + 14 * mm, y - 9 * mm, desc)
        y -= 22 * mm
    y = bloc_titol(c, M, y, "ON DEMANAR AJUDA")
    for a in ["El docent del taller.", "La teva parella de treball.",
              "La fitxa de la unitat (Bx) i el seu vídeo.", "Aquest manual."]:
        c.setFillColor(CIAN); c.setFont("Helvetica-Bold", 11); c.drawString(M, y, "→")
        c.setFillColor(TINTA); c.setFont("Helvetica", 10.5); c.drawString(M + 6 * mm, y, a)
        y -= 6.5 * mm
    dibuixa_bici(c, W / 2, 34 * mm, escala=1.0, color=INDIGO)
    c.showPage()
```

- [ ] **Step 4: Actualitzar `main()` per generar les 12 pàgines**

```python
def main():
    c = canvas.Canvas(SORTIDA, pagesize=A4)
    c.setTitle("Manual ràpid de taller de bicicletes")
    portada(c)
    pagina_eines(c)
    for t in TASQUES:
        fitxa(c, t)
    contraportada(c)
    c.save()
    print(f"Manual generat a {SORTIDA} ({2 + len(TASQUES) + 1} pàgines esperades)")
```

- [ ] **Step 5: Generar, verificar recompte i renderitzar totes les pàgines**

Run: `py -3.11 scripts/genera_manual_taller.py`
Run:
```bash
py -3.11 -c "import pypdf; n=len(pypdf.PdfReader(r'Recursos/Manual_taller_bicicletes.pdf').pages); print('pagines', n); assert n==12"
py -3.11 -c "import fitz; d=fitz.open(r'Recursos/Manual_taller_bicicletes.pdf'); [d[i].get_pixmap(dpi=100).save(rf'.superpowers/sdd/manual_p{i+1}.png') for i in range(len(d))]; print('render ok')"
```
Expected: `pagines 12` i `render ok`. Obrir cada PNG i comprovar: cap text tallat, els passos no trepitgen el bloc de peu, capçalera i requadres alineats. Ajustar coordenades a `fitxa()` si cal i repetir.

- [ ] **Step 6: Commit**

```bash
git add scripts/genera_manual_taller.py
git commit -m "feat: manual taller - contingut 9 tasques, plantilla, eines i contraportada"
```

---

### Task 3: Esquemes vectorials de cada tasca

**Files:**
- Modify: `scripts/genera_manual_taller.py`

**Interfaces:**
- Consumeix: `dibuixa_bici`, paleta, helpers.
- Produeix: 9 funcions `esq_*(c, cx, cy)` que dibuixen dins el requadre de la columna dreta (centrat aprox. a `(cx, cy)`, amplada útil ~54 mm). S'assignen a la clau `"esquema"` de cada dict de `TASQUES`.

Cada esquema és una funció independent. Especificació d'elements (dibuixar amb `line`, `circle`, `rect`, `drawString`; retolar amb Helvetica 8):

- [ ] **Step 1: Escriure les 9 funcions d'esquema**

```python
def _fletxa(c, x1, y1, x2, y2, color=INDIGO):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(1.4)
    c.line(x1, y1, x2, y2)
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    for da in (2.6, -2.6):
        c.line(x2, y2, x2 - 3 * mm * math.cos(ang + da), y2 - 3 * mm * math.sin(ang + da))


def esq_mcheck(c, cx, cy):
    # bici amb 6 punts numerats sobre el recorregut
    dibuixa_bici(c, cx, cy, escala=0.85, color=GRIS, gruix=1.2)
    punts = [("1", cx + 15 * mm, cy), ("2", cx + 6 * mm, cy + 10 * mm),
             ("3", cx + 11 * mm, cy + 20 * mm), ("4", cx - 8 * mm, cy + 22 * mm),
             ("5", cx - 3 * mm, cy), ("6", cx - 17 * mm, cy)]
    for n, x, y in punts:
        c.setFillColor(INDIGO); c.circle(x, y, 3 * mm, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x, y - 2.6, n)


def esq_neteja(c, cx, cy):
    # llaç de cadena (el·lipse discontínua) amb gotes i fletxa de pedaleig enrere
    c.setStrokeColor(GRIS); c.setLineWidth(1.4)
    c.ellipse(cx - 20 * mm, cy - 8 * mm, cx + 20 * mm, cy + 8 * mm, stroke=1, fill=0)
    c.setFillColor(CIAN)
    for dx in (-10 * mm, 0, 10 * mm):
        c.circle(cx + dx, cy + 8 * mm, 1.3 * mm, fill=1, stroke=0)  # gotes d'oli
    _fletxa(c, cx + 6 * mm, cy - 12 * mm, cx - 6 * mm, cy - 12 * mm)  # pedala enrere
    c.setFillColor(GRIS); c.setFont("Helvetica", 8)
    c.drawCentredString(cx, cy - 18 * mm, "pedala enrere")


def esq_roda(c, cx, cy):
    # palanca de tancament ràpid: obert vs tancat
    for x, estat, ang in ((cx - 12 * mm, "obert", 55), (cx + 12 * mm, "tancat", 0)):
        c.setStrokeColor(GRIS); c.setLineWidth(1.6)
        c.line(x, cy - 10 * mm, x, cy + 10 * mm)  # eix
        c.setStrokeColor(INDIGO); c.setLineWidth(2.2)
        import math
        c.line(x, cy, x + 12 * mm * math.cos(math.radians(ang)), cy + 12 * mm * math.sin(math.radians(ang)))
        c.setFillColor(GRIS); c.setFont("Helvetica", 8); c.drawCentredString(x, cy - 15 * mm, estat)


def esq_punxada(c, cx, cy):
    # secció de pneumàtic (U) + cambra + desmuntador
    c.setStrokeColor(GRIS); c.setLineWidth(1.6)
    c.arc(cx - 18 * mm, cy - 10 * mm, cx + 18 * mm, cy + 14 * mm, startAng=200, extent=140)
    c.setStrokeColor(CIAN); c.circle(cx, cy + 2 * mm, 8 * mm, stroke=1, fill=0)  # cambra
    c.setFillColor(VERMELL); c.circle(cx + 6 * mm, cy + 6 * mm, 1.4 * mm, fill=1, stroke=0)  # forat
    c.setFillColor(GRIS); c.setFont("Helvetica", 8)
    c.drawCentredString(cx, cy - 14 * mm, "busca el forat")


def esq_fre_sabata(c, cx, cy):
    # llanta (arc) + sabata amb separació 2-3 mm i toe-in
    c.setStrokeColor(GRIS); c.setLineWidth(2)
    c.arc(cx - 4 * mm, cy - 20 * mm, cx + 30 * mm, cy + 20 * mm, startAng=120, extent=120)  # llanta
    c.setFillColor(INDIGO); c.rect(cx - 14 * mm, cy - 3 * mm, 9 * mm, 6 * mm, fill=1, stroke=0)  # sabata
    _fletxa(c, cx - 5 * mm, cy + 9 * mm, cx - 1 * mm, cy + 9 * mm, color=VERMELL)
    c.setFillColor(GRIS); c.setFont("Helvetica", 8); c.drawString(cx - 3 * mm, cy + 11 * mm, "2-3 mm")


def esq_fre_disc(c, cx, cy):
    # disc (cercle amb forats) + pinça
    c.setStrokeColor(GRIS); c.setLineWidth(1.6); c.circle(cx, cy, 16 * mm, stroke=1, fill=0)
    c.circle(cx, cy, 4 * mm, stroke=1, fill=0)
    c.setFillColor(INDIGO); c.rect(cx + 12 * mm, cy - 5 * mm, 7 * mm, 10 * mm, fill=1, stroke=0)  # pinça
    c.setFillColor(VERMELL); c.setFont("Helvetica-Bold", 8); c.drawCentredString(cx, cy - 22 * mm, "no toquis el disc")


def esq_cadena(c, cx, cy):
    # tram de cadena (rectangles) amb mesurador i marca 0,75%
    c.setStrokeColor(GRIS); c.setLineWidth(1.2)
    for i in range(6):
        c.rect(cx - 24 * mm + i * 8 * mm, cy - 2 * mm, 6 * mm, 4 * mm, fill=0, stroke=1)
    c.setStrokeColor(CIAN); c.setLineWidth(1.6); c.line(cx - 24 * mm, cy + 6 * mm, cx + 24 * mm, cy + 6 * mm)
    c.setFillColor(VERMELL); c.setFont("Helvetica-Bold", 8); c.drawCentredString(cx, cy - 10 * mm, "0,75% = gastada")


def esq_canvi(c, cx, cy):
    # pinyons (cercles concèntrics) + cargols H i L
    c.setStrokeColor(GRIS); c.setLineWidth(1.4)
    for r in (14 * mm, 10 * mm, 6 * mm): c.circle(cx - 4 * mm, cy, r, stroke=1, fill=0)
    c.setFillColor(INDIGO); c.setFont("Helvetica-Bold", 9)
    c.drawString(cx + 12 * mm, cy + 6 * mm, "H"); c.drawString(cx + 12 * mm, cy - 8 * mm, "L")
    c.setFillColor(GRIS); c.setFont("Helvetica", 8)
    c.drawString(cx + 17 * mm, cy + 6 * mm, "petit"); c.drawString(cx + 17 * mm, cy - 8 * mm, "gran")


def esq_seient(c, cx, cy):
    # tija amb marca màxima + alçada
    c.setStrokeColor(GRIS); c.setLineWidth(2); c.line(cx, cy - 16 * mm, cx, cy + 12 * mm)
    c.setStrokeColor(VERMELL); c.setLineWidth(1.4); c.line(cx - 4 * mm, cy - 8 * mm, cx + 4 * mm, cy - 8 * mm)
    c.setFillColor(INDIGO); c.rect(cx - 7 * mm, cy + 12 * mm, 14 * mm, 3 * mm, fill=1, stroke=0)  # seient
    c.setFillColor(VERMELL); c.setFont("Helvetica", 8); c.drawString(cx + 6 * mm, cy - 9 * mm, "marca màx.")
```

- [ ] **Step 2: Assignar cada esquema al seu dict a `TASQUES`**

Canviar `"esquema": None` per la funció corresponent a cada dict:
- Tasca 1 → `esq_mcheck`, 2 → `esq_neteja`, 3 → `esq_roda`, 4 → `esq_punxada`, 5 → `esq_fre_sabata`, 6 → `esq_fre_disc`, 7 → `esq_cadena`, 8 → `esq_canvi`, 9 → `esq_seient`.

Com que les funcions es defineixen abans de `TASQUES`? No: `TASQUES` es defineix al principi (Task 2) i les funcions d'esquema després. Per evitar problemes d'ordre, definir les funcions `esq_*` ABANS de `TASQUES`, o assignar-les després amb un pas d'enllaç al final del mòdul:

```python
_ESQUEMES = [esq_mcheck, esq_neteja, esq_roda, esq_punxada, esq_fre_sabata,
             esq_fre_disc, esq_cadena, esq_canvi, esq_seient]
for _t, _e in zip(TASQUES, _ESQUEMES):
    _t["esquema"] = _e
```

Col·locar aquest bloc d'enllaç just abans de `def main()`.

- [ ] **Step 3: Generar i revisar visualment cada esquema**

Run: `py -3.11 scripts/genera_manual_taller.py`
Run: `py -3.11 -c "import fitz; d=fitz.open(r'Recursos/Manual_taller_bicicletes.pdf'); [d[i].get_pixmap(dpi=110).save(rf'.superpowers/sdd/manual_p{i+1}.png') for i in range(len(d))]; print('ok')"`
Obrir els PNG de les pàgines 3–11 i comprovar que cada esquema es veu dins el requadre, no surt dels marges i les etiquetes es llegeixen. Ajustar coordenades/escala de la funció que calgui i repetir.

- [ ] **Step 4: Commit**

```bash
git add scripts/genera_manual_taller.py
git commit -m "feat: manual taller - esquemes vectorials de les 9 tasques"
```

---

### Task 4: Publicar el manual a la web

**Files:**
- Modify: `build_web.py` (funció `copy_assets` i l'índex de Bicicletes)

**Interfaces:**
- Consumeix: el PDF `Recursos/Manual_taller_bicicletes.pdf` generat a Tasks 1–3.
- Produeix: còpia del PDF sota `web/` i un enllaç de descàrrega a `web/classes/bicicletes/index.html`.

- [ ] **Step 1: Localitzar `copy_assets` i la construcció de l'índex de Bicicletes**

Run: `grep -n "def copy_assets\|Recursos\|bicicletes/index\|BIKE_CARDS\|def build_track_index\|index.html" build_web.py`
Identificar (a) on `copy_assets` copia PDFs/xlsx de Recursos, i (b) on es genera l'índex de la pista de Bicicletes.

- [ ] **Step 2: Fer que `copy_assets` copiï el PDF del manual**

A `copy_assets`, allà on ja es copien els `Recursos/*.xlsx`, afegir la còpia del PDF del manual a `web/recursos/` (o la carpeta d'assets que faci servir). Codi (adaptar el destí al patró existent de la funció):

```python
    # Manual de taller (PDF descarregable)
    manual = SRC / "Recursos" / "Manual_taller_bicicletes.pdf"
    if manual.exists():
        dest = WEB / "recursos" / manual.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(manual, dest)
```

Nota: usar els mateixos noms de variable (`SRC`, `WEB`, `shutil`) que ja hi hagi al fitxer; si difereixen, adaptar-los.

- [ ] **Step 3: Afegir l'enllaç de descàrrega a l'índex de Bicicletes**

A la generació de `web/classes/bicicletes/index.html`, afegir a la capçalera de la pàgina (a prop del títol) un enllaç destacat:

```python
    manual_html = ('<p class="manual-link"><a href="{prefix}recursos/Manual_taller_bicicletes.pdf" '
                   'download>📘 Descarrega el manual ràpid de taller (PDF)</a></p>').format(prefix=prefix_rel)
```

Inserir `manual_html` al cos de l'índex de Bicicletes (no al de Maker). Fer servir la variable de prefix relatiu que ja utilitzi la funció per als enllaços (p. ex. `prefix`/`rel`).

- [ ] **Step 4: Construir la web i verificar còpia i enllaç**

Run: `py -3.11 build_web.py`
Run:
```bash
py -3.11 -c "import pathlib; p=pathlib.Path('web/recursos/Manual_taller_bicicletes.pdf'); print('PDF copiat', p.exists() and p.stat().st_size>0)"
grep -c "Manual_taller_bicicletes.pdf" web/classes/bicicletes/index.html
```
Expected: `PDF copiat True` i el `grep` retorna `>=1`. Comprovar que l'enllaç NO apareix a `web/classes/maker/index.html` (`grep -c` → `0`).

- [ ] **Step 5: Validar que l'enllaç resol (servidor local)**

Run (amb el servidor local actiu o obrint el fitxer): comprovar que `web/recursos/Manual_taller_bicicletes.pdf` existeix i que l'`href` de l'índex hi apunta. Reutilitzar el validador d'enllaços locals (com a `Recursos/LLEGEIX-ME`):

```bash
py -3.11 -c "
import pathlib, re, urllib.parse
f = pathlib.Path('web/classes/bicicletes/index.html'); html=f.read_text(encoding='utf-8')
for m in re.findall(r'href=\"([^\"]+\.pdf)\"', html):
    if m.startswith('http'): continue
    p=(f.parent/urllib.parse.unquote(m)).resolve()
    print('OK' if p.exists() else 'TRENCAT', m)
"
```
Expected: la línia del manual surt `OK`.

- [ ] **Step 6: Commit**

```bash
git add build_web.py
git commit -m "feat: publicar el manual de taller a la web (copia + enllac a l'index de Bicicletes)"
```

---

### Task 5: Revisió de català i verificació final

**Files:**
- Cap canvi de codi tret de correccions que sorgeixin de la revisió.

- [ ] **Step 1: Extreure el text del PDF i revisar el català**

Run: `py -3.11 -c "import pypdf; r=pypdf.PdfReader(r'Recursos/Manual_taller_bicicletes.pdf'); print('\n'.join(p.extract_text() for p in r.pages))" > .superpowers/sdd/manual_text.txt`
Revisar `.superpowers/sdd/manual_text.txt` (o dispatch d'un reviewer de català) buscant: faltes d'accent, castellanismes, confusió `ll`/`l·l`, concordances. Recordatori: «llanta», «baula», «lligam» porten dígraf `ll` (correcte); «col·locar» porta ela geminada. Corregir a `TASQUES` / pàgines si cal, regenerar i tornar a extreure.

- [ ] **Step 2: Verificació final completa**

Run:
```bash
py -3.11 scripts/genera_manual_taller.py
py -3.11 -c "import pypdf; n=len(pypdf.PdfReader(r'Recursos/Manual_taller_bicicletes.pdf').pages); print('pagines',n); assert n==12"
py -3.11 build_web.py
py -3.11 -c "import pathlib; print('web PDF', pathlib.Path('web/recursos/Manual_taller_bicicletes.pdf').exists())"
```
Expected: `pagines 12`, `web PDF True`, sense errors. Render final de totes les pàgines i repàs visual: portada, eines, 9 fitxes amb esquema, contraportada; res tallat.

- [ ] **Step 3: Commit final (si hi ha correccions)**

```bash
git add -A
git commit -m "fix: correccions de catala i acabats del manual de taller"
```

---

## Self-Review

**Spec coverage:**
- §4 contingut (12 pàgines, ordre) → Task 1 (portada) + Task 2 (eines, 9 fitxes, contraportada). ✓
- §5 plantilla de fitxa → Task 2 `fitxa()`. ✓
- §6 esquemes per fitxa → Task 3 (9 funcions `esq_*`). ✓
- §7 arquitectura (script content-as-data, copy_assets, enllaç) → Tasks 1–4. ✓
- §8 verificació (pypdf, pymupdf, català, enllaços) → Task 5 + steps de verificació a cada tasca. ✓
- §2 constraint NEE (plantilla fixa, pictogrames, ⚠️/✅) → Task 2 plantilla. ✓
- Constraint «sense drets» → Task 3 tot vectorial. ✓

**Placeholder scan:** el text de les 9 tasques és complet i literal a Task 2. Els esquemes de Task 3 tenen codi real; s'afinen contra render PNG (mètode declarat als Global Constraints), no són TODO. Cap «TBD».

**Type consistency:** claus de `TASQUES` (`num, icona, titol, temps, unitat, eines, passos, compte, criteri, esquema`) usades igual a `fitxa()`. Les 9 `esq_*(c, cx, cy)` tenen la mateixa signatura i s'enllacen via `_ESQUEMES`. `capsalera_fitxa` retorna `y0` consumit per `fitxa` i `pagina_eines`.

**Nota d'execució:** el PDF és sortida visual; els «tests» són recompte (pypdf) + render (pymupdf) + revisió d'ull, no pytest. És el patró coherent amb la resta de `scripts/genera_*.py` (cap test unitari).
