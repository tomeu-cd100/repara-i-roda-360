#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el diari setmanal de l'alumnat en PDF (A4, 2 pàgines a doble cara).

Cara A = taller de bicicletes · Cara B = aula maker. Pensat per imprimir i
que l'alumnat l'ompli a mà al taller. Sortida:
Programació didàctica/Diari_setmanal_paper.pdf

Ús:  py -3.11 scripts/genera_diari_setmanal.py
Requereix: reportlab
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

AQUI = os.path.dirname(os.path.abspath(__file__))
SORTIDA = os.path.normpath(os.path.join(AQUI, "..", "Programació didàctica",
                                        "Diari_setmanal_paper.pdf"))

W, H = A4
M = 16 * mm
VERD = colors.HexColor("#12a594")   # taller
BLAU = colors.HexColor("#5b5bd6")   # maker (indigo)
GRIS = colors.HexColor("#5a6079")
LINIA = colors.HexColor("#c3c7d9")


def barra(c, y, text, color):
    c.setFillColor(color)
    c.roundRect(M, y, W - 2 * M, 9 * mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M + 4 * mm, y + 2.6 * mm, text)


def etiqueta(c, x, y, text, mida=9.5):
    c.setFillColor(colors.HexColor("#14172a"))
    c.setFont("Helvetica-Bold", mida)
    c.drawString(x, y, text)


def gris(c, x, y, text, mida=8.5):
    c.setFillColor(GRIS)
    c.setFont("Helvetica", mida)
    c.drawString(x, y, text)


def ratlles(c, x, y, ample, n=1, gap=7 * mm):
    c.setStrokeColor(LINIA)
    c.setLineWidth(0.6)
    for i in range(n):
        yy = y - i * gap
        c.line(x, yy, x + ample, yy)


def caixa(c, x, y, w, h, etq=None):
    c.setStrokeColor(LINIA)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 4, fill=0, stroke=1)
    if etq:
        c.setFillColor(GRIS)
        c.setFont("Helvetica-Oblique", 7.5)
        c.drawString(x + 2 * mm, y + h - 4 * mm, etq)


def quadre(c, x, y, costat=3.2 * mm):
    c.setStrokeColor(colors.HexColor("#8a90ab"))
    c.setLineWidth(0.8)
    c.rect(x, y, costat, costat, fill=0, stroke=1)


def check(c, x, y, text):
    quadre(c, x, y)
    c.setFillColor(colors.HexColor("#14172a"))
    c.setFont("Helvetica", 8.5)
    c.drawString(x + 4.5 * mm, y + 0.3 * mm, text)


def semafor(c, x, y):
    gris(c, x, y + 6 * mm, "Com m'ha anat avui?")
    dades = [(colors.HexColor("#e5484d"), "M'ha costat"),
             (colors.HexColor("#f5a623"), "Amb ajuda"),
             (colors.HexColor("#30a46c"), "Sol/a")]
    cx = x
    for col, lbl in dades:
        c.setFillColor(col)
        c.circle(cx + 3 * mm, y + 1.5 * mm, 3 * mm, fill=1, stroke=0)
        c.setFillColor(GRIS)
        c.setFont("Helvetica", 7.5)
        c.drawString(cx + 7 * mm, y + 0.4 * mm, lbl)
        cx += 33 * mm


def capcalera_dades(c, y):
    gris(c, M, y, "Nom:")
    ratlles(c, M + 12 * mm, y - 1, 55 * mm)
    gris(c, M + 72 * mm, y, "Setmana:")
    ratlles(c, M + 92 * mm, y - 1, 18 * mm)
    gris(c, M + 114 * mm, y, "SA:")
    ratlles(c, M + 122 * mm, y - 1, 14 * mm)
    gris(c, M + 140 * mm, y, "Data:")
    ratlles(c, M + 152 * mm, y - 1, 26 * mm)


