#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fitxa de planificació i seguiment de sortida en bicicleta (B9) en PDF (A4, 2 pàgines).

Pàgina 1 = ABANS (dades, objectius, planificació, seguretat).
Pàgina 2 = DURANT i DESPRÉS (registre, reflexió, avaluació docent, documentació).
Adaptada de Recursos/Projecte Bicicletes/Annex1 SENSE rols rotatius de grup
(la sortida la lidera el/la docent; l'alumnat treballa en parella).

Sortida: Normativa/Fitxa_sortida_bici.pdf
Ús:  py -3.11 scripts/genera_fitxa_sortida.py   ·   Requereix: reportlab
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

AQUI = os.path.dirname(os.path.abspath(__file__))
SORTIDA = os.path.normpath(os.path.join(AQUI, "..", "Normativa", "Fitxa_sortida_bici.pdf"))
W, H = A4
M = 16 * mm
INDIGO = colors.HexColor("#5b5bd6")
CIAN = colors.HexColor("#0e9aa1")
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


def capsalera(c, titol, etiqueta):
    c.setFillColor(INDIGO)
    c.roundRect(M, H - M - 10 * mm, W - 2 * M, 10 * mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13.5)
    c.drawString(M + 4 * mm, H - M - 7 * mm, titol)
    c.setFont("Helvetica", 8)
    c.drawRightString(W - M - 4 * mm, H - M - 7 * mm, etiqueta)


def camp(c, x, y, etiqueta, ample_linia, ample_etiq=None):
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 9.5)
    c.drawString(x, y, etiqueta)
    dx = ample_etiq if ample_etiq else (c.stringWidth(etiqueta, "Helvetica", 9.5) + 3 * mm)
    liniah(c, x + dx, y - 1, ample_linia)


def check(c, x, y, text):
    quadre(c, x, y - 1 * mm, 3.5 * mm)
    c.setFillColor(TINTA)
    c.setFont("Helvetica", 9.5)
    c.drawString(x + 5.5 * mm, y, text)
    return c.stringWidth(text, "Helvetica", 9.5) + 11 * mm


def pagina1(c):
    capsalera(c, "FITXA DE SORTIDA EN BICICLETA  ·  Abans de sortir", "B9 · Repara i Roda 360")
    y = H - M - 18 * mm

    h2(c, M, y, "Dades generals")
    y -= 8 * mm
    camp(c, M, y, "Data:", 42 * mm)
    camp(c, M + 70 * mm, y, "Horari:", W - M - (M + 70 * mm) - 20 * mm)
    y -= 7 * mm
    camp(c, M, y, "Lloc de sortida:", W - 2 * M - 38 * mm)
    y -= 7 * mm
    camp(c, M, y, "Destinació / itinerari:", W - 2 * M - 50 * mm)
    y -= 7 * mm
    camp(c, M, y, "Professor/a responsable:", 55 * mm)
    camp(c, M + 100 * mm, y, "Acompanyants:", W - M - (M + 100 * mm) - 34 * mm)

    y -= 12 * mm
    h2(c, M, y, "Objectius de la sortida")
    y -= 8 * mm
    objectius = [
        "Aplicar les normes de circulació i seguretat viària.",
        "Observar infraestructures urbanes (carrils bici, passos, senyals).",
        "Respectar vianants i altres vehicles; conviure a la via.",
        "Conèixer rutes segures i zones 30 del barri.",
        "Rodar en grup amb ordre i cohesió.",
    ]
    for t in objectius:
        check(c, M, y, t)
        y -= 6.5 * mm

    y -= 5 * mm
    h2(c, M, y, "Planificació prèvia de la ruta")
    y -= 8 * mm
    camp(c, M, y, "Recorregut previst:", W - 2 * M - 45 * mm)
    y -= 7 * mm
    camp(c, M, y, "Distància aprox.:", 24 * mm)
    c.setFillColor(GRIS); c.drawString(M + 62 * mm, y, "km")
    camp(c, M + 80 * mm, y, "Temps estimat:", 24 * mm)
    c.setFillColor(GRIS); c.drawString(M + 80 * mm + 55 * mm, y, "min")
    y -= 7 * mm
    c.setFillColor(GRIS); c.setFont("Helvetica", 9.5)
    c.drawString(M, y, "Dificultat:")
    x = M + 22 * mm
    for t in ["Baixa", "Mitjana", "Alta"]:
        x += check(c, x, y, t)
    y -= 7 * mm
    camp(c, M, y, "Punts de risc a vigilar:", W - 2 * M - 50 * mm)

    y -= 12 * mm
    h2(c, M, y, "Seguretat abans de sortir (revisió en parella)")
    y -= 8 * mm
    c.setFillColor(TINTA); c.setFont("Helvetica", 9.5)
    c.drawString(M, y, "EPI i bici (marca quan ho hagis comprovat):")
    y -= 7 * mm
    x = M
    for t in ["Casc ben cordat", "Armilla reflectant", "Frens OK", "Rodes i pressió OK", "Llums (si cal)"]:
        w = check(c, x, y, t)
        x += w
        if x > W - M - 40 * mm:
            x = M; y -= 6.5 * mm
    y -= 6.5 * mm
    c.setFillColor(GRIS); c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(M, y, "La sortida la dirigeix el professorat. Circulem en fila, respectem els semàfors i mantenim distàncies.")


