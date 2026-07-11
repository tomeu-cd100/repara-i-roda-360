#!/usr/bin/env python3
"""Generador de la web estàtica de «Repara i Roda 360».

Converteix tots els .md del repositori a HTML dins de `web/`, amb una plantilla
compartida, enllaços interns reescrits (també les referències en `codi`) i
portades per a docents, alumnat i famílies. Mateix estil que els projectes
germans (Aula Maker, Robòtica).

Ús:  python build_web.py     (regenera web/ sencera)
Requereix: pip install markdown
"""

import html
import json
import re
import shutil
import unicodedata
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
OUT = ROOT / "web"

SECTIONS = [
    "Programació didàctica",
    "Classes",
    "Avaluació",
    "Normativa",
    "Memòria de treball",
    "Recursos",
]

SECTION_ICONS = {
    "Programació didàctica": "📚",
    "Classes": "🧩",
    "Avaluació": "📊",
    "Normativa": "🛡️",
    "Memòria de treball": "🗂️",
    "Recursos": "🧰",
}

SECTION_DESC = {
    "Programació didàctica": "PD, temporització, mapatge competencial i diari setmanal",
    "Classes": "SA0 i les 9 SA amb fitxa de l'alumnat i rúbrica",
    "Avaluació": "Criteris, rúbriques, fulls de seguiment i el full de valoració diària",
    "Normativa": "Seguretat, carnets, protocol VR, famílies i certificat",
    "Memòria de treball": "Diari docent, inventari, incidències i memòria final",
    "Recursos": "Material de referència del taller",
}

# (codi, nom, trimestre, "icona + producte", carpeta)
SA_CARDS = [
    ("SA0", "Punt de partida", "setm. 1-2", "📍 Carnets d'eines i de màquina", "SA0"),
    ("SA1", "La bici per dins", "1r trim.", "🚲 Fitxa de recepció + placa", "SA1"),
    ("SA2", "Posada a punt", "1r trim.", "🧼 M-check + organitzador d'eines", "SA2"),
    ("SA3", "Rodes i punxades", "1r trim.", "🛞 Punxada reparada + kit", "SA3"),
    ("SA4", "Frens", "1r-2n trim.", "🛑 Frens segurs + peces 3D", "SA4"),
    ("SA5", "Transmissió I", "2n trim.", "🔩 Cadena + mesurador de desgast", "SA5"),
    ("SA6", "Transmissió II", "2n trim.", "⚙️ Canvis ajustats + classificadora", "SA6"),
    ("SA7", "Punts de contacte", "2n trim.", "🪑 Bici ajustada + peça de confort", "SA7"),
    ("SA8", "Seguretat i accessoris", "3r trim.", "💡 Bici legal + suport càmera 360", "SA8"),
    ("SA9", "Repara i Roda", "3r trim. ⭐", "🚦 Sortides, rutes VR i exposició", "SA9"),
]

ALUMNAT_LINKS = [
    ("📓", "El diari setmanal", "Programació didàctica/Diari_setmanal_paper.md",
     "Com és el teu full de cada setmana (taller i maker)"),
    ("📖", "Vocabulari bàsic", "Classes/SA0/Vocabulari_basic.md",
     "Les paraules de mecànic, curt i clar"),
    ("🔍", "Com m'avaluaran?", "Avaluació/Criteris_i_qualificacio.md",
     "El sistema d'avaluació explicat"),
    ("🌱", "Autoavaluació i coavaluació", "Avaluació/Autoavaluacio_coavaluacio.md",
     "Com valores la teva feina i la dels companys"),
    ("🛡️", "Normes de seguretat", "Normativa/Normes_seguretat_taller.md",
     "Lectura obligatòria abans de tocar res"),
    ("🎫", "Carnets d'eines i màquina", "Normativa/Carnet_de_maquina.md",
     "Sense carnet no s'opera"),
    ("🥽", "Protocol de la realitat virtual", "Normativa/Protocol_us_VR.md",
     "Temps, higiene i seguretat amb les ulleres"),
    ("🏅", "El certificat final", "Normativa/Certificat_mecanic_junior.md",
     "Mecànic/a Júnior: el que t'enduràs"),
]

