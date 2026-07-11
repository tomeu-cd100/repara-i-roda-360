#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full de resposta de la gimcana d'eines i seguretat (B0) en PDF (A4, 1 pàgina).

L'omple cada parella durant la gimcana. Sortida: Avaluació/Full_gimcana_alumne.pdf
Ús:  py -3.11 scripts/genera_full_gimcana.py   ·   Requereix: reportlab
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

AQUI = os.path.dirname(os.path.abspath(__file__))
SORTIDA = os.path.normpath(os.path.join(AQUI, "..", "Avaluació", "Full_gimcana_alumne.pdf"))
W, H = A4
M = 16 * mm
INDIGO = colors.HexColor("#5b5bd6")
GRIS = colors.HexColor("#5a6079")
TINTA = colors.HexColor("#14172a")
LINIA = colors.HexColor("#c3c7d9")


def liniah(c, x, y, ample):
    c.setStrokeColor(LINIA)
    c.setLineWidth(0.6)
    c.line(x, y, x + ample, y)


def quadre(c, x, y, costat=4 * mm):
    c.setStrokeColor(colors.HexColor("#8a90ab"))
    c.setLineWidth(0.9)
    c.rect(x, y, costat, costat, fill=0, stroke=1)


def h2(c, x, y, text):
    c.setFillColor(INDIGO)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y, text)
    liniah(c, x, y - 2 * mm, W - 2 * M - (x - M))


def build():
    c = canvas.Canvas(SORTIDA, pagesize=A4)
    c.setTitle("Full de resposta de la gimcana — B0")

    c.setFillColor(INDIGO)
    c.roundRect(M, H - M - 10 * mm, W - 2 * M, 10 * mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(M + 4 * mm, H - M - 7 * mm, "GIMCANA D'EINES I SEGURETAT  ·  Full de resposta")
    c.setFont("Helvetica", 8)
    c.drawRightString(W - M - 4 * mm, H - M - 7 * mm, "B0 · Repara i Roda 360")

    y = H - M - 18 * mm
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 9.5)
    c.drawString(M, y, "Nom:")
    liniah(c, M + 13 * mm, y - 1, 78 * mm)
    c.drawString(M + 98 * mm, y, "Parella:")
    liniah(c, M + 118 * mm, y - 1, W - M - (M + 118 * mm))

    # Estació 1
    y -= 11 * mm
    h2(c, M, y, "Estació 1 — Cada eina, la seva feina")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 9.5)
    c.drawString(M, y - 7 * mm, "Escriu el NOM de l'eina de cada número de la imatge projectada:")
    yy = y - 14 * mm
    for fila in range(4):
        for col in range(2):
            n = fila * 2 + col + 1
            x = M + col * 92 * mm
            c.setFillColor(INDIGO)
            c.setFont("Helvetica-Bold", 9.5)
            c.drawString(x, yy, f"{n}.")
            liniah(c, x + 6 * mm, yy - 1, 78 * mm)
        yy -= 8 * mm

    # Estació 2
    y = yy - 4 * mm
    h2(c, M, y, "Estació 2 — Troba el perill")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 9.5)
    c.drawString(M, y - 7 * mm, "Per a cada situació perillosa, escriu la lletra de la solució correcta:")
    yy = y - 14 * mm
    for i in range(5):
        c.setFillColor(INDIGO)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(M, yy, f"Situació {i + 1} →")
        quadre(c, M + 26 * mm, yy - 1 * mm)
        yy -= 7.5 * mm

    # Estació 3
    y = yy - 3 * mm
    h2(c, M, y, "Estació 3 — La pressió correcta")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 9.5)
    c.drawString(M, y - 7 * mm, "Pressió que diu el flanc del pneumàtic:")
    liniah(c, M + 68 * mm, y - 7 * mm - 1, 30 * mm)
    c.drawString(M + 100 * mm, y - 7 * mm, "bar/psi")
    quadre(c, M + 128 * mm, y - 7 * mm - 1 * mm)
    c.drawString(M + 135 * mm, y - 7 * mm, "inflada")

    # Estació 4
    y -= 16 * mm
    h2(c, M, y, "Estació 4 — Parts de la bici (1 minut)")
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 9.5)
    c.drawString(M, y - 7 * mm, "Parts que he sabut anomenar en 1 minut:")
    liniah(c, M + 70 * mm, y - 7 * mm - 1, 25 * mm)

    # Carnet
    y -= 16 * mm
    quadre(c, M, y - 1 * mm, 5 * mm)
    c.setFillColor(TINTA)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M + 8 * mm, y, "CARNET D'EINES OBTINGUT")
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 9)
    c.drawString(M + 75 * mm, y, "data ____/____/______")

    c.save()
    print("PDF generat:", SORTIDA)


if __name__ == "__main__":
    build()