def taula_registre(c, y, files, valoracio="🔴 🟡 🟢"):
    x0, wobs, wval = M, 92 * mm, 26 * mm
    wcom = W - 2 * M - wobs - wval
    c.setFillColor(colors.HexColor("#eef0fb"))
    c.rect(x0, y - 6 * mm, W - 2 * M, 6 * mm, fill=1, stroke=0)
    c.setFillColor(INDIGO); c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x0 + 2 * mm, y - 4.3 * mm, "Observació")
    c.drawString(x0 + wobs + 2 * mm, y - 4.3 * mm, "Valoració")
    c.drawString(x0 + wobs + wval + 2 * mm, y - 4.3 * mm, "Comentaris")
    yy = y - 6 * mm
    fh = 9 * mm
    for t in files:
        c.setStrokeColor(LINIA); c.setLineWidth(0.6)
        c.rect(x0, yy - fh, W - 2 * M, fh, fill=0, stroke=1)
        c.line(x0 + wobs, yy - fh, x0 + wobs, yy)
        c.line(x0 + wobs + wval, yy - fh, x0 + wobs + wval, yy)
        c.setFillColor(TINTA); c.setFont("Helvetica", 9)
        c.drawString(x0 + 2 * mm, yy - 5.5 * mm, t)
        c.setFillColor(GRIS); c.setFont("Helvetica", 9)
        c.drawString(x0 + wobs + 3.5 * mm, yy - 5.5 * mm, "O   O   O")
        yy -= fh
    return yy


def pagina2(c):
    capsalera(c, "FITXA DE SORTIDA  ·  Durant i després", "B9 · Repara i Roda 360")
    y = H - M - 18 * mm
    camp(c, M, y, "Nom:", 78 * mm, 13 * mm)
    camp(c, M + 100 * mm, y, "Parella:", W - M - (M + 100 * mm) - 3 * mm)

    y -= 10 * mm
    h2(c, M, y, "Registre durant la sortida")
    c.setFillColor(GRIS); c.setFont("Helvetica-Oblique", 8.5)
    c.drawRightString(W - M, y, "O O O  =  malament / regular / bé")
    y -= 4 * mm
    y = taula_registre(c, y, [
        "Respecte a les normes de circulació",
        "Ús adequat del casc i l'equip",
        "Convivència amb vianants i vehicles",
        "Identificació de punts de risc",
        "Participació i actitud",
    ])

    y -= 8 * mm
    h2(c, M, y, "Reflexió posterior")
    for pregunta in [
        "Què has après avui sobre circular amb bici per la ciutat?",
        "Quina situació t'ha fet pensar en la seguretat?",
        "Què milloraries per a la propera sortida?",
    ]:
        y -= 8 * mm
        c.setFillColor(TINTA); c.setFont("Helvetica", 9.5)
        c.drawString(M, y, pregunta)
        y -= 6 * mm
        liniah(c, M, y, W - 2 * M)

    y -= 12 * mm
    h2(c, M, y, "Avaluació docent")
    y -= 7 * mm
    c.setFillColor(GRIS); c.setFont("Helvetica", 9)
    c.drawString(M, y, "Valoració global:")
    x = M + 32 * mm
    for t in ["Inici", "En progrés", "Assolit", "Excel·lent"]:
        x += check(c, x, y, t)
    y -= 8 * mm
    for etiq in ["Preparació i implicació", "Aplicació de normes i seguretat",
                 "Actitud i cooperació", "Reflexió i dossier"]:
        camp(c, M, y, etiq + ":", W - 2 * M - c.stringWidth(etiq + ":", "Helvetica", 9.5) - 5 * mm)
        y -= 7 * mm

    y -= 3 * mm
    h2(c, M, y, "Documentació associada")
    y -= 8 * mm
    x = M
    for t in ["Fotografies", "Fitxa de rutes/mapes", "Autoritzacions familiars", "Valoració del grup (assemblea)"]:
        w = check(c, x, y, t)
        x += w
        if x > W - M - 45 * mm:
            x = M; y -= 6.5 * mm


def build():
    c = canvas.Canvas(SORTIDA, pagesize=A4)
    c.setTitle("Fitxa de sortida en bicicleta — B9 · Repara i Roda 360")
    pagina1(c)
    c.showPage()
    pagina2(c)
    c.showPage()
    c.save()
    print("PDF generat:", SORTIDA)


if __name__ == "__main__":
    build()
