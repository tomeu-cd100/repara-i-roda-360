# Plantilles SVG per a l'aula maker

Fitxers de partida per a l'alumnat, en **mil·límetres reals** (1 unitat SVG = 1 mm),
llestos per obrir amb **Inkscape** o **xTool Creative Space**.

## Convenció de colors (capes)

| Color | Codi | Significat a la làser |
|---|---|---|
| 🔴 Vermell | `#FF0000` | **TALL** (contorn, forats) |
| ⚫ Negre | `#000000` | **GRAVAT** (text, logos — raster) |
| 🔵 Blau | `#0000FF` | **Marca / score** (línia gravada fina, opcional) |

> Comprova sempre potència i velocitat en un tros de material de prova abans de tallar la peça bona.

## Plantilles

| Fitxer | Unitat | Què és | Personalitza |
|---|---|---|---|
| [placa_identificativa.svg](placa_identificativa.svg) | M7 | Placa 60×25 mm amb número de bici i forat Ø4 | El text `BICI NN` |
| [etiqueta_organitzador.svg](etiqueta_organitzador.svg) | M7 | Etiqueta penjant per a eines o calaixos | El text `NOM EINA` |
| [regle_desgast_cadena.svg](regle_desgast_cadena.svg) | M7 | Regle de desgast de cadena (marca `nova` i `0,5%`) | Res; comprova la mida en imprimir/tallar |

Totes tres són del bloc làser: es preparen a **M6** (Inkscape i codis de color) i es tallen a
**M7** (peces útils). Els rètols i la decoració de **M8** parteixen de zero o d'aquestes mateixes
convencions.

## Peces amb encaix (caixes)

La **caixa-kit** (M7) es fa millor amb un generador d'encaixos: **MakerCase**
(`makercase.com`) — hi ha vídeo-tutorial enllaçat a la unitat M7.
Exporta l'SVG, obre'l a Inkscape i aplica-hi la convenció de colors d'aquí dalt.

## Peces 3D

Les peces impreses (maneta M3, peces útils M4, decoratives M5, suport de càmera M9) es
dissenyen amb **Tinkercad** (vídeos enllaçats a les unitats), no amb SVG.
