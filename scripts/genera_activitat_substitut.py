#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Activitat autònoma de 50' per a professor/a substitut/a (B0), en PDF amb imatges incrustades.

Full de l'alumnat (autònom, per parelles) + full del docent substitut (temps + solucions).
Sortida: Classes/Bicicletes/B0_Punt_de_partida/Activitat_substitut_aula.pdf
Ús:  py -3.11 scripts/genera_activitat_substitut.py   ·   Requereix: reportlab, pillow
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

AQUI = os.path.dirname(os.path.abspath(__file__))
ARREL = os.path.normpath(os.path.join(AQUI, ".."))
SORTIDA = os.path.join(ARREL, "Classes", "Bicicletes", "B0_Punt_de_partida",
                        "Activitat_substitut_aula.pdf")
EINES_DIR = os.path.join(ARREL, "Recursos", "imatges", "eines")
POSTER = os.path.join(ARREL, "Recursos", "parts-de-la-bicicleta-en-català-1024x602.png")

W, H = A4
M = 16 * mm
INDIGO = colors.HexColor("#5b5bd6")
GRIS = colors.HexColor("#5a6079")
TINTA = colors.HexColor("#14172a")
LINIA = colors.HexColor("#c3c7d9")

EINES = [
    ("Claus Allen", "Collar/descollar cargols de cap hexagonal (potència, bieles, seient)"),
    ("Tornavisos", "Cargols de canvis, portabidons, accessoris"),
    ("Claus fixes / de got", "Femelles i eixos (rodes de femella, pedals)"),
    ("Palanques desmuntables", "Treure el pneumàtic de la llanta"),
    ("Tronxacadenes", "Tallar i unir la cadena"),
    ("Bomba amb manòmetre", "Inflar les rodes a la pressió correcta"),
    ("Clau de radis", "Tensar els radis / centrar la roda"),
    ("Extractor de bieles", "Treure les bieles"),
]

SITUACIONS = [
    "Màniga llarga a prop de la cadena.",
    "Una eina llançada d'una taula a una altra.",
    "Encenalls netejats amb la mà.",
    "Beguda oberta sobre la taula de treball.",
    "Eines escampades pel terra.",
]
SOLUCIONS = [
    "Netejar-los amb un raspall, mai amb la mà.",
    "Donar-la a mà, mai llançar-la.",
    "Cada eina al seu lloc en acabar.",
    "Arremangar-se la màniga.",
    "Deixar-la fora del taller.",
]
RESPOSTA = {1: "D", 2: "B", 3: "A", 4: "E", 5: "C"}


def liniah(c, x, y, ample):
    c.setStrokeColor(LINIA)
    c.setLineWidth(0.6)
    c.line(x, y, x + ample, y)


def capcalera(c, titol, subtitol):
    c.setFillColor(INDIGO)
    c.roundRect(M, H - M - 10 * mm, W - 2 * M, 10 * mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M + 4 * mm, H - M - 7 * mm, titol)
    c.setFont("Helvetica", 8)
    c.drawRightString(W - M - 4 * mm, H - M - 7 * mm, subtitol)


def h2(c, x, y, text):
    c.setFillColor(INDIGO)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y, text)
    liniah(c, x, y - 2 * mm, W - 2 * M - (x - M))


def peu(c, text):
    c.setFillColor(GRIS)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawCentredString(W / 2, M / 2, text)


def img_fit(c, path, x, y, box_w, box_h):
    img = ImageReader(path)
    iw, ih = img.getSize()
    escala = min(box_w / iw, box_h / ih)
    w, h = iw * escala, ih * escala
    cx = x + (box_w - w) / 2
    cy = y + (box_h - h) / 2
    c.setStrokeColor(LINIA)
    c.setLineWidth(0.6)
    c.rect(x, y, box_w, box_h, fill=0, stroke=1)
    c.drawImage(img, cx, cy, width=w, height=h, preserveAspectRatio=True, mask="auto")