DOCENT_DESTACATS = [
    ("📚", "Programació didàctica", "Programació didàctica/Programacio_didactica_ReparaIRoda_4ESO.md",
     "La PD completa: 12 apartats"),
    ("🗓️", "Temporització anual", "Programació didàctica/Temporitzacio_anual.md",
     "35 setmanes, taller + maker"),
    ("🎯", "Mapatge competencial", "Programació didàctica/Mapatge_competencial_oficial.md",
     "CE oficials de Tecnologia 4t, verificades"),
    ("📊", "Criteris i qualificació", "Avaluació/Criteris_i_qualificacio.md",
     "Pesos, nivells i traçabilitat"),
    ("🗂️", "Full de valoració diària", "Avaluació/Full_valoracio_diaria.md",
     "El full (PDF) per avaluar cada dia taller i maker"),
    ("📓", "Diari setmanal (disseny)", "Programació didàctica/Diari_setmanal_paper.md",
     "El full de l'alumnat, a dues cares"),
]

MD = markdown.Markdown(extensions=["tables", "sane_lists", "fenced_code"])


def slugify(name: str) -> str:
    base = unicodedata.normalize("NFKD", name)
    base = "".join(c for c in base if not unicodedata.combining(c))
    base = base.lower().replace(" ", "-")
    base = re.sub(r"[^a-z0-9._/-]", "", base)
    return base


def collect_md_files():
    files = [p for p in sorted(ROOT.glob("*.md"))]
    for section in SECTIONS:
        d = ROOT / section
        if d.is_dir():
            files.extend(sorted(d.rglob("*.md")))
    return files


def out_path_for(md_path: Path) -> str:
    rel = md_path.relative_to(ROOT)
    return slugify(str(rel.with_suffix(".html")).replace("\\", "/"))


def page_title(md_text: str, fallback: str) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


MD_FILES = collect_md_files()
PATH_MAP = {}
for p in MD_FILES:
    rel = str(p.relative_to(ROOT)).replace("\\", "/")
    PATH_MAP[rel] = out_path_for(p)
    PATH_MAP[rel.replace(" ", "%20")] = out_path_for(p)
NAME_MAP = {}
for rel in list(PATH_MAP):
    if "%20" in rel:
        continue
    NAME_MAP.setdefault(rel.rsplit("/", 1)[-1], []).append(rel)

FOLDER_MAP = {f"{s}/": slugify(s) + "/index.html" for s in SECTIONS}
FOLDER_MAP.update({f"{s.replace(' ', '%20')}/": slugify(s) + "/index.html"
                   for s in SECTIONS})
FOLDER_MAP["web/"] = "index.html"


def resolve_ref(ref: str, current_rel_dir: str):
    ref = ref.strip().lstrip("./")
    if ref in PATH_MAP:
        return PATH_MAP[ref]
    if current_rel_dir:
        candidate = f"{current_rel_dir}/{ref}"
        if candidate in PATH_MAP:
            return PATH_MAP[candidate]
    name = ref.rsplit("/", 1)[-1]
    hits = NAME_MAP.get(name, [])
    if len(hits) == 1:
        return PATH_MAP[hits[0]]
    for h in hits:
        if current_rel_dir and h.startswith(current_rel_dir + "/"):
            return PATH_MAP[h]
    return None


def rel_prefix(out_rel: str) -> str:
    return "../" * out_rel.count("/")


