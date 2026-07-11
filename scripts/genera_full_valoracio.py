#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el full de valoració diària del docent en PDF (A4 apaïsat).

Un full per sessió. El docent valora cada alumne/a al taller de bicicletes i a
l'aula maker amb codis ràpids. Sortida: Avaluació/Full_valoracio_diaria.pdf

Ús:  py -3.11 scripts/genera_full_valoracio.py
Requereix: reportlab  (py -3.11 -m pip install reportlab)
"""
import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph,
                                Spacer)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

AQUI = os.path.dirname(os.path.abspath(__file__))
SORTIDA = os.path.normpath(os.path.join(AQUI, "..", "Avaluació",
                                        "Full_valoracio_diaria.pdf"))

NObiles = 12  # nombre de files d'alumnat

# --- Colors del projecte ---
VERD = colors.HexColor("#1f9e7a")     # taller
BLAU = colors.HexColor("#2b6cb0")     # maker
GRIS = colors.HexColor("#e2e8f0")
GRIS_FOSC = colors.HexColor("#4a5568")
TINTA = colors.HexColor("#1a202c")


def build():
    doc = SimpleDocTemplate(
        SORTIDA, pagesize=landscape(A4),
        leftMargin=10 * mm, rightMargin=10 * mm,
        topMargin=9 * mm, bottomMargin=8 * mm,
        title="Full de valoració diària — Repara i Roda 360",
        author="Repara i Roda 360",
    )
    estils = getSampleStyleSheet()
    h = ParagraphStyle("h", parent=estils["Title"], fontSize=15, spaceAfter=2,
                       textColor=TINTA)
    sub = ParagraphStyle("sub", parent=estils["Normal"], fontSize=8.5,
                          textColor=GRIS_FOSC)
    cel = ParagraphStyle("cel", parent=estils["Normal"], fontSize=7.6,
                         alignment=TA_CENTER, leading=8.4, textColor=colors.white)
    elems = []

    elems.append(Paragraph("Full de valoració diària — Repara i Roda 360", h))
    elems.append(Paragraph(
        "Optativa 4t ESO · <b>Data:</b> ____ / ____ / ______   "
        "<b>Setmana:</b> ______   <b>SA:</b> ______   "
        "<b>Avui:</b> [ &nbsp; ] Taller de bicicletes (2h)  &nbsp; [ &nbsp; ] Aula maker (1h)",
        sub))
    elems.append(Spacer(1, 4))

    def th(txt, color=colors.white, mida=7.6):
        return Paragraph(f"<b>{txt}</b>", ParagraphStyle(
            "th", fontSize=mida, alignment=TA_CENTER, leading=8.2,
            textColor=color, fontName="Helvetica-Bold"))

    # Fila de grups (span) + fila de subcapçaleres
    fila_grup = [
        Paragraph("<b>Nº</b>", ParagraphStyle("g", fontSize=8,
                  alignment=TA_CENTER, textColor=colors.white)),
        Paragraph("<b>Alumne/a</b>", ParagraphStyle("g2", fontSize=8,
                  textColor=colors.white)),
        th("TALLER DE BICICLETES"), "", "", "",
        th("AULA MAKER"), "", "",
        th("Diari"), th("Observacions"),
    ]
    fila_sub = [
        "", "",
        th("Seguretat", mida=6.8), th("Tècnica", mida=6.8),
        th("Ordre i eines", mida=6.8), th("Parella", mida=6.8),
        th("Seguretat", mida=6.8), th("Fabricació", mida=6.8),
        th("Autonomia", mida=6.8),
        th("cara A i B", mida=6.8), th(""),
    ]
    dades = [fila_grup, fila_sub]
    for i in range(1, NObiles + 1):
        dades.append([str(i), "", "", "", "", "", "", "", "", "", ""])

    # Amplades (suma ~ 277 mm útils en A4 apaïsat amb marges de 10 mm)
    amplades = [8*mm, 44*mm,
                16*mm, 16*mm, 16*mm, 16*mm,
                18*mm, 18*mm, 18*mm,
                14*mm, 77*mm]
    t = Table(dades, colWidths=amplades, rowHeights=[8*mm, 8*mm] + [11*mm]*NObiles)

    estil = TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 2), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 2), (0, -1), "CENTER"),
        ("ALIGN", (2, 2), (9, -1), "CENTER"),
        # Capçaleres de grup
        ("SPAN", (2, 0), (5, 0)),   # TALLER
        ("SPAN", (6, 0), (8, 0)),   # MAKER
        ("SPAN", (0, 0), (0, 1)),   # Nº
        ("SPAN", (1, 0), (1, 1)),   # Alumne
        ("SPAN", (9, 0), (9, 1)),   # Diari
        ("SPAN", (10, 0), (10, 1)),  # Observacions
        ("BACKGROUND", (0, 0), (1, 1), GRIS_FOSC),
        ("BACKGROUND", (2, 0), (5, 1), VERD),
        ("BACKGROUND", (6, 0), (8, 1), BLAU),
        ("BACKGROUND", (9, 0), (10, 1), GRIS_FOSC),
        # Files d'alumnat: ratllat zebra
        ("BACKGROUND", (0, 2), (-1, -1), colors.white),
        *[("BACKGROUND", (0, r), (-1, r), colors.HexColor("#f4f7fa"))
          for r in range(2, NObiles + 2) if r % 2 == 0],
        # Reixa
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ("LINEBELOW", (0, 1), (-1, 1), 1.0, GRIS_FOSC),
        ("LINEAFTER", (5, 0), (5, -1), 1.0, colors.HexColor("#a0aec0")),
        ("LINEAFTER", (8, 0), (8, -1), 1.0, colors.HexColor("#a0aec0")),
        # Farciment mínim a les subcapçaleres perquè els mots hi càpiguen
        ("LEFTPADDING", (2, 1), (10, 1), 1),
        ("RIGHTPADDING", (2, 1), (10, 1), 1),
    ])
    t.setStyle(estil)
    elems.append(t)
    elems.append(Spacer(1, 5))

    # Llegenda de codis
    lleg = ParagraphStyle("lleg", parent=estils["Normal"], fontSize=8.2,
                          textColor=TINTA, leading=11)
    elems.append(Paragraph(
        "<b>Codis de valoració:</b> &nbsp; "
        "<b>+</b> ho fa bé / amb autonomia &nbsp;&nbsp; "
        "<b>=</b> correcte / se'n surt amb suport &nbsp;&nbsp; "
        "<b>!</b> cal atenció / encara no &nbsp;&nbsp; "
        "<b>A</b> absent &nbsp;&nbsp;|&nbsp;&nbsp; "
        "Es pot fer servir el semàfor: <b>V</b> verd · <b>G</b> groc · <b>R</b> vermell.",
        lleg))
    elems.append(Paragraph(
        "<b>Referència de criteris:</b> Seguretat = CA1.4 · Tècnica = CA1/CA2 "
        "(diagnosi i reparació) · Ordre i eines = CA2.3 · Parella = CA6.1 · "
        "Seguretat maker = CA1.4 (làser/3D) · Fabricació = CA3 · Diari = CA4.1. "
        "Buida-ho al <i>Full_seguiment_grup.md</i> i al <i>Full_progres_competencial.md</i>.",
        ParagraphStyle("ref", parent=estils["Normal"], fontSize=7.4,
                       textColor=GRIS_FOSC, leading=9.5)))

    doc.build(elems)
    print("PDF generat:", SORTIDA)


if __name__ == "__main__":
    build()