def pagina1_alumnat(c):
    capcalera(c, "ACTIVITAT AUTÒNOMA · Full de l'alumnat (1/2)", "B0 · Repara i Roda 360")

    y = H - M - 18 * mm
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 9.5)
    c.drawString(M, y, "Nom 1:")
    liniah(c, M + 15 * mm, y - 1, 65 * mm)
    c.drawString(M + 85 * mm, y, "Nom 2:")
    liniah(c, M + 100 * mm, y - 1, W - M - (M + 100 * mm))

    # Part 1
    y -= 11 * mm
    h2(c, M, y, "Part 1 — Endevina l'eina (15 min)")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 8.8)
    c.drawString(M, y - 6 * mm,
                 "Mira cada foto i escriu quin nom li poses i per a què creus que serveix.")

    box_w, box_h = 41 * mm, 27 * mm
    gap_x = 4 * mm
    fila_alt = box_h + 5 * mm + 9 * mm + 4 * mm  # imatge + núm + 2 línies + marge
    origin_y = y - 11 * mm
    fila_bottom = origin_y
    for i in range(8):
        col = i % 4
        fila = i // 4
        x = M + col * (box_w + gap_x)
        yy = origin_y - fila * fila_alt - box_h
        img_fit(c, os.path.join(EINES_DIR, f"{i + 1}.jpg"), x, yy, box_w, box_h)
        c.setFillColor(INDIGO)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(x + 1 * mm, yy + box_h + 1.5 * mm, f"{i + 1}.")
        liniah(c, x + 5 * mm, yy - 3 * mm, box_w - 5 * mm)
        liniah(c, x + 5 * mm, yy - 8 * mm, box_w - 5 * mm)
        fila_bottom = min(fila_bottom, yy - 8 * mm)

    y = fila_bottom - 8 * mm

    # Part 2
    h2(c, M, y, "Part 2 — Troba el perill (10 min)")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 8.8)
    c.drawString(M, y - 6 * mm,
                 "Llegiu cada situació perillosa i escriviu la lletra de la solució que la resol.")

    colx = [M, M + 95 * mm]
    titols = ["Situacions perilloses", "Solucions"]
    llistes = [SITUACIONS, SOLUCIONS]
    marques = [str(i + 1) + "." for i in range(5)]
    marques2 = ["A.", "B.", "C.", "D.", "E."]
    yy0 = y - 13 * mm
    for bloc in range(2):
        c.setFillColor(GRIS)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(colx[bloc], yy0, titols[bloc])
        yy = yy0 - 5 * mm
        marcadors = marques if bloc == 0 else marques2
        for j, text in enumerate(llistes[bloc]):
            c.setFillColor(INDIGO)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(colx[bloc], yy, marcadors[j])
            c.setFillColor(TINTA)
            c.setFont("Helvetica", 8)
            c.drawString(colx[bloc] + 6 * mm, yy, text[:56])
            yy -= 6.5 * mm

    yy = yy0 - 5 * mm - 5 * 6.5 * mm - 4 * mm
    c.setFillColor(GRIS)
    c.setFont("Helvetica-Bold", 8.8)
    c.drawString(M, yy, "Les vostres respostes:")
    xr = M + 42 * mm
    for i in range(1, 6):
        c.setFillColor(TINTA)
        c.setFont("Helvetica", 8.8)
        c.drawString(xr, yy, f"{i} →")
        c.rect(xr + 8 * mm, yy - 1.5 * mm, 6 * mm, 5 * mm, fill=0, stroke=1)
        xr += 18 * mm

    peu(c, "Repara i Roda 360 · B0 · Full de l'alumnat 1/2")


def pagina2_alumnat(c):
    capcalera(c, "ACTIVITAT AUTÒNOMA · Full de l'alumnat (2/2)", "B0 · Repara i Roda 360")

    y = H - M - 18 * mm
    h2(c, M, y, "Part 3 — Parts de la bicicleta (18 min)")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 8.8)
    c.drawString(M, y - 6 * mm,
                 "1) Sense mirar la imatge, escriviu (5') totes les parts que recordeu:")

    yy = y - 12 * mm
    for _ in range(4):
        liniah(c, M, yy, W - 2 * M)
        yy -= 6 * mm

    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8.8)
    c.drawString(M, yy - 2 * mm, "Quantes n'heu escrit en total:")
    c.rect(M + 62 * mm, yy - 3.5 * mm, 12 * mm, 5.5 * mm, fill=0, stroke=1)

    yy -= 14 * mm
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 8.8)
    c.drawString(M, yy, "2) Ara mireu la imatge projectada i marqueu quantes n'heu encertat:")
    c.setFillColor(GRIS)
    c.drawString(M, yy - 8 * mm, "Encertades:")
    c.rect(M + 24 * mm, yy - 9.5 * mm, 12 * mm, 5.5 * mm, fill=0, stroke=1)
    c.drawString(M + 45 * mm, yy - 8 * mm, "Noves que no coneixia:")
    c.rect(M + 90 * mm, yy - 9.5 * mm, 12 * mm, 5.5 * mm, fill=0, stroke=1)

    img_top = yy - 18 * mm
    img_h = 78 * mm
    img_w = W - 2 * M
    img_fit(c, POSTER, M, img_top - img_h, img_w, img_h)

    y2 = img_top - img_h - 10 * mm
    h2(c, M, y2, "Part 4 — Tancament (5 min)")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 8.8)
    c.drawString(M, y2 - 6 * mm, "El que més m'ha costat avui ha estat...")
    liniah(c, M, y2 - 12 * mm, W - 2 * M)
    c.drawString(M, y2 - 18 * mm, "Una part de la bici que no coneixia i ara sí és...")
    liniah(c, M, y2 - 24 * mm, W - 2 * M)

    peu(c, "Repara i Roda 360 · B0 · Full de l'alumnat 2/2 — entrega-ho en sortir")


