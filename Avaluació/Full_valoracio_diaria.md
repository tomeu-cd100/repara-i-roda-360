# Fulls de valoració diària del docent — «Repara i Roda 360»

> Hi ha **dos** fulls per avaluar cada dia, tria segons el que et convingui:
>
> 📄 **Per alumne (checklist):** `Full_valoracio_alumne.pdf` — 2 fitxes per full. Per a cada
> alumne/a, llista de coses que **compleix** o **encara no** té assolides, incloent-hi les
> **normes del taller**. Ideal per a un seguiment detallat i individual. Es regenera amb
> `py -3.11 scripts/genera_valoracio_alumne.py`.
>
> 🗂️ **De grup (graella):** `Full_valoracio_diaria.pdf` — A4 apaïsat amb tot el grup d'un cop
> d'ull (taller + aula maker), amb codis ràpids. Es regenera amb
> `py -3.11 scripts/genera_full_valoracio.py` (canvieu `NObiles` per a més o menys files).
>
> Tots dos es buiden després al `Full_seguiment_grup.md` i al `Full_progres_competencial.md`.

## Estructura de la graella de grup

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