def rewrite_links(html_text: str, out_rel: str, current_rel_dir: str) -> str:
    prefix = rel_prefix(out_rel)

    def fix_href(m):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        target = None
        if href.rstrip("/") + "/" in FOLDER_MAP or href in FOLDER_MAP:
            target = FOLDER_MAP.get(href, FOLDER_MAP.get(href.rstrip("/") + "/"))
        elif href.endswith(".md"):
            target = resolve_ref(href.replace("%20", " "), current_rel_dir)
        elif href.endswith(".pdf"):
            target = "impressos/" + href.rsplit("/", 1)[-1]
        if target:
            return f'href="{prefix}{target}"'
        return m.group(0)

    html_text = re.sub(r'href="([^"]+)"', fix_href, html_text)

    def fix_code(m):
        inner = m.group(1)
        clean = html.unescape(inner)
        base = re.split(r"\s*§", clean)[0].strip().rstrip("`").strip()
        target = None
        if base.endswith(".md"):
            target = resolve_ref(base, current_rel_dir)
        elif base.endswith(".pdf"):
            target = "impressos/" + base.rsplit("/", 1)[-1]
        elif base in FOLDER_MAP:
            target = FOLDER_MAP[base]
        if target:
            return f'<a class="doclink" href="{prefix}{target}"><code>{inner}</code></a>'
        return m.group(0)

    html_text = re.sub(r"<code>([^<]+)</code>", fix_code, html_text)

    def fix_src(m):
        src = m.group(1)
        if src.startswith(("http://", "https://", "data:")):
            return m.group(0)
        asset = src.replace("%20", " ").lstrip("./")
        cand = asset if (ROOT / asset).exists() else f"{current_rel_dir}/{asset}"
        if (ROOT / cand).exists():
            return f'src="{prefix}{slugify(cand)}"'
        return m.group(0)

    html_text = re.sub(r'src="([^"]+)"', fix_src, html_text)
    return html_text


def checkboxify(html_text: str) -> str:
    html_text = re.sub(r"<li>\[ \]", '<li class="task">☐', html_text)
    html_text = re.sub(r"<li>\[x\]", '<li class="task done">☑', html_text, flags=re.I)
    html_text = re.sub(r"<p>\[ \]", '<p class="task">☐', html_text)
    return html_text


def render_page(title, body, out_rel, crumb):
    prefix = rel_prefix(out_rel)
    crumb_html = " <span class=\"sep\">›</span> ".join(
        f'<a href="{prefix}{href}">{html.escape(text)}</a>' if href
        else f"<span>{html.escape(text)}</span>"
        for text, href in crumb)
    return f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · Repara i Roda 360</title>
<link rel="stylesheet" href="{prefix}assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🚲</text></svg>">
</head>
<body>
<a class="skip" href="#contingut">Salta al contingut ↓</a>
<header class="site-header">
  <a class="brand" href="{prefix}index.html">🚲 <strong>Repara i Roda 360</strong> <span>4t ESO</span></a>
  <nav>
    <a href="{prefix}index.html">Inici</a>
    <a href="{prefix}sa.html">Les SA</a>
    <a href="{prefix}docent.html">Docent</a>
    <a href="{prefix}alumnat.html">Alumnat</a>
    <a href="{prefix}families.html">Famílies</a>
    <a href="{prefix}cerca.html" title="Cerca">🔍</a>
    <span class="a11y" role="group" aria-label="Ajustos de lectura">
      <button id="fmenys" title="Lletra més petita" aria-label="Lletra més petita">A−</button>
      <button id="fmes" title="Lletra més gran" aria-label="Lletra més gran">A+</button>
      <button id="espaiat" title="Lectura fàcil: més espai" aria-label="Lectura fàcil" aria-pressed="false">Aa↔</button>
      <button id="llegir" title="Escolta la pàgina" aria-label="Escolta la pàgina">🔊</button>
      <button id="theme" title="Canvia el tema" aria-label="Canvia el tema">🌗</button>
    </span>
  </nav>
</header>
<div class="crumb">{crumb_html}</div>
<main class="content" id="contingut" tabindex="-1">
{body}
</main>
<footer class="site-footer">
  <p>«Repara i Roda 360» · optativa de 4t d'ESO · curs 2026-2027 · material sota
  <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.ca">CC BY-SA 4.0</a></p>
