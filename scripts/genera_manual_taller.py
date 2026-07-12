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
    c.drawString(M + 5 * mm, y + 3.7 * mm, f"{prefix}{icona}  {titol}")
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


def main():
    c = canvas.Canvas(SORTIDA, pagesize=A4)
    c.setTitle("Manual ràpid de taller de bicicletes")
    portada(c)
    c.save()
    print(f"Manual generat a {SORTIDA}")


if __name__ == "__main__":
    main()
