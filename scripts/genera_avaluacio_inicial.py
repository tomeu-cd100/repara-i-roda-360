#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Avaluació inicial de l'alumnat (SA0) en PDF (A4, 1 pàgina).

El full que omple cada alumne/a a la SA0: sense nota, per situar el punt de
partida. Es torna a mirar al juny. Sortida:
Avaluació/Avaluacio_inicial_alumne.pdf

Ús:  py -3.11 scripts/genera_avaluacio_inicial.py   ·   Requereix: reportlab
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

AQUI = os.path.dirname(os.path.abspath(__file__))
SORTIDA = os.path.normpath(os.path.join(AQUI, "..", "Avaluació",
                                        "Avaluacio_inicial_alumne.pdf"))
W, H = A4
M = 16 * mm
INDIGO = colors.HexColor("#5b5bd6")
GRIS = colors.HexColor("#5a6079")
TINTA = colors.HexColor("#14172a")
LINIA = colors.HexColor("#c3c7d9")

PARAULES = ["cambra", "desviador", "maneta de fre", "pinyó", "radi",
            "potència", "tija de seient", "pastilla de fre", "M-check", "tolerància"]


def ratlles(c, x, y, ample, n=1, gap=8 * mm):
    c.setStrokeColor(LINIA)
    c.setLineWidth(0.6)
    for i in range(n):
        c.line(x, y - i * gap, x + ample, y - i * gap)


def etiqueta(c, x, y, text, mida=10):
    c.setFillColor(TINTA)
    c.setFont("Helvetica-Bold", mida)
    c.drawString(x, y, text)


def quadre(c, x, y, costat=3.6 * mm):
    c.setStrokeColor(colors.HexColor("#8a90ab"))
    c.setLineWidth(0.9)
    c.rect(x, y, costat, costat, fill=0, stroke=1)


def build():
    c = canvas.Canvas(SORTIDA, pagesize=A4)
    c.setTitle("Avaluació inicial de l'alumnat — Repara i Roda 360")

    c.setFillColor(INDIGO)
    c.roundRect(M, H - M - 10 * mm, W - 2 * M, 10 * mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(M + 4 * mm, H - M - 7 * mm, "AVALUACIÓ INICIAL  ·  El meu punt de partida")

    y = H - M - 18 * mm
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 9)
    c.drawString(M, y, "Nom:")
    ratlles(c, M + 12 * mm, y - 1, 100 * mm)
    c.drawString(M + 118 * mm, y, "Data:")
    ratlles(c, M + 131 * mm, y - 1, 35 * mm)

    y -= 8 * mm
    c.setFillColor(GRIS)
    c.setFont("Helvetica-Oblique", 8.6)
    c.drawString(M, y, "Sense nota: és per saber d'on partim. Sigues sincer/a — ho tornarem a mirar al juny.")

    # preguntes
    y -= 11 * mm
    etiqueta(c, M, y, "1. Tinc bici? La sé arreglar quan es punxa o falla alguna cosa?")
    ratlles(c, M, y - 7 * mm, W - 2 * M, n=2)
    y -= 24 * mm
    etiqueta(c, M, y, "2. Una cosa de la mecànica que em fa respecte o no he fet mai:")
    ratlles(c, M, y - 7 * mm, W - 2 * M, n=2)
    y -= 24 * mm
    etiqueta(c, M, y, "3. Què se'm dona bé i podria aportar a un equip del taller?")
    ratlles(c, M, y - 7 * mm, W - 2 * M, n=2)

    # vocabulari
    y -= 24 * mm
    etiqueta(c, M, y, "Les meves primeres paraules de mecànic/a")
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8.5)
    c.drawString(M, y - 5 * mm, "Marca les que ja saps què volen dir (de veritat!):")
    y -= 12 * mm
    for i, p in enumerate(PARAULES):
        col = i % 2
        fila = i // 2
        xx = M + col * 90 * mm
        yy = y - fila * 7 * mm
        quadre(c, xx, yy - 0.5 * mm)
        c.setFillColor(TINTA)
        c.setFont("Helvetica", 9.5)
        c.drawString(xx + 6 * mm, yy, p)

    # primera entrada del diari
    y -= 42 * mm
    etiqueta(c, M, y, "La meva primera entrada al diari  (Veig – Penso – Em pregunto)")
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8.5)
    c.drawString(M, y - 5 * mm, "Tria una eina o una màquina del taller i completa:")
    y -= 12 * mm
    for lbl in ["Veig:", "Penso que serveix per:", "Em pregunto:"]:
        c.setFillColor(TINTA)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(M, y, lbl)
        w = c.stringWidth(lbl, "Helvetica-Bold", 9.5)
        ratlles(c, M + w + 3 * mm, y - 0.5, W - 2 * M - w - 3 * mm)
        y -= 9 * mm

    c.save()
    print("PDF generat:", SORTIDA)


if __name__ == "__main__":
    build()