</footer>
<script>
const R=document.documentElement, LS=localStorage;
const el=id=>document.getElementById(id);
if(LS.getItem('theme'))R.dataset.theme=LS.getItem('theme');
el('theme').onclick=()=>{{R.dataset.theme=(R.dataset.theme==='dark')?'light':'dark';
LS.setItem('theme',R.dataset.theme);}};
let fs=+(LS.getItem('fs')||0);
const aplicaFs=()=>{{R.dataset.fs=fs;LS.setItem('fs',fs);}};aplicaFs();
el('fmes').onclick=()=>{{fs=Math.min(2,fs+1);aplicaFs();}};
el('fmenys').onclick=()=>{{fs=Math.max(0,fs-1);aplicaFs();}};
const esp=el('espaiat');
const aplicaEsp=v=>{{if(v)R.dataset.espaiat='1';else delete R.dataset.espaiat;
esp.setAttribute('aria-pressed',v?'true':'false');LS.setItem('espaiat',v?'1':'0');}};
aplicaEsp(LS.getItem('espaiat')==='1');
esp.onclick=()=>aplicaEsp(R.dataset.espaiat!=='1');
const veu=el('llegir');
if(!('speechSynthesis' in window))veu.style.display='none';
else veu.onclick=()=>{{const s=speechSynthesis;
if(s.speaking){{s.cancel();veu.textContent='🔊';return;}}
const u=new SpeechSynthesisUtterance(document.querySelector('main').innerText);
u.lang='ca-ES';const v=s.getVoices().find(v=>v.lang&&v.lang.toLowerCase().startsWith('ca'));
if(v)u.voice=v;u.rate=.95;u.onend=()=>veu.textContent='🔊';
veu.textContent='⏹';s.speak(u);}};
</script>
</body>
</html>
"""


SEARCH_INDEX = []


def sa_idx(folder):
    for i, c in enumerate(SA_CARDS):
        if c[4] == folder:
            return i
    return None


def sa_siblings(folder):
    order = {"fitxa": 0, "doc": 1, "rubrica": 2, "extra": 5}
    out = []
    for p in MD_FILES:
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if not rel.startswith(f"Classes/{folder}/"):
            continue
        fn = rel.rsplit("/", 1)[-1]
        base = PATH_MAP[rel].rsplit("/", 1)[-1]
        if fn.startswith("Fitxa"):
            lbl, kind = "✏️ Fitxa de l'alumnat", "fitxa"
        elif re.match(r"SA\d", fn):
            lbl, kind = "📖 La SA (docent)", "doc"
        elif fn.startswith("Rubrica"):
            lbl, kind = "📊 Rúbrica", "rubrica"
        elif fn.startswith("Material_gimcana"):
            lbl, kind = "🛡️ Gimcana d'eines i seguretat", "extra"
        elif fn.startswith("Vocabulari"):
            lbl, kind = "📖 Vocabulari bàsic", "extra"
        else:
            lbl, kind = "📄 " + fn[:-3].replace("_", " "), "extra"
        out.append((order[kind], lbl, base, kind))
    out.sort()
    return [(lbl, base, kind) for _o, lbl, base, kind in out]


def sa_cards(prefix):
    return "\n".join(
        f'<a class="card sa" href="{prefix}classes/{slugify(folder)}/index.html">'
        f'<div class="card-icon">{product.split()[0]}</div>'
        f'<div><h3>{code} · {html.escape(name)} <span class="badge">{trim}</span></h3>'
        f'<p>{html.escape(product.split(" ", 1)[1])}</p></div></a>'
        for code, name, trim, product, folder in SA_CARDS)


def sa_context_bar(folder, current_base):
    chips = ['<a class="sa-hublink" href="index.html">⌂ Aquesta SA</a>']
    for lbl, base, _kind in sa_siblings(folder):
        if base == current_base:
            chips.append(f'<span class="sa-chip cur">{lbl}</span>')
        else:
            chips.append(f'<a class="sa-chip" href="{base}">{lbl}</a>')
    return f'<div class="sa-sib">{"".join(chips)}</div>'


def build_sa_hubs():
    for code, name, trim, product, folder in SA_CARDS:
        slug = slugify(folder)
        out_rel = f"classes/{slug}/index.html"
        sibs = sa_siblings(folder)
        fitxa = next((b for lbl, b, k in sibs if k == "fitxa"), None)
        primary = ""
        if fitxa:
            primary = (f'<a class="sa-primary" href="{fitxa}"><span class="sa-primary-ic">✏️</span>'
                       f'<span><strong>Fitxa de l\'alumnat</strong>'
                       f'<small>el full amb què treballes aquesta SA</small></span></a>')
        others = [(lbl, b, k) for lbl, b, k in sibs if k != "fitxa"]
        cards = "\n".join(
            f'<a class="card" href="{b}"><div class="card-icon">{lbl.split(" ", 1)[0]}</div>'
            f'<div><h3>{html.escape(lbl.split(" ", 1)[1])}</h3></div></a>'
            for lbl, b, k in others)
        body = f"""