def cara_a(c):
    barra(c, H - M - 9 * mm, "DIARI SETMANAL  ·  Taller de bicicletes", VERD)
    y = H - M - 20 * mm
    capcalera_dades(c, y)
    y -= 9 * mm
    check(c, M, y, "Treballo sol/a")
    check(c, M + 40 * mm, y, "Amb parella  —  company/a:")
    ratlles(c, M + 108 * mm, y + 0.5 * mm, 40 * mm)
    gris(c, M + 152 * mm, y, "Bici núm:")
    ratlles(c, M + 172 * mm, y + 0.5 * mm, 6 * mm)

    y -= 11 * mm
    etiqueta(c, M, y, "1. Què he fet avui?")
    ratlles(c, M, y - 7 * mm, W - 2 * M, n=3)

    y -= 30 * mm
    etiqueta(c, M, y, "2. Eines que he fet servir:")
    y -= 7 * mm
    e = ["claus Allen", "tornavisos", "claus fixes", "desmuntables",
         "tronxacadenes", "bomba/manòmetre"]
    for i, nom in enumerate(e):
        col = i % 3
        fila = i // 3
        check(c, M + col * 58 * mm, y - fila * 7 * mm, nom)

    y -= 22 * mm
    etiqueta(c, M, y, "3. Passos que he seguit:")
    for i in range(3):
        gris(c, M, y - 7 * mm - i * 7 * mm, f"{i + 1}.")
        ratlles(c, M + 6 * mm, y - 7 * mm - i * 7 * mm, W - 2 * M - 6 * mm)

    y -= 32 * mm
    etiqueta(c, M, y, "4. Què m'ha costat i com ho he resolt?")
    ratlles(c, M, y - 7 * mm, W - 2 * M, n=2)

    y -= 22 * mm
    etiqueta(c, M, y, "5. Esquema o foto")
    caixa(c, M, y - 42 * mm, W - 2 * M, 38 * mm, "dibuixa la peça o l'avaria (o enganxa una foto)")

    semafor(c, M, M + 4 * mm)
    c.showPage()


def cara_b(c):
    barra(c, H - M - 9 * mm, "DIARI SETMANAL  ·  Aula maker", BLAU)
    y = H - M - 22 * mm

    etiqueta(c, M, y, "1. Què he dissenyat o fabricat aquesta setmana?")
    ratlles(c, M, y - 7 * mm, W - 2 * M, n=2)

    y -= 24 * mm
    etiqueta(c, M, y, "2. Màquina o eina digital:")
    y -= 7 * mm
    for i, nom in enumerate(["Làser xTool", "Impressora 3D",
                             "Inkscape / Tinkercad", "Càmera 360 / VR"]):
        col = i % 2
        fila = i // 2
        check(c, M + col * 70 * mm, y - fila * 7 * mm, nom)

    y -= 18 * mm
    etiqueta(c, M, y, "3. Croquis o captura del disseny")
    caixa(c, M, y - 52 * mm, W - 2 * M, 48 * mm, "amb les mides si en té")

    y -= 60 * mm
    etiqueta(c, M, y, "4. Resultat:")
    y -= 7 * mm
    check(c, M, y, "Funciona i ja és al taller")
    check(c, M, y - 7 * mm, "Funciona però es pot millorar")
    check(c, M, y - 14 * mm, "Cal repetir-lo")
    gris(c, M + 52 * mm, y - 14 * mm, "per què?")
    ratlles(c, M + 68 * mm, y - 14 * mm + 0.5 * mm, W - 2 * M - 68 * mm)

    y -= 26 * mm
    etiqueta(c, M, y, "5. Una cosa que he après aquesta setmana:")
    ratlles(c, M, y - 7 * mm, W - 2 * M, n=2)

    semafor(c, M, M + 4 * mm)
    c.showPage()


def build():
    c = canvas.Canvas(SORTIDA, pagesize=A4)
    c.setTitle("Diari setmanal — Repara i Roda 360")
    cara_a(c)
    cara_b(c)
    c.save()
    print("PDF generat:", SORTIDA)


if __name__ == "__main__":
    build()