def pagina3_docent(c):
    capcalera(c, "ACTIVITAT AUTÒNOMA · Full del/de la docent substitut/a", "B0 · Repara i Roda 360")

    y = H - M - 18 * mm
    c.setFillColor(TINTA)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(M, y, "El teu paper: repartir el full, projectar les imatges, controlar el")
    c.drawString(M, y - 5 * mm, "temps (15' / 10' / 18' / 5') i donar aquestes solucions NOMÉS quan")
    c.drawString(M, y - 10 * mm, "cada parella ja hagi escrit les seves respostes. No cal saber res")
    c.drawString(M, y - 15 * mm, "de bicicletes: tot hi és aquí sota.")

    y -= 24 * mm
    h2(c, M, y, "Imatges a projectar")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 8.8)
    c.drawString(M, y - 6 * mm, "Part 1: Recursos/imatges/eines/1.jpg … 8.jpg (ja incrustades a la pàg. 1)")
    c.drawString(M, y - 11 * mm, "Part 3: pòster de parts de la bicicleta (ja incrustat a la pàg. 2)")

    y -= 20 * mm
    h2(c, M, y, "Solució Part 1 — Eines")
    yy = y - 7 * mm
    c.setFont("Helvetica", 8.3)
    for i, (nom, us) in enumerate(EINES, start=1):
        c.setFillColor(INDIGO)
        c.setFont("Helvetica-Bold", 8.3)
        c.drawString(M, yy, f"{i}.")
        c.setFillColor(TINTA)
        c.setFont("Helvetica-Bold", 8.3)
        c.drawString(M + 6 * mm, yy, nom)
        c.setFillColor(GRIS)
        c.setFont("Helvetica", 8)
        c.drawString(M + 48 * mm, yy, us[:70])
        yy -= 5.5 * mm

    y = yy - 5 * mm
    h2(c, M, y, "Solució Part 2 — Troba el perill")
    c.setFillColor(TINTA)
    c.setFont("Helvetica-Bold", 9)
    resposta_text = "  ·  ".join(f"{k} → {v}" for k, v in RESPOSTA.items())
    c.drawString(M, y - 7 * mm, resposta_text)

    y -= 15 * mm
    h2(c, M, y, "Part 3 i 4")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 8.8)
    c.drawString(M, y - 6 * mm,
                 "No cal cap solució: la imatge projectada ja mostra tots els noms. Els")
    c.drawString(M, y - 11 * mm,
                 "alumnes es corregeixen sols. Si algú pregunta res que no és en aquest full,")
    c.drawString(M, y - 16 * mm,
                 "digues «ho preguntem dijous a la professora/professor titular».")

    y -= 24 * mm
    h2(c, M, y, "En acabar")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 8.8)
    c.drawString(M, y - 6 * mm,
                 "Recull tots els fulls amb els noms de les parelles i deixa'ls a la taula")
    c.drawString(M, y - 11 * mm, "del/de la docent titular (o entrega'ls al departament).")

    peu(c, "Repara i Roda 360 · B0 · Full del/de la docent substitut/a")


def build():
    c = canvas.Canvas(SORTIDA, pagesize=A4)
    c.setTitle("Activitat autònoma per a substitut/a — B0")
    pagina1_alumnat(c)
    c.showPage()
    pagina2_alumnat(c)
    c.showPage()
    pagina3_docent(c)
    c.save()
    print("PDF generat:", SORTIDA)


if __name__ == "__main__":
    build()