<h1>{code} · {html.escape(name)} <span class="badge">{trim}</span></h1>
<p class="product">{html.escape(product)}</p>
{primary}
<h2>Tot el material d'aquesta SA</h2>
<div class="grid">{cards}</div>
"""
        crumb = [("Inici", "index.html"), ("Classes", "classes/index.html"),
                 (f"{code} · {name}", None)]
        (OUT / out_rel).parent.mkdir(parents=True, exist_ok=True)
        (OUT / out_rel).write_text(
            render_page(f"{code} · {name}", body, out_rel, crumb), encoding="utf-8")


def build_doc_pages():
    pages = {}
    for p in MD_FILES:
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        out_rel = PATH_MAP[rel]
        text = p.read_text(encoding="utf-8")
        title = page_title(text, p.stem.replace("_", " "))
        MD.reset()
        body = MD.convert(text)
        current_dir = rel.rsplit("/", 1)[0] if "/" in rel else ""
        body = rewrite_links(body, out_rel, current_dir)
        body = checkboxify(body)
        plain_src = body
        parts = rel.split("/")
        if len(parts) >= 3 and parts[0] == "Classes" and sa_idx(parts[1]) is not None:
            foot = sa_context_bar(parts[1], out_rel.rsplit("/", 1)[-1])
            body = f'<article class="doc">{body}<footer class="sa-foot">{foot}</footer></article>'
        else:
            body = f'<article class="doc">{body}</article>'
        crumb = [("Inici", "index.html")]
        if "/" in rel:
            section = rel.split("/")[0]
            crumb.append((section, slugify(section) + "/index.html"))
            if rel.count("/") > 1:
                crumb.append((rel.split("/")[1].replace("_", " "), None))
        crumb.append((title if len(title) < 60 else title[:57] + "…", None))
        out = OUT / out_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_page(title, body, out_rel, crumb), encoding="utf-8")
        pages[rel] = (title, out_rel)
        plain = re.sub(r"<[^>]+>", " ", plain_src)
        plain = re.sub(r"\s+", " ", html.unescape(plain)).strip()
        SEARCH_INDEX.append({"t": title, "u": out_rel,
                             "s": rel.split("/")[0] if "/" in rel else "Inici",
                             "x": plain[:4000]})
    return pages


def card(href, icon, title, desc, badge=""):
    b = f'<span class="badge">{badge}</span>' if badge else ""
    return (f'<a class="card" href="{href}"><div class="card-icon">{icon}</div>'
            f'<div><h3>{html.escape(title)} {b}</h3><p>{html.escape(desc)}</p></div></a>')


def build_section_indexes(pages):
    for section in SECTIONS:
        entries = [(rel, t) for rel, (t, _o) in pages.items()
                   if rel.startswith(section + "/")]
        out_rel = slugify(section) + "/index.html"
        icon = SECTION_ICONS.get(section, "📄")
        if section == "Classes":
            body_html = (f"<h1>{icon} El curs, SA a SA</h1>"
                         f"<p class=\"lead\">Clica una SA per obrir-la: hi trobaràs la fitxa de "
                         f"l'alumnat, el material del docent i la rúbrica.</p>"
                         f"<div class='grid'>{sa_cards('../')}</div>")
        else:
            if not entries:
                continue
            items = "\n".join(
                f'<a class="card" href="../{pages[rel][1]}"><div class="card-icon">{icon}</div>'
                f'<div><h3>{html.escape(t)}</h3><p>{html.escape(rel.rsplit("/", 1)[-1])}</p></div></a>'
                for rel, t in entries)
            body_html = f"<h1>{icon} {html.escape(section)}</h1>\n<div class='grid'>{items}</div>"
        (OUT / out_rel).parent.mkdir(parents=True, exist_ok=True)
        (OUT / out_rel).write_text(
            render_page(section, body_html, out_rel,
                        [("Inici", "index.html"), (section, None)]), encoding="utf-8")


def build_home(pages):
    body = f"""
