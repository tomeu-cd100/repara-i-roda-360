#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el full de reparació de l'alumnat en PDF (A4 vertical).

Checklist de les accions de reparació directa de la bici (B1-B9), ordenades per
sistema, de la diagnosi al lliurament. L'alumne/a el guarda al quadern i marca
cada acció quan l'ha feta. Sortida: Avaluació/Full_reparacio_alumne.pdf

Ús:  py -3.11 scripts/genera_full_reparacio.py
Requereix: reportlab  (py -3.11 -m pip install reportlab)
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph,
                                Spacer)
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

AQUI = os.path.dirname(os.path.abspath(__file__))
SORTIDA = os.path.normpath(os.path.join(AQUI, "..", "Avaluació",
                                        "Full_reparacio_alumne.pdf"))

# --- Colors del projecte ---
VERD = colors.HexColor("#1f9e7a")     # taller
VERD_CLAR = colors.HexColor("#e6f6f1")
GRIS_FOSC = colors.HexColor("#4a5568")
REIXA = colors.HexColor("#cbd5e0")
TINTA = colors.HexColor("#1a202c")

# Font única del contingut: (sistema, [accions]). Accions de reparació directa,
# extretes de les Fitxa_alumnat.md de B1-B9 i de la temporització anual.
ACCIONS = [
    ("Diagnosi", [
        "He fet la diagnosi inicial (fitxa de recepció)",
        "He fet el M-check complet i he anotat què cal reparar",
    ]),
    ("Neteja", [
        "He netejat la bici",
        "He lubricat la cadena i els punts de gir (sense excés)",
    ]),
    ("Rodes", [
        "He desmuntat i muntat una roda",
        "He desmuntat i muntat el pneumàtic i la cambra",
        "He localitzat i parxejat una punxada",
        "He substituït una cambra",
        "He inflat a la pressió correcta (la del flanc)",
        "He revisat els radis i l'alineació de la roda",
    ]),
    ("Frens", [
        "He ajustat les sabates i la tensió del cable",
        "He canviat un cable o una funda de fre",
        "He canviat pastilles o centrat una pinça de disc",
        "Prova: el fre atura la roda i no frega",
    ]),
    ("Cadena", [
        "He mesurat el desgast de la cadena",
        "He tallat i unit una cadena",
    ]),
    ("Bieles i pedals", [
        "He extret i muntat bieles o pedals (rosca correcta)",
    ]),
    ("Canvis", [
        "He ajustat els topalls H/L i la tensió del canvi posterior",
        "He ajustat el canvi davanter",
        "Prova: canvia suau i no salta",
    ]),
    ("Seient i direcció", [
        "He ajustat el seient (alçada, avanç, inclinació)",
        "He ajustat el joc de direcció, la potència i el manillar",
        "He canviat o revisat els punys",
    ]),
    ("Equipament", [
        "He muntat i comprovat llums, reflectors i timbre",
    ]),
    ("Lliurament", [
        "Revisió final: la bici està llesta per donar",
    ]),
]


def casella(mida=4.6 * mm):
    """Casella buida vectorial (reportlab no pinta bé els glifs de casella)."""
    d = Drawing(mida, mida)
    d.add(Rect(0, 0, mida, mida, strokeColor=TINTA, strokeWidth=0.9,
               fillColor=colors.white))
    return d


def build():
    doc = SimpleDocTemplate(
        SORTIDA, pagesize=A4,
        leftMargin=14 * mm, rightMargin=14 * mm,
        topMargin=12 * mm, bottomMargin=10 * mm,
        title="Full de reparació — Repara i Roda 360",
        author="Repara i Roda 360",
    )
    estils = getSampleStyleSheet()
    ample = A4[0] - 28 * mm
    elems = []

    # --- Capçalera: banda verda + dades de l'alumne/a ---
    titol = Paragraph(
        "<b>Full de reparació</b>",
        ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=18,
                       leading=21, textColor=colors.white))
    subt = Paragraph(
        "Repara i Roda 360 · Taller de bicicletes · 4t ESO",
        ParagraphStyle("s", fontName="Helvetica", fontSize=9.5, leading=12,
                       textColor=colors.white))
    banda = Table([[titol], [subt]], colWidths=[ample])
    banda.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERD),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
    ]))
    elems.append(banda)
    elems.append(Spacer(1, 6))

    camp = ParagraphStyle("c", fontName="Helvetica", fontSize=10, leading=13,
                          textColor=TINTA)
    dades = Table([[
        Paragraph("<b>Nom:</b> ____________________________________", camp),
        Paragraph("<b>Grup:</b> ________", camp),
        Paragraph("<b>Bici núm.:</b> ______", camp),
    ]], colWidths=[ample * 0.58, ample * 0.20, ample * 0.22])
    dades.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elems.append(dades)
    elems.append(Spacer(1, 4))
    elems.append(Paragraph(
        "Marca cada acció quan l'hagis feta tu a la bici. "
        "Si no surt bé a la primera, torna-ho a provar abans de marcar-la.",
        ParagraphStyle("i", fontName="Helvetica-Oblique", fontSize=8.8,
                       leading=11, textColor=GRIS_FOSC)))
    elems.append(Spacer(1, 6))

    # --- Taula del checklist ---
    cap = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=9,
                         textColor=colors.white)
    sis = ParagraphStyle("sis", fontName="Helvetica-Bold", fontSize=9.2,
                         leading=11, textColor=VERD)
    acc = ParagraphStyle("acc", fontName="Helvetica", fontSize=9.6,
                         leading=11.5, textColor=TINTA)
    files = [[Paragraph("Sistema", cap), Paragraph("Acció", cap),
              Paragraph("Fet", cap)]]
    estil = [
        ("BACKGROUND", (0, 0), (-1, 0), GRIS_FOSC),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, REIXA),
        ("BOX", (0, 0), (-1, -1), 0.8, GRIS_FOSC),
        ("TOPPADDING", (0, 1), (-1, -1), 5.4),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5.4),
    ]
    r = 1
    for n, (sistema, accions) in enumerate(ACCIONS):
        inici = r
        for i, a in enumerate(accions):
            files.append([Paragraph(sistema, sis) if i == 0 else "",
                          Paragraph(a, acc), casella()])
            r += 1
        if len(accions) > 1:
            estil.append(("SPAN", (0, inici), (0, r - 1)))
        if n % 2 == 0:
            estil.append(("BACKGROUND", (0, inici), (-1, r - 1), VERD_CLAR))
        estil.append(("LINEABOVE", (0, inici), (-1, inici), 1.0, VERD))

    t = Table(files, colWidths=[34 * mm, ample - 34 * mm - 16 * mm, 16 * mm],
              repeatRows=1)
    t.setStyle(TableStyle(estil))
    elems.append(t)

    doc.build(elems)
    print("PDF generat:", SORTIDA)


if __name__ == "__main__":
    build()
