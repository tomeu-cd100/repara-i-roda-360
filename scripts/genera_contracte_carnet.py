#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contracte d'aula + carnet, un full per assignatura, en PDF (A4).

- Bicicletes: normes del taller + contracte + carnet d'eines.
- Maker: normes de l'aula maker + contracte + carnet de màquina (làser/3D/360/VR).

Sortida: Normativa/Contracte_carnet_bicicletes.pdf i Contracte_carnet_maker.pdf
Ús:  py -3.11 scripts/genera_contracte_carnet.py   ·   Requereix: reportlab
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

AQUI = os.path.dirname(os.path.abspath(__file__))
NORM = os.path.normpath(os.path.join(AQUI, "..", "Normativa"))
W, H = A4
M = 15 * mm
INDIGO = colors.HexColor("#5b5bd6")
CIAN = colors.HexColor("#12a594")
GRIS = colors.HexColor("#5a6079")
TINTA = colors.HexColor("#14172a")
LINIA = colors.HexColor("#c3c7d9")

NORMES_BICI = [
    "Espera a l'entrada fins que el professor et doni permís per entrar.",
    "Respecta les explicacions: no parlis mentre s'explica.",
    "Arremanga't la màniga llarga; res que pengi prop de les peces.",
    "Fes servir cada eina per a la seva funció. No són joguines.",
    "Les màquines-eina només s'usen amb permís i supervisió.",
    "No mengis ni beguis dins del taller.",
    "No posis en perill els companys: dona les eines a mà, no les llancis.",
    "No toquis les bicis ni el material d'altres sense permís.",
    "En acabar, recull-ho tot i deixa el lloc net (restes amb raspall).",
    "No surtis del taller sense permís del professor.",
]
NORMES_MAKER = [
    "Làser i impressora 3D: només amb el carnet de màquina i sota supervisió.",
    "Làser: no tallis materials no autoritzats; ventilació activa; no la deixis sola.",
    "Impressora 3D: no toquis les parts calentes ni obris la porta en marxa.",
    "Ulleres de protecció i guants quan calgui.",
    "Deixa cada màquina i l'ordinador ordenats en acabar.",
]
CARNETS_MAKER = [
    (colors.HexColor("#e5484d"), "Operador/a làser (xTool S1)"),
    (colors.HexColor("#f5a623"), "Operador/a impressora 3D (P2S)"),
    (colors.HexColor("#30a46c"), "Operador/a càmera 360"),
    (colors.HexColor("#3e63dd"), "Usuari/ària VR / guia"),
]


def h2(c, x, y, text, color):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x, y, text)
    c.setStrokeColor(color)
    c.setLineWidth(1)
    c.line(x, y - 1.8 * mm, W - M, y - 1.8 * mm)


def llista(c, y, items):
    for n, it in enumerate(items, 1):
        c.setFillColor(INDIGO)
        c.setFont("Helvetica-Bold", 9.3)
        c.drawString(M, y, f"{n}.")
        c.setFillColor(TINTA)
        c.setFont("Helvetica", 9.3)
        c.drawString(M + 7 * mm, y, it)
        y -= 6.6 * mm
    return y


def contracte(c, y):
    c.setStrokeColor(INDIGO)
    c.setLineWidth(1.2)
    c.roundRect(M, y - 26 * mm, W - 2 * M, 26 * mm, 4, fill=0, stroke=1)
    c.setFillColor(INDIGO)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M + 4 * mm, y - 6 * mm, "CONTRACTE D'AULA")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 9)
    c.drawString(M + 4 * mm, y - 12 * mm,
                 "Em comprometo a seguir aquestes normes tot el curs, per la meva seguretat i la")
    c.drawString(M + 4 * mm, y - 16.5 * mm, "dels meus companys.")
    c.setStrokeColor(LINIA)
    c.setLineWidth(0.7)
    c.line(M + 4 * mm, y - 22 * mm, M + 88 * mm, y - 22 * mm)
    c.line(W - M - 52 * mm, y - 22 * mm, W - M - 4 * mm, y - 22 * mm)
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8)
    c.drawString(M + 4 * mm, y - 25 * mm, "Signatura de l'alumne/a")
    c.drawString(W - M - 52 * mm, y - 25 * mm, "Data")
    return y - 32 * mm


