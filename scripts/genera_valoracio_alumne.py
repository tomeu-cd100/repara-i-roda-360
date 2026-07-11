#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fitxa de valoració diària PER ALUMNE, tipus checklist, en PDF (A4, 2 per full).

Per a cada alumne/a: llista de coses que fa bé i que encara no té assolides,
amb dues caselles (Compleix / Encara no). Inclou les normes del taller. Pensat
per imprimir i marcar a mà cada dia al taller. Sortida:
Avaluació/Full_valoracio_alumne.pdf

Ús:  py -3.11 scripts/genera_valoracio_alumne.py
Requereix: reportlab
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

AQUI = os.path.dirname(os.path.abspath(__file__))
SORTIDA = os.path.normpath(os.path.join(AQUI, "..", "Avaluació",
                                        "Full_valoracio_alumne.pdf"))

W, H = A4
M = 12 * mm
INDIGO = colors.HexColor("#5b5bd6")
GRISBAR = colors.HexColor("#ecebff")
GRIS = colors.HexColor("#5a6079")
TINTA = colors.HexColor("#14172a")
LINIA = colors.HexColor("#c3c7d9")

COL_C = W - M - 40 * mm   # centre casella "Compleix"
COL_N = W - M - 13 * mm   # centre casella "Encara no"
TEXT_DRETA = W - M - 55 * mm

GRUPS = [
    ("SEGURETAT I NORMES DEL TALLER", [
        "Entra i treballa amb ordre (demana permís)",
        "Treballa de manera segura (roba, moviment)",
        "Fa servir bé les eines i les torna al lloc",
        "Deixa net i endreçat el lloc de treball",
        "Respecta els companys i el seu material",
    ]),
    ("FEINA D'AVUI (taller i/o aula maker)", [
        "Fa la tasca de reparació assignada",
        "Treballa amb autonomia",
        "Maker: avança en el disseny o la fabricació",
        "Maker: segueix la seguretat de làser / 3D",
    ]),
    ("ACTITUD I APRENENTATGE", [
        "Treballa bé amb la parella",
        "Persevera i demana ajuda quan cal",
        "Ha omplert el diari",
    ]),
]


def quadre(c, xc, y, costat=3.4 * mm):
    c.setStrokeColor(colors.HexColor("#8a90ab"))
    c.setLineWidth(0.9)
    c.rect(xc - costat / 2, y, costat, costat, fill=0, stroke=1)


def bloc(c, top):
    # capçalera
    c.setFillColor(INDIGO)
    c.roundRect(M, top - 8 * mm, W - 2 * M, 8 * mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(M + 3 * mm, top - 5.6 * mm, "VALORACIÓ DIÀRIA DE L'ALUMNE/A")
    c.setFont("Helvetica", 8)
    c.drawRightString(W - M - 3 * mm, top - 5.6 * mm, "Repara i Roda 360 · 4t ESO")

    y = top - 14 * mm
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 9)
    c.drawString(M, y, "Nom:")
    c.setStrokeColor(LINIA)
    c.setLineWidth(0.6)
    c.line(M + 11 * mm, y - 1, M + 92 * mm, y - 1)
    c.drawString(M + 98 * mm, y, "Data:")
    c.line(M + 111 * mm, y - 1, M + 140 * mm, y - 1)
    c.drawString(M + 145 * mm, y, "SA:")
    c.line(M + 153 * mm, y - 1, M + 167 * mm, y - 1)

    # capçaleres de columna
    y -= 7.5 * mm
    c.setFillColor(colors.HexColor("#30a46c"))
    c.setFont("Helvetica-Bold", 7.8)
    c.drawCentredString(COL_C, y, "COMPLEIX")
    c.setFillColor(colors.HexColor("#e5484d"))
    c.drawCentredString(COL_N, y, "ENCARA NO")

    y -= 2 * mm
    for titol, items in GRUPS:
        y -= 5.6 * mm
        c.setFillColor(GRISBAR)
        c.rect(M, y - 1 * mm, W - 2 * M, 5.2 * mm, fill=1, stroke=0)
        c.setFillColor(INDIGO)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(M + 2 * mm, y + 0.4 * mm, titol)
        for it in items:
            y -= 5.4 * mm
            c.setFillColor(TINTA)
            c.setFont("Helvetica", 8.6)
            c.drawString(M + 2 * mm, y, it)
            quadre(c, COL_C, y - 0.4 * mm)
            quadre(c, COL_N, y - 0.4 * mm)

    # observació + valoració global
    y -= 8 * mm
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8.5)
    c.drawString(M, y, "Observació del dia:")
    c.setStrokeColor(LINIA)
    c.line(M + 33 * mm, y - 1, W - M, y - 1)

    y -= 8 * mm
    c.setFillColor(GRIS)
    c.drawString(M, y + 1.2 * mm, "Global:")
    dades = [(colors.HexColor("#e5484d"), "Cal millorar"),
             (colors.HexColor("#f5a623"), "Bé, amb ajuda"),
             (colors.HexColor("#30a46c"), "Molt bé, sol/a")]
    cx = M + 18 * mm
    for col, lbl in dades:
        c.setFillColor(col)
        c.circle(cx, y + 2 * mm, 2.6 * mm, fill=1, stroke=0)
        c.setFillColor(GRIS)
        c.setFont("Helvetica", 7.6)
        c.drawString(cx + 4.5 * mm, y + 1.2 * mm, lbl)
        cx += 44 * mm


def build():
    c = canvas.Canvas(SORTIDA, pagesize=A4)
    c.setTitle("Valoració diària per alumne — Repara i Roda 360")
    bloc(c, H - M)              # meitat de dalt
    # línia de tall
    c.setStrokeColor(LINIA)
    c.setLineWidth(0.7)
    c.setDash(3, 3)
    c.line(M, H / 2, W - M, H / 2)
    c.setDash()
    c.setFillColor(GRIS)
    c.setFont("Helvetica-Oblique", 6.5)
    c.drawCentredString(W / 2, H / 2 + 1.2 * mm, "✂ retalla per la línia — dues fitxes per full")
    bloc(c, H / 2 - 4 * mm)     # meitat de baix
    c.save()
    print("PDF generat:", SORTIDA)


if __name__ == "__main__":
    build()
