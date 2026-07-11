#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normes de seguretat + contracte d'aula en PDF (A4, 1 pàgina).

El full que l'alumnat llegeix i signa a la SA0 (contracte d'aula). Sortida:
Normativa/Normes_contracte.pdf

Ús:  py -3.11 scripts/genera_normes_contracte.py   ·   Requereix: reportlab
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

AQUI = os.path.dirname(os.path.abspath(__file__))
SORTIDA = os.path.normpath(os.path.join(AQUI, "..", "Normativa", "Normes_contracte.pdf"))
W, H = A4
M = 15 * mm
INDIGO = colors.HexColor("#5b5bd6")
CIAN = colors.HexColor("#12a594")
GRIS = colors.HexColor("#5a6079")
TINTA = colors.HexColor("#14172a")
LINIA = colors.HexColor("#c3c7d9")

TALLER = [
    "Espera a l'entrada fins que el professor et doni permís per entrar.",
    "Respecta les explicacions: no parlis mentre s'explica.",
    "Arremanga't la màniga llarga; res que pengi (bufandes, cordons) prop de les peces.",
    "Fes servir cada eina per a la seva funció. No són joguines.",
    "Les màquines-eina només s'usen amb permís i supervisió del professor.",
    "No mengis ni beguis dins del taller.",
    "No posis en perill els companys corrent, jugant o llançant eines: dona-les a mà.",
    "No toquis les bicis ni el material d'altres companys sense permís.",
    "En acabar, recull-ho tot i deixa el lloc net (les restes, amb raspall, mai amb la mà).",
    "No surtis del taller sense permís del professor.",
]
MAKER = [
    "Làser i impressora 3D: només amb el carnet de màquina i sota supervisió.",
    "Làser: no tallis materials no autoritzats; ventilació activa; no la deixis sola.",
    "Impressora 3D: no toquis les parts calentes ni obris la porta en marxa.",
    "Ulleres de protecció i guants quan calgui.",
]


def h2(c, x, y, text, color):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x, y, text)
    c.setStrokeColor(color)
    c.setLineWidth(1)
    c.line(x, y - 1.8 * mm, W - M, y - 1.8 * mm)


def llista(c, y, items, start=1):
    c.setFont("Helvetica", 9.3)
    n = start
    for it in items:
        c.setFillColor(INDIGO)
        c.setFont("Helvetica-Bold", 9.3)
        c.drawString(M, y, f"{n}.")
        c.setFillColor(TINTA)
        c.setFont("Helvetica", 9.3)
        c.drawString(M + 7 * mm, y, it)
        y -= 6.6 * mm
        n += 1
    return y, n


def build():
    c = canvas.Canvas(SORTIDA, pagesize=A4)
    c.setTitle("Normes de seguretat i contracte d'aula — Repara i Roda 360")

    c.setFillColor(INDIGO)
    c.roundRect(M, H - M - 10 * mm, W - 2 * M, 10 * mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13.5)
    c.drawString(M + 4 * mm, H - M - 7 * mm, "NORMES DE SEGURETAT  ·  Contracte d'aula")
    c.setFont("Helvetica", 8)
    c.drawRightString(W - M - 4 * mm, H - M - 7 * mm, "Repara i Roda 360 · 4t ESO")

    y = H - M - 17 * mm
    c.setFillColor(GRIS)
    c.setFont("Helvetica-Oblique", 8.6)
    c.drawString(M, y, "La seguretat és l'única cosa innegociable. Llegeix-les, entén per què hi són i signa a baix.")

    y -= 9 * mm
    h2(c, M, y, "Al taller de bicicletes", INDIGO)
    y -= 6.5 * mm
    y, _ = llista(c, y, TALLER)

    y -= 3 * mm
    h2(c, M, y, "A l'aula maker (làser i impressió 3D)", CIAN)
    y -= 6.5 * mm
    y, _ = llista(c, y, MAKER, start=11)

    # contracte
    y -= 4 * mm
    c.setStrokeColor(INDIGO)
    c.setLineWidth(1.2)
    c.roundRect(M, y - 34 * mm, W - 2 * M, 34 * mm, 4, fill=0, stroke=1)
    c.setFillColor(INDIGO)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M + 4 * mm, y - 7 * mm, "CONTRACTE D'AULA")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 9.2)
    c.drawString(M + 4 * mm, y - 14 * mm,
                 "Em comprometo a seguir aquestes normes tot el curs, per la meva")
    c.drawString(M + 4 * mm, y - 19 * mm,
                 "seguretat i la dels meus companys.")
    c.setStrokeColor(LINIA)
    c.setLineWidth(0.7)
    c.line(M + 4 * mm, y - 28 * mm, M + 90 * mm, y - 28 * mm)
    c.line(W - M - 55 * mm, y - 28 * mm, W - M - 4 * mm, y - 28 * mm)
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8)
    c.drawString(M + 4 * mm, y - 31 * mm, "Signatura de l'alumne/a")
    c.drawString(W - M - 55 * mm, y - 31 * mm, "Data")

    c.save()
    print("PDF generat:", SORTIDA)


if __name__ == "__main__":
    build()