<section class="hero">
  <h1>🚲 Repara i Roda 360</h1>
  <p class="tagline">Optativa de 4t d'ESO · <strong>reparar bicicletes de veritat</strong> i
  fabricar-ne les peces amb làser i impressió 3D. Les bicis reparades es donen a la comunitat.</p>
  <div class="hero-actions">
    <a class="btn btn-primary" href="sa.html">🧩 Les SA</a>
    <a class="btn" href="docent.html">👩‍🏫 Soc docent</a>
    <a class="btn" href="alumnat.html">🧑‍🎓 Soc alumne/a</a>
    <a class="btn" href="families.html">👨‍👩‍👧 Soc família</a>
  </div>
</section>
<section>
  <h2>El curs, SA a SA</h2>
  <div class="grid">{sa_cards("")}</div>
</section>
"""
    (OUT / "index.html").write_text(
        render_page("Inici", body, "index.html", [("Inici", None)]), encoding="utf-8")

    # Alumnat
    cards = "\n".join(card(PATH_MAP[rel], icon, t, d) for icon, t, rel, d in ALUMNAT_LINKS)
    fitxes = "\n".join(
        f'<a class="chip" href="classes/{slugify(folder)}/index.html">{code}</a>'
        for code, _n, _t, _p, folder in SA_CARDS)
    body = f"""
<h1>🧑‍🎓 Per a l'alumnat</h1>
<p class="lead">Tot el que fas servir tu: les fitxes de cada SA, com t'avaluaran i els carnets.</p>
<blockquote><p>💡 <strong>Fes-te la web teva</strong> amb els botons de dalt: <strong>A−/A+</strong>
per la mida de la lletra, <strong>Aa↔</strong> per llegir amb més espai, <strong>🔊</strong> perquè
es llegeixi sola i <strong>🌗</strong> pel mode fosc.</p></blockquote>
<h2>✏️ Les fitxes de cada SA</h2>
<div class="chips">{fitxes}</div>
<h2>Els teus documents</h2>
<div class="grid">{cards}</div>
"""
    (OUT / "alumnat.html").write_text(
        render_page("Alumnat", body, "alumnat.html",
                    [("Inici", "index.html"), ("Alumnat", None)]), encoding="utf-8")

    # Docent
    dest = "\n".join(card(PATH_MAP[rel], icon, t, d) for icon, t, rel, d in DOCENT_DESTACATS)
    impresos = card("impressos/Full_valoracio_diaria.pdf", "🖨️",
                    "Full de valoració diària (PDF)",
                    "A4 apaïsat per avaluar cada dia el taller i l'aula maker", "imprimible")
    sections = "\n".join(
        card(slugify(s) + "/index.html", SECTION_ICONS[s], s, SECTION_DESC[s])
        for s in SECTIONS)
    body = f"""
<h1>👩‍🏫 Per al professorat</h1>
<p class="lead">El material complet de l'optativa. Comença per la programació didàctica i tingues
a mà el full de valoració diària.</p>
<h2>Imprescindibles</h2>
<div class="grid">{dest}</div>
<h2>🖨️ Per imprimir</h2>
<div class="grid">{impresos}</div>
<h2>Tot el material, per carpetes</h2>
<div class="grid">{sections}</div>
"""
    (OUT / "docent.html").write_text(
        render_page("Docent", body, "docent.html",
                    [("Inici", "index.html"), ("Docent", None)]), encoding="utf-8")

    # SA (accés directe = còpia de l'índex de Classes amb rutes ajustades)
    shutil.copyfile(OUT / "classes/index.html", OUT / "sa.html")
    sa_html = (OUT / "sa.html").read_text(encoding="utf-8")
    sa_html = sa_html.replace('href="../', 'href="').replace('src="../', 'src="')
    (OUT / "sa.html").write_text(sa_html, encoding="utf-8")

    # Famílies
    fam = "\n".join([
        card(PATH_MAP["Normativa/Carta_families_inici_curs.md"], "✉️",
             "Carta d'inici de curs", "Què farà el vostre fill/a a l'optativa"),
        card(PATH_MAP["Normativa/Autoritzacio_families_sortides.md"], "📝",
             "Autorització de les sortides en bici", "El document que us demanarem signat (3r trim.)"),
        card(PATH_MAP["Normativa/Autoritzacio_families_VR_360.md"], "🥽",
             "Autorització VR i drets d'imatge", "Per a l'ús de les ulleres i la càmera 360"),
        card(PATH_MAP["Normativa/Protocol_us_VR.md"], "🔎",
             "Protocol d'ús de la realitat virtual", "Salut, temps d'ús i seguretat"),
        card(PATH_MAP["Normativa/Normes_seguretat_taller.md"], "🛡️",
             "Normes de seguretat del taller", "Com treballem al taller i a l'aula maker"),
    ])
    body = f"""