def capcalera(c, titol, color):
    c.setFillColor(color)
    c.roundRect(M, H - M - 10 * mm, W - 2 * M, 10 * mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M + 4 * mm, H - M - 7 * mm, titol)
    c.setFont("Helvetica", 8)
    c.drawRightString(W - M - 4 * mm, H - M - 7 * mm, "Repara i Roda 360 · 4t ESO")
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 9)
    c.drawString(M, H - M - 17 * mm, "Nom: ____________________________________________  Data: ____/____/______")


def pagina_bici(c):
    capcalera(c, "TALLER DE BICICLETES  ·  Contracte i carnet d'eines", INDIGO)
    y = H - M - 24 * mm
    h2(c, M, y, "Normes del taller de bicicletes", INDIGO)
    y = llista(c, y - 6.5 * mm, NORMES_BICI)
    y = contracte(c, y - 2 * mm)

    # carnet d'eines
    c.setStrokeColor(TINTA)
    c.setLineWidth(1.4)
    c.roundRect(M, y - 30 * mm, W - 2 * M, 30 * mm, 4, fill=0, stroke=1)
    c.setFillColor(INDIGO)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M + 4 * mm, y - 7 * mm, "CARNET D'EINES")
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8.5)
    c.drawString(M + 4 * mm, y - 13 * mm,
                 "Per obtenir-lo (checkpoint pràctic): tria l'eina correcta per a una tasca, fes-la")
    c.drawString(M + 4 * mm, y - 17.5 * mm,
                 "servir bé i respon 1 pregunta de seguretat.")
    c.setStrokeColor(colors.HexColor("#8a90ab"))
    c.setLineWidth(1.1)
    c.rect(M + 4 * mm, y - 26 * mm, 5 * mm, 5 * mm, fill=0, stroke=1)
    c.setFillColor(TINTA)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M + 12 * mm, y - 25 * mm, "CARNET D'EINES OBTINGUT")
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 9)
    c.drawString(W - M - 45 * mm, y - 25 * mm, "data ____/____/______")
    c.save()


def pagina_maker(c):
    capcalera(c, "AULA MAKER  ·  Contracte i carnet de màquina", CIAN)
    y = H - M - 24 * mm
    h2(c, M, y, "Normes de l'aula maker (làser i impressió 3D)", CIAN)
    y = llista(c, y - 6.5 * mm, NORMES_MAKER)
    y = contracte(c, y - 2 * mm)

    # carnet de màquina (4 nivells)
    c.setStrokeColor(TINTA)
    c.setLineWidth(1.4)
    c.roundRect(M, y - 44 * mm, W - 2 * M, 44 * mm, 4, fill=0, stroke=1)
    c.setFillColor(CIAN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M + 4 * mm, y - 7 * mm, "CARNET DE MÀQUINA")
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8.3)
    c.drawString(M + 4 * mm, y - 12.5 * mm,
                 "Cada màquina té el seu checkpoint (3 preguntes + demostració). Sense carnet no s'opera.")
    yy = y - 19 * mm
    for col, nom in CARNETS_MAKER:
        c.setFillColor(col)
        c.circle(M + 7 * mm, yy + 1 * mm, 1.8 * mm, fill=1, stroke=0)
        c.setFillColor(TINTA)
        c.setFont("Helvetica-Bold", 9.3)
        c.drawString(M + 11 * mm, yy, nom)
        c.setFillColor(GRIS)
        c.setFont("Helvetica", 8.5)
        c.drawString(W - M - 45 * mm, yy, "data ____/____/______")
        c.setStrokeColor(colors.HexColor("#8a90ab"))
        c.setLineWidth(1)
        c.rect(W - M - 9 * mm, yy - 1 * mm, 4.5 * mm, 4.5 * mm, fill=0, stroke=1)
        yy -= 6.6 * mm
    c.save()


def build():
    c = canvas.Canvas(os.path.join(NORM, "Contracte_carnet_bicicletes.pdf"), pagesize=A4)
    c.setTitle("Contracte i carnet d'eines — Taller de bicicletes")
    pagina_bici(c)
    print("PDF generat: Contracte_carnet_bicicletes.pdf")

    c = canvas.Canvas(os.path.join(NORM, "Contracte_carnet_maker.pdf"), pagesize=A4)
    c.setTitle("Contracte i carnet de màquina — Aula maker")
    pagina_maker(c)
    print("PDF generat: Contracte_carnet_maker.pdf")


if __name__ == "__main__":
    build()
