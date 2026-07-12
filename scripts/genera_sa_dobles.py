#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera les SA de les DUES assignatures separades: Bicicletes i Maker.

Per a cada SA escriu <CODI>.md (la unitat, per al docent) i Fitxa_alumnat.md
(el full de l'alumnat) dins Classes/Bicicletes/<carpeta>/ o Classes/Maker/<carpeta>/.

Ús:  py -3.11 scripts/genera_sa_dobles.py
"""
import os

ARREL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

TRACKS = {
    "bicicletes": {"icon": "🚲", "full": "Taller de bicicletes", "hores": "2 h",
                   "rubrica": "Rubrica_bicicletes"},
    "maker": {"icon": "🛠️", "full": "Aula maker", "hores": "1 h",
              "rubrica": "Rubrica_maker"},
}


def sa_md(track, s):
    t = TRACKS[track]
    out = [f"# {s['code']} — «{s['name']}» ({t['full']})", ""]
    out.append("| | |")
    out.append("|---|---|")
    out.append(f"| **Assignatura** | {t['icon']} {t['full']} ({t['hores']}/setmana) |")
    out.append("| **Nivell** | 4t ESO · grup professionalitzador |")
    out.append(f"| **Setmanes** | {s['setm']} |")
    out.append(f"| **Producte** | {s['producte']} |")
    if s.get("bloc"):
        out.append(f"| **Bloc** | {s['bloc']} |")
    out.append("")
    out.append(f"> 🔗 **Es complementa amb** {s['compl']}, però són **dues assignatures "
               f"separades**: aquí, només {t['full'].lower()}.")
    out.append("")
    out.append("## 1. Descripció")
    out.append(s["desc"])
    out.append("")
    out.append(f"> **Repte:** «{s['repte']}»")
    out.append("")
    out.append("## 2. Aprenentatge visible")
    out.append("En acabar seré capaç de…")
    out.append("")
    out += [f"- {x}" for x in s["visible"]]
    out.append("")
    out.append("**Criteris d'èxit**")
    out.append("")
    out += [f"- [ ] {x}" for x in s["exit"]]
    out.append("")
    out.append("## 3. Sabers")
    out += [f"- {x}" for x in s["sabers"]]
    out.append("")
    out.append("## 4. Sessions")
    for titol, bullets in s["sessions"]:
        out.append(f"**{titol}**")
        out.append("")
        out += [f"{i + 1}. {b}" for i, b in enumerate(bullets)]
        out.append("")
    out.append("## 5. Atenció a la diversitat (DUA)")
    out += [f"- {x}" for x in s["dua"]]
    out.append("")
    out.append("## 6. Materials")
    out += [f"- {x}" for x in s["materials"]]
    out.append(f"- Fitxa: `Fitxa_alumnat.md` · Rúbrica: `Avaluació/{t['rubrica']}.md` · "
               f"Diari: `Programació didàctica/Diari_setmanal_paper.pdf`")
    out.append("")
    out.append("## 7. Avaluació")
    out.append("| Evidència | Instrument | Criteris |")
    out.append("|-----------|-----------|----------|")
    for ev, ins, cr in s["aval"]:
        out.append(f"| {ev} | {ins} | {cr} |")
    out.append("")
    return "\n".join(out)


def fitxa_md(track, s):
    t = TRACKS[track]
    out = [f"# Fitxa de l'alumnat — {s['code']}: {s['name']}", ""]
    out.append("**Nom:** ______________________  **Setmana:** ______  "
               "**Data:** ____/____/______" +
               ("  **Bici núm:** ______" if track == "bicicletes" else ""))
    out.append("")
    out.append(f"## El repte {t['icon']}")
    out.append(s["repte"])
    out.append("")
    out.append("## 🧑‍🏫 Com ho aprendràs avui")
    out.append("**No cal saber-ho abans: ho aprens fent-ho**, pas a pas amb el professor.")
    out.append("")
    out.append("1. **Mira la demostració** del profe (com es fa, pas a pas).")
    out.append("2. **Prova-ho amb ajuda** (pràctica guiada, en parella).")
    out.append("3. **Fes-ho tu** i marca els passos de sota.")
    out.append("")
    if s.get("video"):
        vtit, vid = s["video"]
        out.append("## 📹 Mira com es fa")
        out.append(f'<div class="video-wrap"><iframe '
                   f'src="https://www.youtube-nocookie.com/embed/{vid}" '
                   f'title="{vtit}" loading="lazy" '
                   f'allow="accelerometer; encrypted-media; picture-in-picture" '
                   f'allowfullscreen></iframe></div>')
        out.append("")
        out.append(f"*Vídeo: {vtit} (YouTube).*")
        out.append("")
    out.append("## Els passos d'avui")
    out.append("*(marca'ls a mesura que els aprens i els fas)*")
    out.append("")
    out += [f"- [ ] {x}" for x in s["exit"]]
    out.append("")
    if s.get("fitxa"):
        for titol, linia in s["fitxa"]:
            out.append(f"**{titol}** {linia}")
            out.append("")
    if s.get("imprimibles"):
        out.append("## 🖨️ Per imprimir")
        out += [f"- [{txt}]({fitxer})" for txt, fitxer in s["imprimibles"]]
        out.append("")
    out.append("## Com m'avaluaran")
    out.append("| Què miraran | Com |")
    out.append("|-------------|-----|")
    for ev, ins, _cr in s["aval"]:
        out.append(f"| {ev} | {ins} |")
    out.append("")
    return "\n".join(out)


# ─────────────────────────── DADES: BICICLETES (B0–B9) ──────────────────────
BICI = [
 {"video": ("Eines bàsiques d'un taller de bicis (en castellà)", "2Lq-OvujjsM"),
  "code": "B0", "folder": "B0_Punt_de_partida", "name": "Punt de partida", "setm": "1–2",
  "producte": "**Carnet d'eines** + contracte d'aula + avaluació inicial",
  "compl": "l'hora de maker **M0** (benvinguda i carnet de màquina)",
  "desc": "Abans de tocar cap bici, cal conèixer el taller, les eines i treballar segur.",
  "repte": "Mou-te pel taller amb seguretat i autonomia: guanya't el carnet d'eines.",
  "visible": ["Anomenar les eines bàsiques i la seva funció.",
              "Treballar seguint les normes de seguretat.",
              "Omplir la primera entrada del diari."],
  "exit": ["He signat el contracte d'aula.", "Tinc el carnet d'eines.",
           "He fet l'avaluació inicial i la primera entrada del diari."],
  "sabers": ["El taller: espai, zones, ordre i seguretat.",
             "Eines bàsiques: nom, funció, ús segur.",
             "Introducció a les parts de la bicicleta."],
  "sessions": [("Setmana 1 — Benvinguda i seguretat",
                ["Acollida i recorregut pel taller (25').",
                 "Les normes, raonades una a una (30').",
                 "Presentació de les eines amb la làmina de parts (35').",
                 "Tancament i diari (10')."]),
               ("Setmana 2 — Gimcana i punt de partida",
                ["Gimcana d'eines i seguretat (`Material_gimcana_taller.md`) (50').",
                 "Checkpoint del carnet d'eines (20').",
                 "Avaluació inicial pràctica (40').",
                 "Contracte + tancament (10')."])],
  "dua": ["Demostracions físiques i làmina il·lustrada.",
          "Els checkpoints es superen fent (sense escriure).",
          "Èxit immediat el primer dia; parella d'ajuda."],
  "materials": ["Eines bàsiques, bici de demostració, bomba i manòmetre.",
                "`Recursos/parts-de-la-bicicleta-en-català-1024x602.png`.",
                "Imprimibles: `Normativa/Normes_contracte.pdf`, "
                "`Normativa/Passaport_alumne.pdf`, "
                "`Avaluació/Avaluacio_inicial_alumne.pdf`."],
  "fitxa": [("Una eina que ara sé fer servir:", "________________"),
            ("Una norma de seguretat important i per què:", "________________")],
  "imprimibles": [("Contracte d'aula i carnet d'eines (PDF)", "Contracte_carnet_bicicletes.pdf"),
                  ("Avaluació inicial (PDF)", "Avaluacio_inicial_alumne.pdf"),
                  ("Diari setmanal (PDF)", "Diari_setmanal_paper.pdf")],
  "aval": [("Carnet d'eines", "Checkpoint pràctic", "CA2.3, CA1.1"),
           ("Seguretat i contracte", "Observació", "CA1.4, CA6.1"),
           ("Diari del taller", "Pauta del diari", "CA4.1")]},

 {"video": ("Les parts de la bicicleta (en castellà)", "uQ2csLLygps"),
  "code": "B1", "folder": "B1_La_bici_per_dins", "name": "La bici per dins", "setm": "3–4",
  "producte": "**Fitxa de recepció** d'una bici + diagnosi",
  "compl": "l'hora de maker **M1** (placa identificativa a làser)",
  "desc": "Han arribat les bicis de donació. Cal conèixer-les, identificar-les i diagnosticar-les.",
  "repte": "Rep una bici, identifica'n el tipus i les parts i omple la fitxa de recepció.",
  "visible": ["Anomenar les parts i la funció de cada sistema.",
              "Distingir els tipus de bici (urbana, BTT, carretera, elèctrica).",
              "Fer una diagnosi visual de l'estat."],
  "exit": ["Identifico 10 parts sobre una bici real.",
           "Dic de quin tipus és la meva bici i ho justifico.",
           "He omplert la fitxa de recepció."],
  "sabers": ["Anatomia de la bicicleta i tipus.", "Història i evolució (nocions).",
             "Diagnosi visual i fitxa de recepció."],
  "sessions": [("Setmana 3 — Anatomia i tipus",
                ["Les parts de la bici amb la làmina i una bici real (40').",
                 "Tipus de bicicleta i usos; breu història (35').",
                 "Acollida i tancament amb diari (25')."]),
               ("Setmana 4 — Recepció i diagnosi",
                ["Demo de diagnosi de dalt a baix (20').",
                 "Recepció d'una bici: omplir la fitxa (`Recursos/Fitxa_recepció_bicicleta.xlsx`) (70').",
                 "Tancament i diari (10')."])],
  "dua": ["Làmina de parts il·lustrada i bici real per manipular.",
          "La diagnosi es marca amb icones/colors (sense text llarg).",
          "Cada parella «adopta» una bici per a tot el curs."],
  "materials": ["Bicicletes de donació, làmina de parts.",
                "`Recursos/Fitxa_recepció_bicicleta.xlsx`, `Recursos/Tipus de bicicletes.xlsx`."],
  "fitxa": [("El tipus de la meva bici i com ho sé:", "________________"),
            ("La primera reparació que crec que necessitarà:", "________________")],
  "imprimibles": [("Full de recepció de la bicicleta (Excel — imprimeix-lo i omple'l)",
                   "Fitxa_recepció_bicicleta.xlsx"),
                  ("Diari setmanal (PDF)", "Diari_setmanal_paper.pdf")],
  "aval": [("Parts i tipus de bici", "Checklist sobre bici real", "CA1.1"),
           ("Fitxa de recepció", "Rúbrica de diagnosi", "CA1.2"),
           ("Diari del taller", "Pauta del diari", "CA4.1")]},

 {"video": ("Com netejar i greixar la cadena (en castellà)", "1Z14L21k3yA"),
  "code": "B2", "folder": "B2_Posada_a_punt", "name": "Posada a punt", "setm": "5–7",
  "producte": "Una bici amb el **M-check** fet",
  "compl": "l'hora de maker **M2** (organitzadors d'eines)",
  "desc": "Un mecànic segueix una rutina: netejar, greixar i fer la revisió de seguretat (M-check).",
  "repte": "Fes la posada a punt completa d'una bici seguint la rutina.",
  "visible": ["Netejar i greixar la transmissió i els punts de gir.",
              "Fer un M-check de davant a darrere."],
  "exit": ["He netejat i greixat la bici (sense excés de greix).",
           "He fet el M-check complet i he anotat què cal ajustar."],
  "sabers": ["Rutina de manteniment: neteja, desgreixatge, lubricació.",
             "M-check: revisió sistemàtica de seguretat."],
  "sessions": [("Setmana 5 — Neteja i lubricació",
                ["Demo de neteja i greixatge (20').", "Pràctica per parelles (70').",
                 "Diari (10'). El greix va on hi ha moviment, no a tot arreu."]),
               ("Setmana 6 — El M-check",
                ["Demo del M-check pas a pas (25').", "M-check guiat amb full de comprovació (65').",
                 "Diari (10')."]),
               ("Setmana 7 — Autonomia",
                ["M-check autònom verificat pel docent (50').",
                 "Posada a punt de la primera bici (50')."])],
  "dua": ["Full de M-check amb pictogrames i ordre fix.",
          "El M-check es registra amb semàfors.",
          "Ritmes flexibles."],
  "materials": ["Desgreixant, lubricant, draps; full de M-check.",
                "`Recursos/Llibre Manteniment Bici/Cap02_rutina mantenimiento y reparacion.pdf` (docent)."],
  "fitxa": [("Un pas del M-check que no oblidaré:", "________________"),
            ("On va el greix i on NO:", "________________")],
  "aval": [("Neteja i lubricació", "Observació", "CA2.2"),
           ("M-check autònom", "Full verificat", "CA2.1"),
           ("Diari del taller", "Pauta del diari", "CA4.1")]},

 {"code": "B3", "folder": "B3_Rodes_i_punxades", "name": "Rodes i punxades", "setm": "8–10",
  "producte": "Una **punxada reparada** i la roda comprovada",
  "compl": "l'hora de maker **M3** (kit de reparació: palanques i caixa)",
  "desc": "La punxada és l'avaria més freqüent i la que més autonomia dona saber resoldre.",
  "repte": "Repara una punxada de principi a fi i deixa la roda rodona i segura.",
  "visible": ["Treure i posar una roda correctament.",
              "Localitzar la punxada i parxejar o canviar la cambra.",
              "Comprovar la tensió dels radis i que la roda no balli."],
  "exit": ["He tret i posat la roda sense danyar res.",
           "He reparat la punxada i la roda aguanta la pressió.",
           "La roda gira recta."],
  "sabers": ["Desmuntatge i muntatge de la roda; sistema de tancament.",
             "Cambra i pneumàtic: substitució, parxejat, pressió.",
             "Radis i centrat bàsic de la roda."],
  "sessions": [("Setmana 8 — Treure i posar la roda",
                ["Demo (20').", "Pràctica de desmuntatge/muntatge (70').", "Diari (10')."]),
               ("Setmana 9 — Reparar la punxada",
                ["Demo de localització i parxejat (20').", "Pràctica completa (70').", "Diari (10')."]),
               ("Setmana 10 — Radis i roda rodona",
                ["Comprovació de tensió i centrat bàsic (25').", "Pràctica (65').", "Diari (10')."])],
  "dua": ["Fitxa de passos numerada i plastificada.",
          "Es demostra reparant (sense explicar per escrit).",
          "Es practica repetidament (és molt motivador)."],
  "materials": ["Cambres, pegats, pneumàtics, palanques, bomba.",
                "`Recursos/Llibre Manteniment Bici/Cap06_ruedas.pdf` (docent), "
                "`Recursos/reparació de punxades.docx`."],
  "video": ("Aprèn a reparar una punxada — Decathlon", "sNt0N9CNjAM"),
  "fitxa": [("El pas de la punxada que més em costa:", "________________"),
            ("Pressió correcta del pneumàtic (mira el flanc):", "______ bar/psi")],
  "aval": [("Desmuntatge/muntatge de roda", "Observació", "CA1.3"),
           ("Punxada reparada", "Prova: la roda aguanta", "CA1.2, CA1.3"),
           ("Diari del taller", "Pauta del diari", "CA4.1")]},

 {"video": ("Com muntar i ajustar frens V-Brake (en castellà)", "-KoffE0P9HE"),
  "code": "B4", "folder": "B4_Frens", "name": "Frens", "setm": "11–14",
  "producte": "Una bici amb els **frens segurs**",
  "compl": "l'hora de maker **M4** (separadors i guies de fre en 3D)",
  "desc": "El fre és el sistema de seguretat: una bici que no frena bé no es pot donar.",
  "repte": "Deixa una bici amb els frens ajustats, canvia el que calgui i comprova que frena.",
  "visible": ["Distingir fre de sabata i de disc.",
              "Ajustar tensió de cable i posició de sabates/pastilles.",
              "Comprovar que el fre és segur abans de donar la bici."],
  "exit": ["He ajustat un fre de sabata.",
           "He centrat una pinça de disc o canviat pastilles.",
           "El fre atura la roda amb una pressió raonable."],
  "sabers": ["Fre de sabata: ajust, tensió, canvi de cable.",
             "Fre de disc: pastilles, centrat de pinça.",
             "Diagnòstic de seguretat del fre."],
  "sessions": [("Setmana 11 — Fre de sabata: ajust",
                ["Demo (20').", "Ajust de sabates i tensió (70').", "Diari (10')."]),
               ("Setmana 12 — Fre de sabata: cables",
                ["Demo de canvi de cable i funda (20').", "Pràctica (70').", "Diari (10')."]),
               ("Setmana 13 — Fre de disc",
                ["Pastilles i centrat de pinça (25').", "Pràctica (65').", "Diari (10')."]),
               ("Setmana 14 — Frens segurs",
                ["Pràctica completa i comprovació final (100').",
                 "Tancament de trimestre: autoavaluació i coavaluació."])],
  "dua": ["Fitxa amb fotos «abans/després» del fre ben ajustat.",
          "La comprovació final es fa frenant (fent).",
          "«Aquest fre pot evitar un accident»: dona sentit."],
  "materials": ["Cables, fundes, sabates, pastilles, eines d'ajust.",
                "`Recursos/Llibre Manteniment Bici/Cap03_sistema de frenos.pdf` (docent), "
                "`Recursos/reparació frens.docx`."],
  "fitxa": [("Com sé que un fre frena prou per donar la bici:", "________________"),
            ("La diferència principal entre sabata i disc:", "________________")],
  "aval": [("Ajust de frens", "Observació + rúbrica", "CA1.3"),
           ("Comprovació de seguretat", "Prova de frenada", "CA1.4"),
           ("Diari del taller", "Pauta del diari", "CA4.1")]},

 {"video": ("Com canviar la cadena de la bicicleta (en castellà)", "W3alcslVgaE"),
  "code": "B5", "folder": "B5_Transmissio_I", "name": "Transmissió I: cadena i pedals",
  "setm": "15–17", "producte": "Cadena **mantinguda o substituïda**",
  "compl": "l'hora de maker **M5** (mesurador de desgast de cadena)",
  "desc": "La transmissió és el cor de la bici: converteix el pedaleig en moviment.",
  "repte": "Comprova si la cadena està gastada, mantén-la o canvia-la, i revisa bieles i pedals.",
  "visible": ["Mesurar el desgast d'una cadena i decidir si cal canviar-la.",
              "Tallar i unir una cadena a la mida correcta.",
              "Revisar i muntar bieles i pedals (rosca correcta)."],
  "exit": ["He mesurat el desgast i he decidit què fer.",
           "He lubricat o substituït la cadena correctament.",
           "Bieles i pedals ben collats (rosca correcta)."],
  "sabers": ["Cadena: desgast, tall i unió, lubricació.",
             "Bieles i pedals: extracció, rosca, muntatge.",
             "Relació plats/pinyons (nocions)."],
  "sessions": [("Setmana 15 — La cadena",
                ["Mesura del desgast, tall i unió, lubricació (95').", "Diari (10')."]),
               ("Setmana 16 — Bieles i pedals",
                ["Extracció i muntatge; rosca dreta/esquerra (90').", "Diari (10')."]),
               ("Setmana 17 — Transmissió a punt",
                ["Pràctica completa a les bicis del taller (100')."])],
  "dua": ["Fitxa de passos del tall/unió amb fotos.",
          "Codi de colors dreta/esquerra per a la rosca.",
          "El desgast es llegeix amb el mesurador (visual)."],
  "materials": ["Cadenes, baules ràpides, tronxacadenes, extractor, lubricant.",
                "`Recursos/Llibre Manteniment Bici/Cap04_Transmision.pdf` (docent), "
                "`Recursos/canvi de marxes.docx`."],
  "fitxa": [("Com sé que una cadena està gastada:", "________________"),
            ("Un pedal es colla a l'esquerra o a la dreta?", "________________")],
  "aval": [("Diagnosi del desgast", "Prova amb el mesurador", "CA1.2"),
           ("Manteniment de cadena", "Observació", "CA1.3, CA2.2"),
           ("Diari del taller", "Pauta del diari", "CA4.1")]},

 {"video": ("Com ajustar el desviador (canvi) posterior (en castellà)", "oo8IIL2ofxY"),
  "code": "B6", "folder": "B6_Transmissio_II", "name": "Transmissió II: canvis i desviadors",
  "setm": "18–21", "producte": "Bici amb els **canvis ben ajustats**",
  "compl": "l'hora de maker **M6** (caixa classificadora de recanvis)",
  "desc": "Que una bici canviï de marxa suau i sense saltar separa una reparació correcta d'una excel·lent.",
  "repte": "Ajusta els canvis perquè pugin i baixin net i sense saltar.",
  "visible": ["Ajustar topalls (H/L) i tensió del canvi posterior.",
              "Ajustar el canvi davanter i alinear-lo.",
              "Provar el canvi i corregir si salta o frega."],
  "exit": ["He ajustat topalls i tensió del canvi posterior.",
           "He ajustat el canvi davanter.",
           "La bici canvia suau i no salta."],
  "sabers": ["Canvi posterior i davanter; desviadors.",
             "Ajust: topalls H/L, tensor, alineació.",
             "Diagnòstic de problemes de canvi."],
  "sessions": [("Setmana 18 — Canvi posterior: topalls i tensió",
                ["Demo (25').", "Ajust de topalls i tensió (65').", "Diari (10')."]),
               ("Setmana 19 — Canvi posterior: ajust fi",
                ["Afinament amb el tensor i prova (90').", "Diari (10')."]),
               ("Setmana 20 — Canvi davanter i alineació",
                ["Ajust del davanter i alineació (90').", "Diari (10')."]),
               ("Setmana 21 — Diagnosi encreuada",
                ["Cada parella ajusta una bici i una altra la prova i comenta (100')."])],
  "dua": ["Fitxa amb l'ordre d'ajust (primer topalls, després tensió).",
          "La diagnosi encreuada permet mostrar el que se sap ajudant.",
          "Qui domina ajuda els altres."],
  "materials": ["Canvis, cables, tensors, eines d'ajust.",
                "`Recursos/Llibre Manteniment Bici/Cap04_Transmision.pdf` (docent)."],
  "fitxa": [("L'ordre correcte per ajustar un canvi:", "________________"),
            ("Un problema de canvi i com el resoldria:", "________________")],
  "aval": [("Ajust dels canvis", "Observació + prova de marxes", "CA1.3"),
           ("Diagnosi encreuada", "Coavaluació entre parelles", "CA1.2, CA6.2"),
           ("Diari del taller", "Pauta del diari", "CA4.1")]},

 {"video": ("Com ajustar el seient: 3 ajustos bàsics (en castellà)", "iha16E-qMmc"),
  "code": "B7", "folder": "B7_Punts_de_contacte", "name": "Punts de contacte", "setm": "22–24",
  "producte": "Bici **ajustada a la persona**",
  "compl": "l'hora de maker **M7** (peces de confort i adaptadors)",
  "desc": "Una bici pot ser perfecta i incòmoda si no s'ajusta a qui la fa servir.",
  "repte": "Ajusta una bici a la persona que la farà servir: alçada, posició, direcció suau.",
  "visible": ["Ajustar l'alçada i la posició del seient.",
              "Ajustar el manillar i revisar el joc de direcció.",
              "Detectar què fa una bici incòmoda o insegura."],
  "exit": ["He ajustat el seient (alçada, avanç, inclinació).",
           "He revisat el joc de direcció i el manillar.",
           "La bici queda còmoda i segura."],
  "sabers": ["Seient: alçada, avanç, inclinació.",
             "Manillar, potència i joc de direcció.",
             "Ergonomia i confort."],
  "sessions": [("Setmana 22 — El seient",
                ["Alçada, avanç i inclinació; com es mesura (90').", "Diari (10')."]),
               ("Setmana 23 — Manillar i direcció",
                ["Potència, punys i joc de direcció (90').", "Diari (10')."]),
               ("Setmana 24 — Ergonomia",
                ["Ajust ergonòmic complet bici-usuari (100').",
                 "Tancament de trimestre: autoavaluació i coavaluació."])],
  "dua": ["Fitxa d'ajust amb referències corporals senzilles.",
          "L'ajust es comprova provant la bici (fent).",
          "Pensar «per a qui és» connecta amb l'ApS."],
  "materials": ["Tijas, potències, punys, eines d'ajust.",
                "`Recursos/Llibre Manteniment Bici/Cap05_puntos de contacto.pdf` (docent), "
                "`Recursos/el seient.docx`."],
  "fitxa": [("Com sé que el seient està a l'alçada correcta:", "________________"),
            ("Un senyal que la direcció té joc:", "________________")],
  "aval": [("Ajust dels punts de contacte", "Observació + prova", "CA1.3"),
           ("Ergonomia bici-usuari", "Prova bici-usuari", "CA1.2"),
           ("Diari del taller", "Pauta del diari", "CA4.1")]},

 {"video": ("20 normes de circulació per a bicicletes (DGT, en castellà)", "HnpAjaHac9o"),
  "code": "B8", "folder": "B8_Seguretat_viaria", "name": "Seguretat i normativa viària",
  "setm": "25–27", "producte": "Bici **equipada i legal** per circular",
  "compl": "l'hora de maker **M8** (suports de llum i suport de càmera 360)",
  "desc": "Abans de sortir al carrer, la bici ha de ser visible i legal i cal conèixer les normes.",
  "repte": "Deixa una bici equipada i legal per circular i coneix les normes de circulació.",
  "visible": ["Muntar i comprovar llums, reflectors i timbre.",
              "Conèixer les normes bàsiques de circulació per a bicicletes."],
  "exit": ["La bici té llums, reflectors i timbre, i tot funciona.",
           "Sé les normes bàsiques (per on circular, senyals, prioritats)."],
  "sabers": ["Enllumenat i seguretat passiva: llums, reflectors, casc.",
             "Normativa viària per a bicicletes."],
  "sessions": [("Setmana 25 — Enllumenat i accessoris",
                ["Muntatge i comprovació de llums, reflectors i timbre (90').", "Diari (10')."]),
               ("Setmana 26 — Normativa viària",
                ["Normes de circulació; casos pràctics al pati (100')."]),
               ("Setmana 27 — Preparació de la sortida",
                ["Revisió completa de les bicis + protocol de grup (100')."])],
  "dua": ["Pictogrames de senyals; checklist d'enllumenat.",
          "Els casos es resolen movent-se pel pati (fent).",
          "Preparar-se per sortir al carrer és molt motivador."],
  "materials": ["Llums, reflectors, timbres, cascos, armilles.",
                "`Recursos/Llibre Manteniment Bici/Cap09_seguridad proteccion y accesorios.pdf` (docent)."],
  "fitxa": [("Tres coses que fan visible una bici:", "________________"),
            ("Una norma de circulació que no sabia:", "________________")],
  "aval": [("Bici equipada i legal", "Checklist d'enllumenat", "CA1.4"),
           ("Normes de circulació", "Casos pràctics al pati", "CA5.1"),
           ("Diari del taller", "Pauta del diari", "CA4.1")]},

 {"video": ("Normes de circulació i seguretat vial per a ciclistes (en castellà)", "6Zmc18NzWeg"),
  "code": "B9", "folder": "B9_Repara_i_Roda", "name": "Repara i Roda (sortides)", "setm": "28–35",
  "producte": "**Bicis acabades i donades** + exposició",
  "compl": "l'hora de maker **M9** (rutes virtualitzades 360/VR per a l'exposició)",
  "desc": "Sortim al carrer amb les bicis reparades, apliquem les normes i acabem amb l'exposició.",
  "repte": "Acaba les bicis, surt a rodar amb seguretat i dona-les a la comunitat.",
  "visible": ["Circular pel carrer amb seguretat i aplicant les normes.",
              "Analitzar infraestructures i comportaments viaris.",
              "Lliurar una bici reparada a la comunitat."],
  "exit": ["He fet les sortides circulant amb seguretat.",
           "La meva bici està acabada i llesta per donar.",
           "He participat a l'exposició pública."],
  "sabers": ["Circulació urbana real: ordre de marxa, normes, anàlisi d'infraestructures.",
             "Comprovació final de seguretat abans de donar la bici.",
             "Aprenentatge servei: donació i certificació."],
  "sessions": [("Setmanes 28–32 — Sortides urbanes",
                ["Una sortida per setmana (revisió prèvia, ordre de marxa, normes).",
                 "Cicle preparació → execució → reflexió al diari.",
                 "Cal autoritzacions (`Normativa/Autoritzacio_families_sortides.md`)."]),
               ("Setmana 33 — Reparació final",
                ["Acabar les bicis pendents; comprovació final de seguretat (100')."]),
               ("Setmana 34 — Preparació de l'exposició",
                ["Assaig i revisió final de totes les bicis (100')."]),
               ("Setmana 35 — Exposició i donació",
                ["Exposició pública, donació de les bicis i certificats."])],
  "dua": ["El visionat VR previ (a l'hora de maker) redueix l'ansietat de la sortida.",
          "Cadascú aporta a l'exposició des del que se li dona millor.",
          "Públic real i bicis que canvien de mans."],
  "materials": ["Bicis reparades, cascos, armilles, kit portàtil.",
                "`Normativa/Autoritzacio_families_sortides.md`.",
                "Imprimible: `Normativa/Fitxa_sortida_bici.pdf` (una per alumne i sortida)."],
  "imprimibles": [("Fitxa de sortida en bicicleta (PDF)", "Fitxa_sortida_bici.pdf"),
                  ("Diari setmanal (PDF)", "Diari_setmanal_paper.pdf")],
  "fitxa": [("Una cosa que he vist del carrer i milloraria:", "________________"),
            ("La bici que he reparat es donarà a:", "________________")],
  "aval": [("Comportament a les sortides", "Fitxa de sortida + observació", "CA5.2, CA5.3"),
           ("Bici acabada i donada", "Comprovació final", "CA1.4, CA6.3"),
           ("Diari del taller", "Pauta del diari", "CA4.1")]},
]

# ─────────────────────────── DADES: MAKER (M0–M9) ───────────────────────────
MAKER = [
 {"video": ("Vídeo càpsula: la impressió 3D (en català, Ajuntament de Girona)", "wQZB0LrQ9-s"),
  "bloc": "🧊 3D",
  "code": "M0", "folder": "M0_Benvinguda_maker", "name": "Benvinguda maker i seguretat",
  "setm": "1–2", "producte": "**Carnet de màquina** (làser i 3D)",
  "compl": "el taller de bicicletes (les peces que farem serviran per a les bicis)",
  "desc": "L'aula maker fabrica peces i eines reals per al taller de bicicletes. Aquest curs treballem en tres blocs: primer impressió 3D, després tall làser i, si hi ha temps, un recorregut 360. Primer de tot: conèixer l'aula i treballar-hi amb seguretat.",
  "repte": "Guanya't el carnet de màquina: demostra que saps operar la 3D i la làser amb seguretat.",
  "visible": ["Conèixer la impressora 3D i la làser i què fabricarem tot el curs.",
              "Saber les normes de seguretat de les màquines."],
  "exit": ["Sé què fabricarem: peces 3D, després peces a làser i, si hi ha temps, el 360.",
           "Tinc el carnet de màquina (nivell làser i nivell 3D)."],
  "sabers": ["L'aula maker: impressora 3D Bambu Lab P2S i làser xTool S1.",
             "Els tres blocs del curs: 3D, làser i 360.",
             "Seguretat de màquines: materials, ventilació, parts calentes."],
  "sessions": [("Setmana 1 — L'aula i el pla del curs",
                ["Què fabricarem: exemples de peces per a la bici (20').",
                 "Les màquines i les normes de seguretat; demostració (30').",
                 "Diari (cara B) (10')."]),
               ("Setmana 2 — Carnet de màquina",
                ["Repàs de seguretat (15').",
                 "Checkpoint del carnet de màquina (`Normativa/Carnet_de_maquina.md`) (35').",
                 "Diari (10')."])],
  "dua": ["Demostració física de les màquines.",
          "El checkpoint es supera fent (posar material, aturada d'emergència).",
          "Carnet 🔵 amb variant «guia» per a qui no operi."],
  "materials": ["Impressora 3D i làser (demostració).",
                "Imprimible: `Normativa/Passaport_alumne.pdf`."],
  "fitxa": [("La norma de seguretat més important de les màquines:", "________________"),
            ("Una peça que vull fabricar aquest curs:", "________________")],
  "imprimibles": [("Contracte d'aula i carnet de màquina (PDF)", "Contracte_carnet_maker.pdf"),
                  ("Diari setmanal (PDF)", "Diari_setmanal_paper.pdf")],
  "aval": [("Carnet de màquina", "Checkpoint pràctic", "CA1.4"),
           ("Seguretat a l'aula maker", "Observació", "CA1.4, CA6.1"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Tinkercad: primers passos de disseny 3D (en castellà)", "csvBRWfgf1I"),
  "bloc": "🧊 3D",
  "code": "M1", "folder": "M1_Tinkercad", "name": "Tinkercad des de zero", "setm": "3–5",
  "producte": "**Primer objecte 3D propi** (imprès)",
  "compl": "el taller de bicicletes (aviat dissenyaràs peces per a la bici)",
  "desc": "Aprens a fer servir Tinkercad des de zero: com s'hi entra, com és per dins i com fer el primer disseny en 3D.",
  "repte": "Dissenya el teu primer objecte 3D i imprimeix-lo.",
  "visible": ["Entrar a Tinkercad amb el compte de classe.",
              "Moure, girar i escalar formes al pla de treball.",
              "Exportar el disseny a STL per imprimir."],
  "exit": ["Sé entrar a Tinkercad i moure'm per la interfície.",
           "He fet un disseny senzill combinant formes.",
           "He exportat l'STL i s'ha imprès."],
  "sabers": ["Tinkercad: compte de classe, interfície, formes, forats, agrupar.",
             "Pla de treball i mides en mm.",
             "Exportació a STL i enviament a impressió."],
  "sessions": [("Setmana 3 — Entrar i moure's",
                ["Registre amb el codi de classe; tour de la interfície (20').",
                 "Arrossegar formes; moure, girar i escalar (30').", "Diari (10')."]),
               ("Setmana 4 — Primer disseny",
                ["Combinar formes plenes i forats; agrupar (30').",
                 "Disseny lliure senzill (p. ex. una placa amb la teva inicial) (20').", "Diari (10')."]),
               ("Setmana 5 — Imprimir",
                ["Exportar STL; com es prepara la impressió (25').",
                 "Impressió per tandes; observar la màquina (25').", "Diari (10')."])],
  "dua": ["Fitxa visual pas a pas de Tinkercad.",
          "Plantilla d'inici amb formes ja posades.",
          "Producte personal i immediat."],
  "materials": ["Chromebooks amb Tinkercad (web); impressora 3D; material d'impressió."],
  "fitxa": [("El meu usuari de Tinkercad:", "________________"),
            ("Què he dissenyat:", "________________")],
  "aval": [("Ús bàsic de Tinkercad", "Observació + criteris d'èxit", "CA3.1"),
           ("Primer objecte imprès", "El disseny imprès", "CA3.1, CA3.2"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Com usar el peu de rei (calibre): parts i mesura (en castellà)", "qStcdgxZPec"),
  "bloc": "🧊 3D",
  "code": "M2", "folder": "M2_Peu_de_rei", "name": "Mesurar amb el peu de rei", "setm": "6–8",
  "producte": "**Peça senzilla** dissenyada a mida real",
  "compl": "el taller de bicicletes (mesuraràs peces reals de la bici)",
  "desc": "Per fabricar peces que encaixin cal mesurar bé. Aprens a fer servir el peu de rei i a passar les mides al disseny.",
  "repte": "Mesura un objecte real amb el peu de rei i reprodueix-lo a mida a Tinkercad.",
  "visible": ["Llegir mides amb el peu de rei (en mm).",
              "Dibuixar un plànol 2D senzill acotat.",
              "Reproduir les mides a Tinkercad."],
  "exit": ["Sé mesurar amb el peu de rei.",
           "He fet un plànol 2D amb les mides.",
           "He reproduït la peça a mida a Tinkercad."],
  "sabers": ["El peu de rei: parts i lectura en mm.",
             "Cotes bàsiques i toleràncies (l'encaix).",
             "Del plànol 2D al model 3D."],
  "sessions": [("Setmana 6 — El peu de rei",
                ["Com es llegeix el peu de rei; pràctica amb objectes (30').",
                 "Plànol 2D acotat d'un objecte senzill (20').", "Diari (10')."]),
               ("Setmana 7 — Al Tinkercad",
                ["Reproduir les mides al pla de treball (40').", "Diari (10' + revisió de mides)."]),
               ("Setmana 8 — Imprimir i comparar",
                ["Imprimir i comparar amb l'original amb el peu de rei (40').", "Diari (10')."])],
  "dua": ["Peu de rei digital si costa la lectura de l'escala.",
          "Plantilla de plànol acotat.",
          "Es valida comparant amb l'original (visual)."],
  "materials": ["Peus de rei; objectes de mostra; Chromebooks; impressora 3D."],
  "fitxa": [("La mida més gran que he mesurat:", "______ mm"),
            ("La meva peça encaixa amb l'original?", "sí / cal ajustar")],
  "aval": [("Lectura del peu de rei", "Observació", "CA3.1"),
           ("Peça a mida real", "Comparació amb l'original", "CA3.1, CA3.2"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Tinkercad: modelatge 3D de peces (en castellà)", "xvt7D38CYFQ"),
  "bloc": "🧊 3D",
  "code": "M3", "folder": "M3_Enginyeria_inversa", "name": "Enginyeria inversa: la maneta de fre",
  "setm": "9–11", "producte": "**Rèplica 3D d'una maneta de fre**",
  "compl": "el taller de bicicletes (la maneta és una peça real del fre)",
  "desc": "A partir d'una maneta de fre real, en fem el plànol i la reproduïm en 3D per imprimir-la.",
  "repte": "Copia una maneta de fre real: plànol 2D, model 3D i impressió que encaixi.",
  "visible": ["Mesurar la maneta amb el peu de rei.",
              "Fer-ne el plànol 2D acotat.",
              "Modelar-la a Tinkercad i imprimir-la."],
  "exit": ["He mesurat i dibuixat la maneta.",
           "L'he modelada a Tinkercad.",
           "L'he impresa i he provat l'encaix."],
  "sabers": ["Enginyeria inversa: de l'objecte al model.",
             "Cotes crítiques (pivot, forats).",
             "Iteració segons la prova d'encaix."],
  "sessions": [("Setmana 9 — Mesurar i dibuixar",
                ["El docent lliura una maneta; mesura amb el peu de rei (25').",
                 "Plànol 2D acotat (vista superior i lateral) (25').", "Diari (10')."]),
               ("Setmana 10 — Modelar",
                ["Model 3D a Tinkercad a partir del plànol (40').", "Diari (10' + revisió de mides)."]),
               ("Setmana 11 — Imprimir i ajustar",
                ["Impressió i prova d'encaix; iteració (40').", "Diari (10')."])],
  "dua": ["Plànol amb algunes cotes ja marcades per a qui ho necessiti.",
          "Es valida fent (prova d'encaix real).",
          "Treball en parella."],
  "materials": ["Manetes de fre reals; peus de rei; Chromebooks; impressora 3D."],
  "fitxa": [("La cota crítica de la maneta:", "______ mm"),
            ("Encaixa a la bici?", "sí / cal ajustar")],
  "aval": [("Plànol i model", "Criteris d'èxit + rúbrica", "CA3.1"),
           ("Impressió i encaix", "La peça provada", "CA3.2, CA3.3"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Tinkercad: modelatge i disseny 3D per a principiants (en castellà)", "IVxa96tfey8"),
  "bloc": "🧊 3D",
  "code": "M4", "folder": "M4_Peces_utils", "name": "Peces útils per a la bici (3D)", "setm": "12–14",
  "producte": "**Peça útil** impresa i provada al taller",
  "compl": "el taller de bicicletes (la peça ajuda en una reparació o millora)",
  "desc": "Cada parella tria una peça útil del catàleg, la dissenya i la prova a la bici.",
  "repte": "Fabrica una peça útil per a la bici i comprova que funciona.",
  "visible": ["Triar una peça del catàleg i mesurar-ne les mides.",
              "Dissenyar-la a Tinkercad.",
              "Provar-la al taller i millorar-la."],
  "exit": ["He triat i dissenyat una peça útil.",
           "L'he impresa.",
           "L'he provada a la bici i millorada si calia."],
  "sabers": ["Disseny de peces funcionals a mida.",
             "Tria segons la necessitat del taller.",
             "Prova i iteració."],
  "sessions": [("Setmana 12 — Tria i disseny",
                ["Triar del catàleg (tapa de puny, clip passacables, separador de pastilles, "
                 "tapa de vàlvula, clip de llum, protector de beina) i mesurar (30').",
                 "Disseny a Tinkercad (20').", "Diari (10')."]),
               ("Setmana 13 — Impressió i prova",
                ["Impressió i primera prova a la bici (40').", "Diari (10')."]),
               ("Setmana 14 — Millora",
                ["Ajust i reimpressió si cal; acabats (40').", "Diari (10')."])],
  "dua": ["Catàleg amb imatges i nivell de dificultat.",
          "Es valida fent (a la bici real).",
          "L'error és informació: es millora."],
  "materials": ["Chromebooks; impressora 3D; bicis del taller; peus de rei."],
  "fitxa": [("Quina peça he triat:", "________________"),
            ("Funciona a la bici?", "sí / cal millorar")],
  "aval": [("Peça útil fabricada", "Criteris d'èxit", "CA3.2"),
           ("Prova i millora", "Peça provada a la bici", "CA3.3"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Dissenyar un clauer 3D a Tinkercad + impressió (en castellà)", "ecvAFxZ6o6o"),
  "bloc": "🧊 3D",
  "code": "M5", "folder": "M5_Decoratives", "name": "Peces decoratives temàtica bici (3D)", "setm": "15–17",
  "producte": "**Objecte decoratiu** propi (temàtica bici)",
  "compl": "el taller de bicicletes (temàtica ciclista; per a l'exposició i els certificats)",
  "desc": "Dissenyem objectes decoratius amb temàtica de bici per a l'exposició i els records del curs.",
  "repte": "Dissenya i imprimeix un objecte decoratiu amb temàtica de bici.",
  "visible": ["Triar un objecte decoratiu (clauer baula, tapa de vàlvula, imant silueta, pin «Mecànic Júnior», marcador).",
              "Dissenyar-lo a Tinkercad.",
              "Imprimir-lo i acabar-lo."],
  "exit": ["He triat i dissenyat un objecte decoratiu.",
           "L'he imprès.",
           "Té bon acabat per a l'exposició."],
  "sabers": ["Disseny 3D creatiu (estètica).",
             "Text i relleu a Tinkercad.",
             "Acabats."],
  "sessions": [("Setmana 15 — Idea i disseny",
                ["Triar l'objecte i dissenyar-lo (text/relleu) (40').", "Diari (10')."]),
               ("Setmana 16 — Impressió",
                ["Impressió per tandes (40').", "Diari (10')."]),
               ("Setmana 17 — Acabats",
                ["Neteja, poliment i preparació per a l'exposició (40').", "Diari (10')."])],
  "dua": ["Galeria d'exemples per inspirar-se.",
          "Plantilla amb el text ja posat.",
          "Producte personal (motivador)."],
  "materials": ["Chromebooks; impressora 3D; material d'acabats."],
  "fitxa": [("El meu objecte decoratiu:", "________________"),
            ("On el posaré / a qui el donaré:", "________________")],
  "aval": [("Objecte decoratiu", "Criteris d'èxit", "CA3.2"),
           ("Acabat i presentació", "L'objecte per a l'exposició", "CA4.2"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Fer una caixa per a tall làser amb MakerCase (en castellà)", "i7H9dgyfM1Q"),
  "code": "M6", "folder": "M6_Classificadora", "name": "Caixa classificadora", "setm": "18–21",
  "producte": "**Caixa classificadora de recanvis** + magatzem ordenat",
  "compl": "l'hora de bicicletes **B6** (transmissió II)",
  "desc": "Organitzem el magatzem de recanvis amb una caixa classificadora modular.",
  "repte": "Fabrica una caixa classificadora i ordena el magatzem de recanvis.",
  "visible": ["Dissenyar una caixa modular amb compartiments.",
              "Tallar i muntar la classificadora.",
              "Organitzar i retolar el magatzem."],
  "exit": ["He dissenyat la classificadora (mòduls).",
           "L'he tallada i muntada.",
           "El magatzem de recanvis està ordenat."],
  "sabers": ["Disseny modular per a làser (encaixos).",
             "Organització i retolació d'un magatzem."],
  "sessions": [("Setmana 18 — Disseny",
                ["Disseny de la caixa classificadora (mòduls) (50').", "Diari (10')."]),
               ("Setmana 19 — Fabricació",
                ["Tall làser i muntatge (50').", "Diari (10')."]),
               ("Setmana 20 — Suports",
                ["Suports i millores per als peus de treball (50').", "Diari (10')."]),
               ("Setmana 21 — Organització final",
                ["Organització del magatzem amb la classificadora (50')."])],
  "dua": ["Plantilla modular.",
          "El resultat s'usa al magatzem (reconeixement).",
          "Treball per parelles."],
  "materials": ["Làser; material de fabricació."],
  "fitxa": [("Quants compartiments té la caixa:", "______"),
            ("Per a què serveix cada compartiment:", "________________")],
  "aval": [("Caixa classificadora", "Criteris d'èxit", "CA3.1, CA3.2"),
           ("Magatzem ordenat", "La caixa en ús", "CA3.3"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Tinkercad: modelatge i disseny 3D per a principiants (en castellà)", "IVxa96tfey8"),
  "code": "M7", "folder": "M7_Confort", "name": "Peces de confort", "setm": "22–24",
  "producte": "**Peces de confort i adaptadors** 3D, provats",
  "compl": "l'hora de bicicletes **B7** (punts de contacte)",
  "desc": "Fabriquem peces de confort i adaptadors a mida per a les bicis del taller.",
  "repte": "Fabrica una peça de confort que millori una bici i prova-la.",
  "visible": ["Dissenyar peces de confort (topalls, proteccions, separadors).",
              "Imprimir adaptadors personalitzats.",
              "Provar i iterar les peces."],
  "exit": ["He dissenyat una peça de confort 3D.",
           "L'he impresa i provada.",
           "L'he millorada si calia."],
  "sabers": ["Modelatge 3D d'adaptadors a mida.",
             "Mesura de la persona/bici per personalitzar."],
  "sessions": [("Setmana 22 — Disseny de peces de confort",
                ["Disseny (topalls, proteccions, separadors) (50').", "Diari (10')."]),
               ("Setmana 23 — Adaptadors",
                ["Impressió d'adaptadors personalitzats (50').", "Diari (10')."]),
               ("Setmana 24 — Prova i iteració",
                ["Prova i iteració de les peces de confort (50')."])],
  "dua": ["Referències de mida senzilles.",
          "Es prova fent (a la bici real).",
          "Personalització (motivador)."],
  "materials": ["Impressora 3D; material de fabricació."],
  "fitxa": [("Què és la meva peça i què millora:", "________________"),
            ("Funciona?", "sí / cal millorar-la")],
  "aval": [("Peça de confort fabricada", "Criteris d'èxit", "CA3.2"),
           ("Prova i iteració", "Peça provada", "CA3.3"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Càmera 360 Insta360 X3: guia d'iniciació (en castellà)", "1uRtvs1_V5w"),
  "code": "M8", "folder": "M8_Suports_i_360", "name": "Suports i captura 360", "setm": "25–27",
  "producte": "**Suport de càmera 360** + iniciació a la captura 360",
  "compl": "l'hora de bicicletes **B8** (seguretat i normativa viària)",
  "desc": "Fabriquem suports (llum, mòbil, càmera 360) i ens iniciem en la captura 360 i el visor VR.",
  "repte": "Fabrica el suport de càmera 360 per a la bici i fes una primera captura 360.",
  "visible": ["Dissenyar i imprimir suports de llum/mòbil i de càmera 360.",
              "Fer una captura 360 senzilla i visualitzar-la.",
              "Fer un ús segur del visor VR."],
  "exit": ["He fabricat el suport de càmera 360 i s'aguanta a la bici.",
           "He fet una captura 360 i l'he visualitzada.",
           "Tinc el carnet de càmera 360 / VR."],
  "sabers": ["Impressió 3D de suports funcionals.",
             "Captura 360 (imatge equirectangular) i visor VR."],
  "sessions": [("Setmana 25 — Suports de llum/mòbil",
                ["Suports impresos en 3D (50').", "Diari (10')."]),
               ("Setmana 26 — Suport de càmera 360",
                ["Disseny i impressió del suport de càmera 360 (50').", "Diari (10')."]),
               ("Setmana 27 — Iniciació 360/VR",
                ["Captura 360 i visor VR; protocol (`Normativa/Protocol_us_VR.md`) (50')."])],
  "dua": ["Vídeo curt de captura 360.",
          "Carnet 🔵 amb variant «guia VR».",
          "Es prepara per a les rutes del 3r trimestre."],
  "materials": ["Impressora 3D, càmera 360, ulleres VR.",
                "`Normativa/Protocol_us_VR.md`, `Normativa/Autoritzacio_families_VR_360.md`."],
  "fitxa": [("El suport de càmera 360 s'aguanta bé?", "sí / cal millorar-lo"),
            ("Què m'ha sorprès de la captura 360:", "________________")],
  "aval": [("Suport de càmera 360", "Criteris d'èxit", "CA3.2"),
           ("Captura 360", "La captura visualitzada", "CA4.2"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},

 {"video": ("Editar vídeo 360 amb Insta360 Studio (en castellà)", "EaZrXTpGSkI"),
  "code": "M9", "folder": "M9_Rutes_VR", "name": "Rutes virtualitzades 360/VR", "setm": "28–35",
  "producte": "**Col·lecció de rutes 360/VR** + estació VR per a l'exposició",
  "compl": "l'hora de bicicletes **B9** (sortides i exposició)",
  "desc": "Documentem les sortides en 360 i muntem rutes virtualitzades per a l'exposició pública.",
  "repte": "Grava, edita i munta les rutes 360/VR i prepara l'estació VR de l'exposició.",
  "visible": ["Capturar en 360 durant les sortides.",
              "Editar i muntar una ruta virtualitzada.",
              "Preparar i guiar l'estació VR de l'exposició."],
  "exit": ["He contribuït a la col·lecció de rutes 360/VR.",
           "He visionat en VR una ruta abans de fer-la.",
           "He col·laborat en l'estació VR de l'exposició."],
  "sabers": ["Captura, edició i muntatge de rutes 360.",
             "Visor VR: anticipació (previ a la sortida) i documentació.",
             "Comunicació: estació VR a l'exposició."],
  "sessions": [("Setmanes 28–32 — Captura i edició",
                ["Descàrrega i edició del 360 de cada sortida.",
                 "Visionat VR de la ruta següent abans de fer-la."]),
               ("Setmana 33 — Col·lecció de rutes",
                ["Muntatge de la col·lecció de rutes virtualitzades (50')."]),
               ("Setmana 34 — Estació VR",
                ["Material de l'exposició i muntatge de l'estació VR (50')."]),
               ("Setmana 35 — Exposició",
                ["Estació VR oberta: els visitants «roden» les rutes. Tancament de curs."])],
  "dua": ["El visionat VR previ ajuda a anticipar la ruta (clau per a NEE).",
          "Cadascú aporta des del que se li dona millor.",
          "Producte que es mostra al públic."],
  "materials": ["Càmera 360, ulleres VR, ordinadors; material d'exposició.",
                "`Normativa/Protocol_us_VR.md`."],
  "fitxa": [("Què m'ha ajudat veure la ruta abans en VR:", "________________"),
            ("Què faré a l'estació VR de l'exposició:", "________________")],
  "aval": [("Rutes 360/VR", "Producte + criteris d'èxit", "CA4.2"),
           ("Exposició (estació VR)", "Rúbrica de producte final", "CA4.3, CA6.3"),
           ("Diari (cara B)", "Pauta del diari", "CA4.1")]},
]


def escriu(track, dades):
    base = os.path.join(ARREL, "Classes",
                        "Bicicletes" if track == "bicicletes" else "Maker")
    for s in dades:
        carpeta = os.path.join(base, s["folder"])
        os.makedirs(carpeta, exist_ok=True)
        with open(os.path.join(carpeta, s["code"] + ".md"), "w", encoding="utf-8") as f:
            f.write(sa_md(track, s))
        with open(os.path.join(carpeta, "Fitxa_alumnat.md"), "w", encoding="utf-8") as f:
            f.write(fitxa_md(track, s))


if __name__ == "__main__":
    escriu("bicicletes", BICI)
    escriu("maker", MAKER)
    print(f"Generades {len(BICI)} SA de Bicicletes i {len(MAKER)} SA de Maker.")