<h1>👨‍👩‍👧 Per a les famílies</h1>
<p class="lead">A Repara i Roda 360 el vostre fill/a <strong>repara bicicletes reals</strong> i
les fabrica peces amb làser i impressió 3D. Les bicis es donen a la comunitat. Aquí teniu els
documents que us afecten.</p>
<div class="grid">{fam}</div>
<blockquote><p>🏅 A final de curs hi ha una <strong>exposició pública</strong> amb estació de
realitat virtual i el lliurament dels <strong>certificats de Mecànic/a Júnior</strong>. Us hi
esperem!</p></blockquote>
"""
    (OUT / "families.html").write_text(
        render_page("Famílies", body, "families.html",
                    [("Inici", "index.html"), ("Famílies", None)]), encoding="utf-8")

    # Cerca
    (OUT / "assets" / "cerca-index.json").write_text(
        json.dumps(SEARCH_INDEX, ensure_ascii=False), encoding="utf-8")
    body = """
<h1>🔍 Cerca al material</h1>
<p class="lead">Cerca per paraula: «M-check», «punxada», «carnet», «rúbrica SA4»…</p>
<p><input id="q" type="search" placeholder="Escriu i prem Enter…" autofocus
   style="width:100%;padding:.8rem 1.2rem;font-size:1.1rem;border-radius:999px;
          border:2px solid var(--line);background:var(--bg-card);color:var(--ink)"></p>
<div id="res"></div>
<script>
let IDX=null;
const q=document.getElementById('q'), res=document.getElementById('res');
async function cerca(){
  if(!IDX) IDX=await (await fetch('assets/cerca-index.json')).json();
  const terms=q.value.toLowerCase().split(/\\s+/).filter(t=>t.length>1);
  if(!terms.length){res.innerHTML='';return;}
  const out=[];
  for(const p of IDX){
    const hay=(p.t+' '+p.x).toLowerCase();
    let score=0, ok=true;
    for(const t of terms){
      const n=hay.split(t).length-1;
      if(!n){ok=false;break;}
      score+=n+(p.t.toLowerCase().includes(t)?8:0);
    }
    if(ok) out.push([score,p,terms[0]]);
  }
  out.sort((a,b)=>b[0]-a[0]);
  res.innerHTML=out.slice(0,25).map(([s,p,t])=>{
    const i=p.x.toLowerCase().indexOf(t);
    const frag=i<0?p.x.slice(0,160):p.x.slice(Math.max(0,i-70),i+110);
    return `<a class="card" href="${p.u}"><div class="card-icon">📄</div>
      <div><h3>${p.t} <span class="badge">${p.s}</span></h3><p>…${frag}…</p></div></a>`;
  }).join('')||'<p>Cap resultat. Prova una paraula més curta o sense accents.</p>';
}
q.addEventListener('input',()=>{clearTimeout(q._d);q._d=setTimeout(cerca,250);});
</script>
"""
    (OUT / "cerca.html").write_text(
        render_page("Cerca", body, "cerca.html",
                    [("Inici", "index.html"), ("Cerca", None)]), encoding="utf-8")


def copy_assets():
    imatges = ROOT / "Recursos"
    dest = OUT / "recursos"
    for f in imatges.glob("*"):
        if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"):
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(f, dest / slugify(f.name))
    pdf = ROOT / "Avaluació" / "Full_valoracio_diaria.pdf"
    if pdf.exists():
        (OUT / "impressos").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pdf, OUT / "impressos" / pdf.name)
    if (ROOT / "LICENSE").exists():
        shutil.copyfile(ROOT / "LICENSE", OUT / "LICENSE")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    shutil.copyfile(ROOT / "web_assets" / "style.css", OUT / "assets" / "style.css")
    pages = build_doc_pages()
    build_sa_hubs()
    build_section_indexes(pages)
    build_home(pages)
    copy_assets()
    print(f"Web generada a {OUT} — {len(pages)} pàgines de contingut.")


if __name__ == "__main__":
    main()
