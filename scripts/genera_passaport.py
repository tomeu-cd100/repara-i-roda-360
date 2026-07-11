#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Passaport de l'alumnat (carnets + fites) en PDF (A4, 2 per full A5).

Cada alumne/a hi va guanyant els carnets (eines, làser, 3D, 360, VR) i els
segells de fita de trimestre. Es retalla pel mig i es pot plastificar.
Sortida: Normativa/Passaport_alumne.pdf

Ús:  py -3.11 scripts/genera_passaport.py   ·   Requereix: reportlab
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

AQUI = os.path.dirname(os.path.abspath(__file__))
SORTIDA = os.path.normpath(os.path.join(AQUI, "..", "Normativa", "Passaport_alumne.pdf"))

W, H = A4
M = 12 * mm
INDIGO = colors.HexColor("#5b5bd6")
CIAN = colors.HexColor("#12a594")
GRIS = colors.HexColor("#5a6079")
TINTA = colors.HexColor("#14172a")
LINIA = colors.HexColor("#c3c7d9")

CARNETS = [
    (colors.HexColor("#8a90ab"), "Carnet d'eines"),
    (colors.HexColor("#e5484d"), "Operador/a làser (xTool S1)"),
    (colors.HexColor("#f5a623"), "Operador/a impressora 3D (P2S)"),
    (colors.HexColor("#30a46c"), "Operador/a càmera 360"),
    (colors.HexColor("#3e63dd"), "Usuari/ària VR / guia"),
]
FITES = [
    "T1 · Primera bici a punt",
    "T2 · Transmissions i taller",
    "T3 · Bici donada + exposició",
]


def dot(c, x, y, col, r=1.8 * mm):
    c.setFillColor(col)
    c.circle(x, y, r, fill=1, stroke=0)


def segell(c, x, y, w=16 * mm, h=8 * mm):
    c.setStrokeColor(INDIGO)
    c.setLineWidth(0.9)
    c.setDash(2, 2)
    c.roundRect(x, y, w, h, 2, fill=0, stroke=1)
    c.setDash()


def h2(c, x, y, text):
    c.setFillColor(INDIGO)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x, y, text.upper())
    c.setStrokeColor(LINIA)
    c.setLineWidth(0.6)
    c.line(x, y - 1.6 * mm, W - M, y - 1.6 * mm)


def bloc(c, top):
    x = M
    ample = W - 2 * M
    # marc de la targeta
    c.setStrokeColor(TINTA)
    c.setLineWidth(1.6)
    c.roundRect(x, top - 128 * mm, ample, 128 * mm, 5 * mm, fill=0, stroke=1)

    # capçalera
    c.setFillColor(TINTA)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(W / 2, top - 12 * mm, "PASSAPORT  ·  REPARA I RODA 360")
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(W / 2, top - 17 * mm, "Taller de bicicletes i aula maker · 4t ESO · curs 20___ / 20___")
    c.setStrokeColor(TINTA)
    c.setLineWidth(0.8)
    c.line(x + 6 * mm, top - 20 * mm, W - M - 6 * mm, top - 20 * mm)

    # dades
    y = top - 27 * mm
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 10)
    c.drawString(x + 6 * mm, y, "Nom:")
    c.setStrokeColor(LINIA)
    c.line(x + 20 * mm, y - 1, x + 110 * mm, y - 1)
    c.drawString(x + 118 * mm, y, "Grup:")
    c.line(x + 133 * mm, y - 1, W - M - 6 * mm, y - 1)

    # carnets
    y -= 9 * mm
    h2(c, x + 6 * mm, y, "Els meus carnets  (sense carnet no s'opera)")
    y -= 6 * mm
    for col, nom in CARNETS:
        dot(c, x + 9 * mm, y + 1 * mm, col)
        c.setFillColor(TINTA)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(x + 13 * mm, y, nom)
        c.setFillColor(GRIS)
        c.setFont("Helvetica", 8.5)
        c.drawString(x + 108 * mm, y, "data ___/___")
        segell(c, W - M - 22 * mm, y - 2.5 * mm)
        y -= 8.5 * mm

    # fites
    y -= 1 * mm
    h2(c, x + 6 * mm, y, "Fites del curs")
    y -= 8 * mm
    amp_f = (ample - 12 * mm - 8 * mm) / 3
    fx = x + 6 * mm
    for f in FITES:
        c.setStrokeColor(LINIA)
        c.setLineWidth(1)
        c.roundRect(fx, y - 10 * mm, amp_f, 14 * mm, 2 * mm, fill=0, stroke=1)
        c.setFillColor(TINTA)
        c.setFont("Helvetica-Bold", 7.6)
        c.drawCentredString(fx + amp_f / 2, y + 1 * mm, f.split(" · ")[0])
        c.setFillColor(GRIS)
        c.setFont("Helvetica", 6.6)
        c.drawCentredString(fx + amp_f / 2, y - 3 * mm, f.split(" · ")[1])
        segell(c, fx + amp_f / 2 - 8 * mm, y - 9 * mm, 16 * mm, 5 * mm)
        fx += amp_f + 4 * mm

    # certificat + peu
    y -= 16 * mm
    c.setStrokeColor(colors.HexColor("#8a90ab"))
    c.setLineWidth(1.1)
    c.rect(x + 6 * mm, y - 1 * mm, 4.5 * mm, 4.5 * mm, fill=0, stroke=1)
    c.setFillColor(TINTA)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(x + 13 * mm, y, "CERTIFICAT DE MECÀNIC/A JÚNIOR (final de curs)")

    c.setFillColor(GRIS)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(W / 2, top - 124 * mm, "«Reparat, provat i donat a Repara i Roda 360.»")


def build():
    c = canvas.Canvas(SORTIDA, pagesize=A4)
    c.setTitle("Passaport de l'alumnat — Repara i Roda 360")
    bloc(c, H - M)
    # línia de tall
    c.setStrokeColor(LINIA)
    c.setLineWidth(0.7)
    c.setDash(3, 3)
    c.line(M, H / 2, W - M, H / 2)
    c.setDash()
    c.setFillColor(GRIS)
    c.setFont("Helvetica-Oblique", 6.5)
    c.drawCentredString(W / 2, H / 2 + 1.2 * mm,
                        "retalla pel mig — 2 passaports per full; es pot plastificar")
    bloc(c, H / 2 - 5 * mm)
    c.save()
    print("PDF generat:", SORTIDA)


if __name__ == "__main__":
    build()
