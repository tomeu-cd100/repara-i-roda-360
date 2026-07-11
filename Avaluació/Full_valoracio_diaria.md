# Full de valoració diària del docent — «Repara i Roda 360»

> **Instrument d'avaluació ràpida de cada sessió.** El docent valora cada alumne/a al **taller
> de bicicletes** i a l'**aula maker** amb codis d'un cop d'ull. Es fa servir imprès (un full
> per sessió) i després es buida al `Full_seguiment_grup.md` i al `Full_progres_competencial.md`.
>
> 📄 **Versió imprimible:** `Full_valoracio_diaria.pdf` (A4 apaïsat, 12 alumnes). Es regenera
> amb `py -3.11 scripts/genera_full_valoracio.py` (canvieu `NObiles` per a més o menys files).

## Estructura del full

Capçalera: **Data · Setmana · SA · quin espai s'avalua avui** (taller 2h / maker 1h).

Una fila per alumne/a amb columnes agrupades:

| Bloc | Columna | Criteri |
|------|---------|---------|
| **Taller de bicicletes** | Seguretat | CA1.4 |
| | Tècnica | CA1/CA2 (diagnosi i reparació) |
| | Ordre i eines | CA2.3 |
| | Parella | CA6.1 |
| **Aula maker** | Seguretat | CA1.4 (làser/3D) |
| | Fabricació | CA3 (disseny i fabricació) |
| | Autonomia | CA3.3 / autoregulació |
| **Comú** | Diari | CA4.1 (cara A i B) |
| | Observacions | nota lliure |

## Codis de valoració

- **+** ho fa bé / amb autonomia
- **=** correcte / se'n surt amb suport
- **!** cal atenció / encara no
- **A** absent
- (Opcional) semàfor: **V** verd · **G** groc · **R** vermell

## Com s'usa

1. Els dies de **només taller** o **només maker** s'omplen les columnes del bloc corresponent
   (les altres es deixen buides).
2. En acabar la setmana, es traslladen els codis al `Full_seguiment_grup.md` (observació
   contínua de C3 i C8).
3. En tancar cada SA, la síntesi alimenta el `Full_progres_competencial.md` (nivell de les CE).

> El full **no posa nota**: recull evidència d'observació diària per a la valoració global
> qualitativa (vegeu `Criteris_i_qualificacio.md`).
