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
import math
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


def icona_avis(c, x, y, mida=4.4 * mm):
    """Triangle d'avís groc amb signe d'exclamació (x, y = cantonada inferior esquerra)."""
    p = c.beginPath()
    p.moveTo(x, y)
    p.lineTo(x + mida, y)
    p.lineTo(x + mida / 2, y + mida)
    p.close()
    c.setFillColor(GROC)
    c.setStrokeColor(GROC)
    c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(x + mida / 2, y + 1.0 * mm, "!")


def requadre(c, x, y, ample, alt, color=LINIA, fons=None, radi=3):
    if fons is not None:
        c.setFillColor(fons)
    c.setStrokeColor(color)
    c.setLineWidth(0.9)
    c.roundRect(x, y, ample, alt, radi, fill=(fons is not None), stroke=1)


def text_ajustat(c, x, y, text, font="Helvetica", mida=10.5, color=TINTA,
                 ample_max=None, interlineat=5 * mm):
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


def dibuixa_bici(c, cx, cy, escala=1.0, color=TINTA, gruix=1.6):
    """Silueta lateral esquemàtica: dues rodes, quadre triangular, manillar i seient."""
    c.setStrokeColor(color)
    c.setLineWidth(gruix)
    r = 15 * mm * escala
    d = 34 * mm * escala  # distància entre eixos
    xr = cx - d / 2   # centre roda del darrere
    xf = cx + d / 2   # centre roda del davant
    c.circle(xr, cy, r, stroke=1, fill=0)
    c.circle(xf, cy, r, stroke=1, fill=0)
    ped = (cx - 2 * mm * escala, cy)           # eix pedaler
    seient = (cx - 6 * mm * escala, cy + r + 6 * mm * escala)
    manillar = (xf - 6 * mm * escala, cy + r + 7 * mm * escala)
    c.line(ped[0], ped[1], seient[0], seient[1])
    c.line(ped[0], ped[1], xr, cy)
    c.line(seient[0], seient[1], xr, cy)
    c.line(seient[0], seient[1], manillar[0], manillar[1])
    c.line(ped[0], ped[1], manillar[0], manillar[1])
    c.line(xf, cy, manillar[0], manillar[1])
    c.line(seient[0] - 4 * mm * escala, seient[1], seient[0] + 4 * mm * escala, seient[1])
    c.line(manillar[0] - 1 * mm * escala, manillar[1], manillar[0] + 6 * mm * escala, manillar[1])


def capsalera_fitxa(c, num, icona, titol, temps, unitat):
    """Barra superior de cada fitxa de tasca. Retorna la y de partida del cos."""
    y = H - M - 12 * mm
    c.setFillColor(INDIGO)
    c.roundRect(M, y, W - 2 * M, 12 * mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    prefix = f"{num}. " if num else ""
    c.drawString(M + 5 * mm, y + 3.7 * mm, f"{prefix}{titol}")
    c.setFont("Helvetica", 8.5)
    dreta = f"{temps} · {unitat}" if temps else unitat
    c.drawRightString(W - M - 5 * mm, y + 3.7 * mm, dreta)
    return y - 6 * mm


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
    dibuixa_bici(c, W / 2, H - 150 * mm, escala=1.4, color=INDIGO)
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 10)
    c.drawCentredString(W / 2, 30 * mm, "Repara i Roda 360 · Taller de bicicletes · 4t ESO")
    c.drawCentredString(W / 2, 24 * mm, "Institut Consell de Cent")
    c.showPage()


TASQUES = [
    {"num": 1, "icona": "🔍", "titol": "M-check de seguretat", "temps": "10 min", "unitat": "B2",
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

    {"num": 2, "icona": "🧽", "titol": "Neteja i lubricació", "temps": "15 min", "unitat": "B2",
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

    {"num": 3, "icona": "🛞", "titol": "Treure i posar la roda", "temps": "10 min", "unitat": "B3",
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

    {"num": 4, "icona": "🔧", "titol": "Reparar una punxada", "temps": "20 min", "unitat": "B3",
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

    {"num": 5, "icona": "🛑", "titol": "Frens de sabata", "temps": "15 min", "unitat": "B4",
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

    {"num": 6, "icona": "⚙️", "titol": "Frens de disc", "temps": "15 min", "unitat": "B4",
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

    {"num": 7, "icona": "🔗", "titol": "Cadena: desgast i unió", "temps": "15 min", "unitat": "B5",
     "eines": ["Mesurador de cadena", "Alicates de baula ràpida"],
     "passos": [
        "Posa el mesurador sobre la cadena: si entra fins a la marca de 0,75 %, està gastada.",
        "Si l'has de canviar, obre la baula ràpida amb les alicates (o el tronçador).",
        "Compta que la cadena nova tingui les mateixes baules que la vella.",
        "Passa la cadena pels plats i els pinyons seguint el desviador.",
        "Tanca la baula ràpida i estira fort perquè encaixi bé."],
     "compte": "Una cadena molt gastada desgasta plats i pinyons: no esperis massa a canviar-la.",
     "criteri": "La baula queda fixa i la cadena passa suau per tots els canvis.",
     "esquema": None},

    {"num": 8, "icona": "🔩", "titol": "Canvi posterior (topalls H i L)", "temps": "20 min", "unitat": "B6",
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

    {"num": 9, "icona": "🪑", "titol": "Seient i manillar", "temps": "10 min", "unitat": "B7",
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
    y = bloc_titol(c, M, y0, "ABANS DE COMENÇAR")
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

    # --- Esquema (columna dreta, part superior) ---
    esq_y = 156 * mm
    esq_alt = (H - M - 18 * mm) - esq_y
    requadre(c, col_dreta_x, esq_y, 62 * mm, esq_alt,
             color=LINIA, fons=colors.HexColor("#f4f5fb"))
    if t["esquema"]:
        t["esquema"](c, col_dreta_x + 31 * mm, esq_y + esq_alt / 2)
    else:
        c.setFillColor(GRIS)
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(col_dreta_x + 31 * mm, esq_y + esq_alt / 2, "(esquema)")

    # --- Compte i criteri (peu, a tota l'amplada) ---
    yb = 40 * mm
    requadre(c, M, yb, W - 2 * M, 13 * mm, color=GROC, fons=colors.HexColor("#fbf3dd"))
    icona_avis(c, M + 4 * mm, yb + 6.3 * mm)
    c.setFillColor(GROC)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M + 10 * mm, yb + 7 * mm, "COMPTE")
    text_ajustat(c, M + 4 * mm, yb + 3 * mm, t["compte"], mida=9.5, color=TINTA,
                 ample_max=W - 2 * M - 8 * mm, interlineat=4 * mm)
    requadre(c, M, yb - 16 * mm, W - 2 * M, 13 * mm, color=VERD, fons=colors.HexColor("#e6f4ec"))
    c.setFillColor(VERD)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M + 4 * mm, yb - 16 * mm + 7 * mm, "✓ COM SÉ QUE ESTÀ BÉ")
    text_ajustat(c, M + 4 * mm, yb - 16 * mm + 3 * mm, t["criteri"], mida=9.5, color=TINTA,
                 ample_max=W - 2 * M - 8 * mm, interlineat=4 * mm)
    c.showPage()


def pagina_eines(c):
    y = capsalera_fitxa(c, 0, "🧰", "Eines i seguretat", "", "Carnet de màquina")
    y = bloc_titol(c, M, y, "LES EINES QUE FARÀS SERVIR")
    eines = ["Joc de claus allen", "Clau fixa del 15", "Tornavís pla i d'estrella",
             "Desmuntadors de pneumàtic", "Bomba d'inflar", "Mesurador de cadena",
             "Drap i raspall", "Oli de cadena i desengreixant", "Tercera mà (frens)"]
    for e in eines:
        c.setFillColor(INDIGO)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M, y, "•")
        c.setFillColor(TINTA)
        c.setFont("Helvetica", 11)
        c.drawString(M + 6 * mm, y, e)
        y -= 6.5 * mm
    y -= 4 * mm
    y = bloc_titol(c, M, y, "SEGURETAT (RECORDA EL CARNET DE MÀQUINA)")
    normes = ["Treballa amb la bici ben subjecta i estable.",
              "Mans netes i cabells o roba recollits a prop de màquines.",
              "Fes servir cada eina per a la seva feina.",
              "Si dubtes o alguna cosa no va, atura't i avisa el docent.",
              "Deixa l'espai net i les eines al seu lloc."]
    for n in normes:
        c.setFillColor(CIAN)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M, y, "✓")
        y = text_ajustat(c, M + 6 * mm, y, n, mida=10.5, ample_max=W - 2 * M - 6 * mm,
                         interlineat=5.5 * mm)
        y -= 1 * mm
    c.showPage()


def contraportada(c):
    c.setFillColor(INDIGO)
    c.roundRect(M, H - M - 12 * mm, W - 2 * M, 12 * mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(M + 5 * mm, H - M - 8.3 * mm, "Abans de deixar la bici: el semàfor")
    files = [(VERD, "VERD — Llesta per rodar", "Frens bé, rodes dures i rectes, tot ben collat."),
             (GROC, "GROC — Falta un últim ajust", "Acaba l'ajust pendent abans de fer-la servir."),
             (VERMELL, "VERMELL — No la facis servir", "Fre o roda insegurs: marca-la i avisa el docent.")]
    y = H - M - 28 * mm
    for col, tit, desc in files:
        c.setFillColor(col)
        c.circle(M + 6 * mm, y - 2 * mm, 4 * mm, fill=1, stroke=0)
        c.setFillColor(TINTA)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(M + 14 * mm, y - 3 * mm, tit)
        c.setFillColor(GRIS)
        c.setFont("Helvetica", 10.5)
        c.drawString(M + 14 * mm, y - 9 * mm, desc)
        y -= 22 * mm
    y = bloc_titol(c, M, y, "ON DEMANAR AJUDA")
    for a in ["El docent del taller.", "La teva parella de treball.",
              "La fitxa de la unitat (Bx) i el seu vídeo.", "Aquest manual."]:
        c.setFillColor(CIAN)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M, y, "→")
        c.setFillColor(TINTA)
        c.setFont("Helvetica", 10.5)
        c.drawString(M + 6 * mm, y, a)
        y -= 6.5 * mm
    dibuixa_bici(c, W / 2, 34 * mm, escala=1.0, color=INDIGO)
    c.showPage()


def _fletxa(c, x1, y1, x2, y2, color=INDIGO):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(1.4)
    c.line(x1, y1, x2, y2)
    ang = math.atan2(y2 - y1, x2 - x1)
    for da in (2.6, -2.6):
        c.line(x2, y2, x2 - 3 * mm * math.cos(ang + da), y2 - 3 * mm * math.sin(ang + da))


def esq_mcheck(c, cx, cy):
    """Bici amb 6 punts numerats sobre el recorregut de revisió."""
    dibuixa_bici(c, cx, cy, escala=0.85, color=GRIS, gruix=1.2)
    punts = [("1", cx + 15 * mm, cy), ("2", cx + 6 * mm, cy + 10 * mm),
             ("3", cx + 11 * mm, cy + 20 * mm), ("4", cx - 8 * mm, cy + 22 * mm),
             ("5", cx - 3 * mm, cy), ("6", cx - 17 * mm, cy)]
    for n, x, y in punts:
        c.setFillColor(INDIGO)
        c.circle(x, y, 3 * mm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x, y - 2.6, n)


def esq_neteja(c, cx, cy):
    """Llaç de cadena amb gotes d'oli i fletxa de pedaleig enrere."""
    c.setStrokeColor(GRIS)
    c.setLineWidth(1.4)
    c.ellipse(cx - 20 * mm, cy - 8 * mm, cx + 20 * mm, cy + 8 * mm, stroke=1, fill=0)
    c.setFillColor(CIAN)
    for dx in (-10 * mm, 0, 10 * mm):
        c.circle(cx + dx, cy + 8 * mm, 1.3 * mm, fill=1, stroke=0)
    _fletxa(c, cx + 6 * mm, cy - 12 * mm, cx - 6 * mm, cy - 12 * mm)
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8)
    c.drawCentredString(cx, cy - 18 * mm, "pedala enrere")


def esq_roda(c, cx, cy):
    """Palanca de tancament ràpid: obert vs tancat."""
    for x, estat, ang in ((cx - 12 * mm, "obert", 55), (cx + 12 * mm, "tancat", 0)):
        c.setStrokeColor(GRIS)
        c.setLineWidth(1.6)
        c.line(x, cy - 10 * mm, x, cy + 10 * mm)
        c.setStrokeColor(INDIGO)
        c.setLineWidth(2.2)
        c.line(x, cy, x + 12 * mm * math.cos(math.radians(ang)),
               cy + 12 * mm * math.sin(math.radians(ang)))
        c.setFillColor(GRIS)
        c.setFont("Helvetica", 8)
        c.drawCentredString(x, cy - 15 * mm, estat)


def esq_punxada(c, cx, cy):
    """Secció de pneumàtic amb cambra i forat marcat."""
    c.setStrokeColor(GRIS)
    c.setLineWidth(1.6)
    c.arc(cx - 18 * mm, cy - 10 * mm, cx + 18 * mm, cy + 14 * mm, startAng=200, extent=140)
    c.setStrokeColor(CIAN)
    c.circle(cx, cy + 2 * mm, 8 * mm, stroke=1, fill=0)
    c.setFillColor(VERMELL)
    c.circle(cx + 6 * mm, cy + 6 * mm, 1.4 * mm, fill=1, stroke=0)
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8)
    c.drawCentredString(cx, cy - 14 * mm, "busca el forat")


def esq_fre_sabata(c, cx, cy):
    """Llanta i sabata amb separació 2-3 mm."""
    c.setStrokeColor(GRIS)
    c.setLineWidth(2)
    c.arc(cx - 4 * mm, cy - 20 * mm, cx + 30 * mm, cy + 20 * mm, startAng=120, extent=120)
    c.setFillColor(INDIGO)
    c.rect(cx - 14 * mm, cy - 3 * mm, 9 * mm, 6 * mm, fill=1, stroke=0)
    _fletxa(c, cx - 5 * mm, cy + 9 * mm, cx - 1 * mm, cy + 9 * mm, color=VERMELL)
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8)
    c.drawString(cx - 3 * mm, cy + 11 * mm, "2-3 mm")


def esq_fre_disc(c, cx, cy):
    """Disc de fre i pinça."""
    c.setStrokeColor(GRIS)
    c.setLineWidth(1.6)
    c.circle(cx, cy, 16 * mm, stroke=1, fill=0)
    c.circle(cx, cy, 4 * mm, stroke=1, fill=0)
    c.setFillColor(INDIGO)
    c.rect(cx + 12 * mm, cy - 5 * mm, 7 * mm, 10 * mm, fill=1, stroke=0)
    c.setFillColor(VERMELL)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(cx, cy - 22 * mm, "no toquis el disc")


def esq_cadena(c, cx, cy):
    """Tram de cadena amb mesurador i marca de desgast."""
    c.setStrokeColor(GRIS)
    c.setLineWidth(1.2)
    for i in range(6):
        c.rect(cx - 24 * mm + i * 8 * mm, cy - 2 * mm, 6 * mm, 4 * mm, fill=0, stroke=1)
    c.setStrokeColor(CIAN)
    c.setLineWidth(1.6)
    c.line(cx - 24 * mm, cy + 6 * mm, cx + 24 * mm, cy + 6 * mm)
    c.setFillColor(VERMELL)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(cx, cy - 10 * mm, "0,75% = gastada")


def esq_canvi(c, cx, cy):
    """Pinyons concèntrics amb cargols H i L."""
    c.setStrokeColor(GRIS)
    c.setLineWidth(1.4)
    for r in (14 * mm, 10 * mm, 6 * mm):
        c.circle(cx - 4 * mm, cy, r, stroke=1, fill=0)
    c.setFillColor(INDIGO)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(cx + 12 * mm, cy + 6 * mm, "H")
    c.drawString(cx + 12 * mm, cy - 8 * mm, "L")
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8)
    c.drawString(cx + 17 * mm, cy + 6 * mm, "petit")
    c.drawString(cx + 17 * mm, cy - 8 * mm, "gran")


def esq_seient(c, cx, cy):
    """Tija del seient amb marca màxima."""
    c.setStrokeColor(GRIS)
    c.setLineWidth(2)
    c.line(cx, cy - 16 * mm, cx, cy + 12 * mm)
    c.setStrokeColor(VERMELL)
    c.setLineWidth(1.4)
    c.line(cx - 4 * mm, cy - 8 * mm, cx + 4 * mm, cy - 8 * mm)
    c.setFillColor(INDIGO)
    c.rect(cx - 7 * mm, cy + 12 * mm, 14 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillColor(VERMELL)
    c.setFont("Helvetica", 8)
    c.drawString(cx + 6 * mm, cy - 9 * mm, "marca màx.")


_ESQUEMES = [esq_mcheck, esq_neteja, esq_roda, esq_punxada, esq_fre_sabata,
             esq_fre_disc, esq_cadena, esq_canvi, esq_seient]
for _t, _e in zip(TASQUES, _ESQUEMES):
    _t["esquema"] = _e


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


if __name__ == "__main__":
    main()
