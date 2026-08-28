# -*- coding: utf-8 -*-
"""Genera mappa.html: mappa concettuale navigabile del libro."""
import glob, re, json, html, os
import schemi

PARTI = [
    ("Fondamenti",       1,  3,  "p1"),
    ("Metodologie, strumenti ed esperienze", 4, 15, "p2"),
    ("Pratiche innovative", 16, 29, "p3"),
    ("Casi ed esperienze",  30, 39, "p4"),
]

def parte_di(n):
    for nome, a, b, cls in PARTI:
        if a <= n <= b:
            return nome, cls
    return "", "p1"

def sezione(md, titolo):
    m = re.search(rf"^## {re.escape(titolo)}\s*\n(.*?)(?=^## |\Z)", md, re.S | re.M)
    return m.group(1).strip() if m else ""

def bullets(txt, limite=None):
    out = []
    for ln in txt.split("\n"):
        s = ln.strip()
        if s.startswith("- "):
            out.append(s[2:])
    return out[:limite] if limite else out

def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = s.replace("&lt;br&gt;", "<br>")
    return s

def nl(s):
    return inline(s).replace("\n", "<br>")

# ------------------------------------------------------------- schemi in HTML
def h_flow(s):
    p = [f'<ol class="dg-flow">']
    for st in s["steps"]:
        p.append('<li><span class="dg-lbl">' + inline(st["label"]) + '</span>' +
                 (f'<span class="dg-det">{nl(st["detail"])}</span>' if st.get("detail") else "") +
                 '</li>')
    p.append("</ol>")
    return "".join(p)

def h_cycle(s):
    nodes = s["nodes"] if "nodes" in s else [
        st["label"] + ("\n" + st["detail"] if st.get("detail") else "") for st in s["steps"]]
    p = ['<ol class="dg-flow dg-cycle">']
    for nd in nodes:
        parts = nd.split("\n")
        p.append('<li><span class="dg-lbl">' + inline(parts[0]) + '</span>' +
                 (f'<span class="dg-det">{nl(chr(10).join(parts[1:]))}</span>' if len(parts) > 1 else "") +
                 '</li>')
    p.append('</ol><p class="dg-loop">↻ il ciclo si richiude sul primo passo</p>')
    return "".join(p)

def h_hier(s):
    p = [f'<div class="dg-hier"><div class="dg-root">{inline(s.get("root",""))}</div>',
         '<div class="dg-branches">']
    for b in s["branches"]:
        p.append('<div class="dg-branch"><h5>' + nl(b["label"]) + "</h5><ul>")
        for c in b.get("children", []):
            p.append("<li>" + inline(c) + "</li>")
        p.append("</ul></div>")
    p.append("</div></div>")
    return "".join(p)

def h_grid(s):
    """Matrice a griglia righe x colonne."""
    p = ['<div class="dg-scroll"><table class="dg-tab dg-grid"><thead><tr><th></th>']
    for c in s["cols"]:
        p.append(f"<th>{inline(c)}</th>")
    p.append("</tr></thead><tbody>")
    for i, r in enumerate(s["rows"]):
        p.append(f"<tr><th>{inline(r)}</th>")
        for v in (s["cells"][i] if i < len(s["cells"]) else []):
            p.append(f"<td>{inline(str(v))}</td>")
        p.append("</tr>")
    p.append("</tbody></table></div>")
    return "".join(p)

def h_matrix(s):
    if "quadrants" not in s:
        return h_grid(s)
    q = {d["pos"]: d for d in s["quadrants"]}
    xa = s.get("xaxis", ["", ""]); ya = s.get("yaxis", ["", ""])
    def cell(pos):
        d = q.get(pos)
        if not d: return '<div class="dg-q dg-q-empty"></div>'
        return ('<div class="dg-q"><span class="dg-lbl">' + inline(d["label"]) + "</span>" +
                (f'<span class="dg-det">{nl(d.get("detail",""))}</span>' if d.get("detail") else "") +
                "</div>")
    return ('<div class="dg-matrix">'
            f'<div class="dg-yhi">{inline(ya[1])}</div>{cell("tl")}{cell("tr")}'
            f'<div class="dg-ylo">{inline(ya[0])}</div>{cell("bl")}{cell("br")}'
            f'<div></div><div class="dg-x">{inline(xa[0])}</div><div class="dg-x">{inline(xa[1])}</div>'
            "</div>")

def h_pyramid(s):
    lv = [(t, None) if isinstance(t, str) else (t["label"], t.get("detail"))
          for t in s["levels"]]
    n = len(lv)
    p = ['<div class="dg-pyr">']
    for k, (lab, det) in enumerate(lv):
        w = 46 + 54 * (k + 1) / n
        p.append(f'<div class="dg-lv" style="width:{w:.0f}%"><span class="dg-lbl">'
                 + inline(lab) + "</span>"
                 + (f'<span class="dg-det">{nl(det)}</span>' if det else "") + "</div>")
    p.append("</div>")
    return "".join(p)

def h_poles(s):
    """Trade-off a due colonne contrapposte."""
    p = ['<div class="dg-poles">']
    for d in (s["left"], s["right"]):
        p.append('<div class="dg-pol"><h5>' + inline(d["label"]) + "</h5><ul>")
        for pt in d["points"]:
            p.append("<li>" + inline(pt) + "</li>")
        p.append("</ul></div>")
    p.append("</div>")
    return "".join(p)

def h_tradeoff(s):
    if "axes" not in s:
        return h_poles(s)
    p = ['<div class="dg-trade">']
    for lab, a, b in s["axes"]:
        p.append(f'<div class="dg-ax"><span class="dg-axl">{inline(lab)}</span>'
                 f'<span class="dg-pole">{inline(a)}</span>'
                 f'<span class="dg-bar" aria-hidden="true"></span>'
                 f'<span class="dg-pole dg-pole-b">{inline(b)}</span></div>')
    p.append("</div>")
    return "".join(p)

def _rows(s):
    """Normalizza le righe di un confronto: liste oppure {label, cells}."""
    out = []
    for r in s["rows"]:
        out.append(r if isinstance(r, list) else [r["label"]] + list(r["cells"]))
    return out

def h_compare(s):
    cols, rows = s["columns"], _rows(s)
    ncol = len(rows[0])
    head = cols if len(cols) == ncol else [""] + cols
    p = ['<div class="dg-scroll"><table class="dg-tab"><thead><tr>']
    for h in head:
        p.append(f"<th>{inline(h)}</th>")
    p.append("</tr></thead><tbody>")
    for r in rows:
        p.append("<tr>")
        for i, v in enumerate(r):
            tag = "th" if (i == 0 and len(cols) != ncol) else "td"
            p.append(f"<{tag}>{inline(str(v))}</{tag}>")
        p.append("</tr>")
    p.append("</tbody></table></div>")
    return "".join(p)

H = {"flow": h_flow, "cycle": h_cycle, "hierarchy": h_hier, "matrix": h_matrix,
     "pyramid": h_pyramid, "tradeoff": h_tradeoff, "compare": h_compare}

def rendi(s):
    fn = H.get(s["type"])
    body = fn(s) if fn else ""
    nota = f'<p class="dg-note">{inline(s["note"])}</p>' if s.get("note") else ""
    return (f'<figure class="dg" data-type="{s["type"]}">'
            f'<figcaption>{inline(s["title"])}</figcaption>{body}{nota}</figure>')

# ------------------------------------------------------------- raccolta dati
def raccogli():
    caps = []
    for f in sorted(glob.glob("riassunti/cap*.md")):
        n = int(re.search(r"cap(\d+)", f).group(1))
        md = open(f).read()
        righe = md.split("\n")
        titolo = righe[0].lstrip("# ").strip()
        tit = re.sub(r"^Capitolo \d+\s*—\s*", "", titolo)
        meta = next((l for l in righe[1:6] if re.match(r"\*\*Aut[a-z]+", l)), "")
        autore = ""
        m = re.search(r"\*\*Aut[a-z]+:\*\*\s*([^·]+)", meta)
        if m: autore = m.group(1).strip()
        m = re.search(r"\*\*In una frase:\*\*\s*(.+)", md)
        frase = m.group(1).strip() if m else ""
        concetti = bullets(sezione(md, "Concetti chiave"))
        punti = bullets(sezione(md, "Punti da ricordare"))
        caps.append(dict(n=n, titolo=tit, autore=autore, frase=frase,
                         concetti=concetti, punti=punti,
                         schemi=schemi.parse_schemi(md)))
    return caps

def termine(c):
    """Estrae il termine in grassetto a inizio bullet, per il glossario."""
    m = re.match(r"\*\*(.+?)\*\*\s*—\s*(.*)", c)
    if m: return m.group(1), m.group(2)
    m = re.match(r"\*\*(.+?)\*\*(.*)", c)
    if m: return m.group(1), m.group(2).lstrip(" —-")
    return None, c

# ------------------------------------------------------------- pagina
CSS = """
:root{
  --ground:#f2f5f7; --surface:#ffffff; --surface-2:#f8fafb;
  --ink:#16202b; --ink-2:#40525f; --ink-3:#6c7f8d;
  --rule:#dde5ea; --rule-2:#eef3f6;
  --p1:#1f5673; --p1-bg:#e7eff4; --p2:#3d6b52; --p2-bg:#e7f0ea;
  --p3:#8a5a2b; --p3-bg:#f6eee4; --p4:#5c4470; --p4-bg:#efe9f3;
  --accent:var(--p1);
  --shadow:0 1px 2px rgba(22,32,43,.05),0 6px 20px -12px rgba(22,32,43,.18);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#11181f; --surface:#18212a; --surface-2:#1d2731;
    --ink:#e7edf1; --ink-2:#aebcc7; --ink-3:#8496a3;
    --rule:#2a3742; --rule-2:#222d37;
    --p1:#7fb3d0; --p1-bg:#1a2c38; --p2:#8dc0a2; --p2-bg:#1a2d24;
    --p3:#d5a878; --p3-bg:#31251a; --p4:#b79ccc; --p4-bg:#271f30;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 20px -12px rgba(0,0,0,.6);
  }
}
:root[data-theme="dark"]{
  --ground:#11181f; --surface:#18212a; --surface-2:#1d2731;
  --ink:#e7edf1; --ink-2:#aebcc7; --ink-3:#8496a3;
  --rule:#2a3742; --rule-2:#222d37;
  --p1:#7fb3d0; --p1-bg:#1a2c38; --p2:#8dc0a2; --p2-bg:#1a2d24;
  --p3:#d5a878; --p3-bg:#31251a; --p4:#b79ccc; --p4-bg:#271f30;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 20px -12px rgba(0,0,0,.6);
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:"Source Sans 3",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  font-size:16px; line-height:1.55; -webkit-font-smoothing:antialiased;
}
h1,h2,h3,h4,h5{font-family:Newsreader,Georgia,"Times New Roman",serif; text-wrap:balance; margin:0}
code,.mono,.num{font-family:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace}
a{color:var(--accent)}
.wrap{max-width:1240px;margin:0 auto;padding:0 24px}

/* ---- testata ---- */
header.top{border-bottom:1px solid var(--rule); background:var(--surface)}
.top .wrap{display:flex;flex-wrap:wrap;gap:20px;align-items:flex-end;
  justify-content:space-between;padding-top:34px;padding-bottom:24px}
.brand h1{font-size:clamp(28px,4.2vw,44px);font-weight:500;letter-spacing:-.015em;line-height:1.08}
.brand .eyebrow{font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-3);margin-bottom:8px;font-weight:600}
.brand p{margin:8px 0 0;color:var(--ink-2);font-size:14.5px;max-width:56ch}
.tools{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
input[type=search]{
  font:inherit;font-size:14px;padding:9px 13px;border:1px solid var(--rule);
  border-radius:8px;background:var(--surface-2);color:var(--ink);min-width:230px}
input[type=search]:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.btn{font:inherit;font-size:13.5px;padding:9px 13px;border:1px solid var(--rule);
  border-radius:8px;background:var(--surface-2);color:var(--ink-2);cursor:pointer}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn:focus-visible{outline:2px solid var(--accent);outline-offset:1px}

/* ---- mappa d'insieme ---- */
.overview{padding:32px 0 8px}
.overview h2{font-size:13px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-3);font-family:"Source Sans 3",sans-serif;font-weight:700;margin-bottom:16px}
.parts{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}
.part{background:var(--surface);border:1px solid var(--rule);border-radius:12px;
  padding:16px 16px 14px;border-top:3px solid var(--pc);box-shadow:var(--shadow)}
.part h3{font-size:17px;font-weight:600;color:var(--pc);margin-bottom:2px}
.part .rng{font-size:11.5px;color:var(--ink-3);letter-spacing:.04em;margin-bottom:12px}
.chips{display:flex;flex-wrap:wrap;gap:5px}
.chip{display:inline-flex;align-items:center;justify-content:center;min-width:30px;height:28px;
  padding:0 7px;border-radius:7px;background:var(--pcbg);color:var(--pc);
  font-family:"IBM Plex Mono",monospace;font-size:12.5px;font-weight:500;
  text-decoration:none;border:1px solid transparent;transition:transform .12s}
.chip:hover,.chip:focus-visible{border-color:var(--pc);transform:translateY(-1px);outline:none}
.chip[aria-disabled="true"]{opacity:.34;pointer-events:none}

/* ---- corpo ---- */
.body{display:grid;grid-template-columns:238px 1fr;gap:36px;padding:34px 0 80px;align-items:start}
nav.idx{position:sticky;top:18px;max-height:calc(100vh - 36px);overflow:auto;
  font-size:13.5px;padding-right:6px}
nav.idx .grp{margin-bottom:18px}
nav.idx .grp>span{display:block;font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--pc);font-weight:700;margin-bottom:7px}
nav.idx a{display:grid;grid-template-columns:26px 1fr;gap:6px;padding:4px 6px;border-radius:6px;
  color:var(--ink-2);text-decoration:none;line-height:1.32}
nav.idx a:hover{background:var(--surface);color:var(--ink)}
nav.idx a.on{background:var(--pcbg);color:var(--pc);font-weight:600}
nav.idx .n{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--ink-3);text-align:right}

main{min-width:0;display:flex;flex-direction:column;gap:22px}
.cap{background:var(--surface);border:1px solid var(--rule);border-radius:14px;
  box-shadow:var(--shadow);overflow:hidden;scroll-margin-top:18px}
.cap>header{padding:20px 26px 18px;border-bottom:1px solid var(--rule-2);
  border-left:4px solid var(--pc);display:flex;gap:18px;align-items:baseline;flex-wrap:wrap}
.cap .num{font-family:"IBM Plex Mono",monospace;font-size:26px;font-weight:500;
  color:var(--pc);line-height:1;font-variant-numeric:tabular-nums}
.cap h3{font-size:21px;font-weight:500;letter-spacing:-.01em;flex:1 1 320px}
.cap .aut{font-size:12.5px;color:var(--ink-3)}
.cap .inner{padding:20px 26px 24px;display:flex;flex-direction:column;gap:20px}
.frase{font-family:Newsreader,Georgia,serif;font-size:17.5px;line-height:1.5;
  color:var(--ink);border-left:3px solid var(--pc);padding-left:16px;margin:0;font-style:italic}
.sect>h4{font-size:11px;letter-spacing:.13em;text-transform:uppercase;color:var(--ink-3);
  font-family:"Source Sans 3",sans-serif;font-weight:700;margin-bottom:10px}
.gloss{list-style:none;margin:0;padding:0;display:grid;gap:7px}
.gloss li{font-size:14.3px;color:var(--ink-2);padding-left:14px;position:relative;line-height:1.48}
.gloss li::before{content:"";position:absolute;left:0;top:.62em;width:5px;height:5px;
  border-radius:50%;background:var(--pc);opacity:.55}
.gloss strong{color:var(--ink)}
.ric{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.ric li{font-size:14.3px;color:var(--ink-2);background:var(--surface-2);
  border:1px solid var(--rule-2);border-radius:8px;padding:9px 12px;line-height:1.45}
.ric strong{color:var(--ink)}

/* ---- schemi ---- */
.dg{margin:0;border:1px solid var(--rule);border-radius:11px;padding:16px 16px 14px;
  background:var(--surface-2)}
.dg+.dg{margin-top:14px}
.dg>figcaption{font-size:13px;font-weight:700;color:var(--pc);margin-bottom:14px;
  letter-spacing:.005em;font-family:"Source Sans 3",sans-serif}
.dg-note{font-size:12.4px;color:var(--ink-3);font-style:italic;margin:12px 0 0;line-height:1.45}
.dg-lbl{display:block;font-weight:650;font-size:13.6px;color:var(--ink);line-height:1.32}
.dg-det{display:block;font-size:12.3px;color:var(--ink-2);margin-top:4px;line-height:1.4}

.dg-flow{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:0}
.dg-flow li{background:var(--surface);border:1px solid var(--rule);border-radius:9px;
  padding:11px 14px;position:relative}
.dg-flow li+li{margin-top:20px}
.dg-flow li+li::before{content:"";position:absolute;left:50%;top:-16px;width:1.5px;height:12px;
  background:var(--pc);opacity:.5}
.dg-flow li+li::after{content:"";position:absolute;left:50%;top:-6px;transform:translateX(-50%);
  border:4.5px solid transparent;border-top-color:var(--pc);opacity:.5}
.dg-loop{font-size:12.4px;color:var(--pc);margin:10px 0 0;text-align:center;font-weight:600}

.dg-hier .dg-root{background:var(--pcbg);color:var(--pc);border:1px solid var(--pc);
  border-radius:9px;padding:9px 14px;font-weight:700;font-size:13.6px;text-align:center;
  margin-bottom:16px}
.dg-branches{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}
.dg-branch{background:var(--surface);border:1px solid var(--rule);border-radius:9px;padding:11px 13px}
.dg-branch h5{font-size:13.2px;font-weight:700;color:var(--ink);margin-bottom:8px;
  font-family:"Source Sans 3",sans-serif;line-height:1.3}
.dg-branch ul{list-style:none;margin:0;padding:0;display:grid;gap:5px}
.dg-branch li{font-size:12.5px;color:var(--ink-2);padding-left:12px;position:relative;line-height:1.4}
.dg-branch li::before{content:"–";position:absolute;left:0;color:var(--pc);opacity:.6}

.dg-matrix{display:grid;grid-template-columns:auto 1fr 1fr;gap:8px;align-items:stretch}
.dg-q{background:var(--surface);border:1px solid var(--rule);border-radius:9px;padding:12px 13px}
.dg-q-empty{background:transparent;border-style:dashed}
.dg-yhi,.dg-ylo{writing-mode:vertical-rl;transform:rotate(180deg);font-size:11.5px;
  color:var(--ink-3);text-align:center;padding:4px 0;font-weight:600;letter-spacing:.03em}
.dg-x{font-size:11.5px;color:var(--ink-3);text-align:center;padding-top:4px;font-weight:600;
  letter-spacing:.03em}

.dg-pyr{display:flex;flex-direction:column;align-items:center;gap:7px}
.dg-lv{background:var(--surface);border:1px solid var(--rule);border-radius:8px;
  padding:10px 14px;text-align:center;font-size:13.2px;font-weight:600;color:var(--ink);line-height:1.35}

.dg-lv .dg-lbl{display:block}
.dg-lv .dg-det{display:block;margin-top:4px;font-weight:400;font-size:12.2px;
  color:var(--ink-2);line-height:1.45}

.dg-poles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}
.dg-pol{background:var(--surface);border:1px solid var(--rule);border-radius:10px;padding:13px 15px}
.dg-pol h5{margin:0 0 9px;font-size:12.6px;font-weight:700;color:var(--pc);
  letter-spacing:.03em;text-transform:uppercase}
.dg-pol ul{margin:0;padding-left:17px}
.dg-pol li{font-size:13px;line-height:1.5;color:var(--ink-2);margin:0 0 5px}

.dg-grid td{vertical-align:top}

.dg-trade{display:grid;gap:9px}
.dg-ax{display:grid;grid-template-columns:minmax(120px,1.1fr) minmax(90px,1fr) 34px minmax(90px,1fr);
  gap:10px;align-items:center}
.dg-axl{font-size:12.6px;font-weight:650;color:var(--ink);line-height:1.3}
.dg-pole{font-size:12.3px;color:var(--ink-2);text-align:right}
.dg-pole-b{text-align:left}
.dg-bar{height:1.5px;background:var(--pc);opacity:.45;border-radius:2px;position:relative}
.dg-bar::before,.dg-bar::after{content:"";position:absolute;top:50%;width:6px;height:6px;
  border-radius:50%;background:var(--pc);transform:translateY(-50%)}
.dg-bar::before{left:-3px}.dg-bar::after{right:-3px}

.dg-scroll{overflow-x:auto}
.dg-tab{border-collapse:collapse;width:100%;font-size:12.9px;min-width:480px}
.dg-tab th,.dg-tab td{border:1px solid var(--rule);padding:8px 11px;text-align:left;
  vertical-align:top;line-height:1.42}
.dg-tab thead th{background:var(--pcbg);color:var(--pc);font-weight:700;font-size:12.4px}
.dg-tab tbody th{background:var(--surface);font-weight:650;color:var(--ink);width:1%;white-space:nowrap}
.dg-tab td{background:var(--surface);color:var(--ink-2)}

.cap.hide{display:none}
.empty{color:var(--ink-3);font-size:14px;padding:30px 0}
footer{border-top:1px solid var(--rule);padding:24px 0 40px;color:var(--ink-3);font-size:12.8px}

@media (max-width:900px){
  .body{grid-template-columns:1fr;gap:0}
  nav.idx{position:static;max-height:none;margin-bottom:26px;
    columns:2;column-gap:22px}
  .dg-ax{grid-template-columns:1fr;gap:2px}
  .dg-pole,.dg-pole-b{text-align:left}
  .dg-bar{display:none}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
@media print{
  body{background:#fff}
  header.top,.tools,nav.idx,footer,.overview{display:none}
  .body{display:block;padding:0}
  .cap{break-inside:avoid;box-shadow:none;border-radius:0;border-left:3px solid #333;
    margin-bottom:18px}
  .dg{break-inside:avoid}
}
"""

JS = """
const q=document.getElementById('q'), caps=[...document.querySelectorAll('.cap')];
const links=[...document.querySelectorAll('nav.idx a')];
const chips=[...document.querySelectorAll('.chip')];
function filtra(){
  const t=q.value.trim().toLowerCase();
  let vis=0;
  caps.forEach(c=>{
    const ok = !t || c.dataset.k.includes(t);
    c.classList.toggle('hide',!ok); if(ok) vis++;
    const n=c.dataset.n;
    links.forEach(a=>{if(a.dataset.n===n)a.style.display=ok?'':'none'});
    chips.forEach(a=>{if(a.dataset.n===n)a.setAttribute('aria-disabled',ok?'false':'true')});
  });
  document.getElementById('vuoto').hidden = vis>0;
}
q.addEventListener('input',filtra);
const io=new IntersectionObserver(es=>{
  es.forEach(e=>{if(e.isIntersecting){
    links.forEach(a=>a.classList.toggle('on',a.dataset.n===e.target.dataset.n));}});
},{rootMargin:'-15% 0px -70% 0px'});
caps.forEach(c=>io.observe(c));
document.getElementById('tema').addEventListener('click',()=>{
  const r=document.documentElement;
  const dark=getComputedStyle(r).getPropertyValue('--ground').trim().startsWith('#1');
  r.setAttribute('data-theme',dark?'light':'dark');
});
"""

def pagina(caps, out="mappa.html"):
    have = {c["n"] for c in caps}
    # --- mappa d'insieme
    parts_html = []
    for nome, a, b, cls in PARTI:
        chips = []
        for n in range(a, b + 1):
            dis = "" if n in have else ' aria-disabled="true"'
            chips.append(f'<a class="chip" data-n="{n}" href="#c{n}"{dis}>{n}</a>')
        parts_html.append(
            f'<section class="part" style="--pc:var(--{cls});--pcbg:var(--{cls}-bg)">'
            f"<h3>{nome}</h3><p class=\"rng\">capitoli {a}–{b}</p>"
            f'<div class="chips">{"".join(chips)}</div></section>')

    # --- indice laterale
    idx = []
    for nome, a, b, cls in PARTI:
        gruppo = [c for c in caps if a <= c["n"] <= b]
        if not gruppo: continue
        righe = "".join(
            f'<a href="#c{c["n"]}" data-n="{c["n"]}"><span class="n">{c["n"]}</span>'
            f'<span>{html.escape(c["titolo"])}</span></a>' for c in gruppo)
        idx.append(f'<div class="grp" style="--pc:var(--{cls});--pcbg:var(--{cls}-bg)">'
                   f"<span>{nome}</span>{righe}</div>")

    # --- schede capitolo
    schede = []
    for c in caps:
        nome, cls = parte_di(c["n"])
        gloss = ""
        if c["concetti"]:
            li = []
            for x in c["concetti"]:
                t, d = termine(x)
                li.append("<li>" + (f"<strong>{inline(t)}</strong> — " if t else "") + inline(d) + "</li>")
            gloss = ('<div class="sect"><h4>Concetti chiave</h4>'
                     f'<ul class="gloss">{"".join(li)}</ul></div>')
        ric = ""
        if c["punti"]:
            ric = ('<div class="sect"><h4>Da ricordare</h4><ul class="ric">' +
                   "".join(f"<li>{inline(x)}</li>" for x in c["punti"]) + "</ul></div>")
        sch = ""
        if c["schemi"]:
            sch = ('<div class="sect"><h4>Schemi</h4>' +
                   "".join(rendi(s) for s in c["schemi"]) + "</div>")
        chiave = " ".join([c["titolo"], c["autore"], c["frase"], nome,
                           " ".join(c["concetti"]), " ".join(c["punti"]),
                           " ".join(s["title"] for s in c["schemi"])]).lower()
        chiave = re.sub(r"[*`]", "", chiave)
        schede.append(
            f'<article class="cap" id="c{c["n"]}" data-n="{c["n"]}" '
            f'data-k="{html.escape(chiave, quote=True)}" '
            f'style="--pc:var(--{cls});--pcbg:var(--{cls}-bg)">'
            f'<header><span class="num">{c["n"]:02d}</span><h3>{html.escape(c["titolo"])}</h3>'
            f'<span class="aut">{html.escape(c["autore"])}</span></header>'
            f'<div class="inner"><p class="frase">{inline(c["frase"])}</p>'
            f"{gloss}{ric}{sch}</div></article>")

    doc = f"""<title>Mappa del controllo di gestione</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Source+Sans+3:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
<header class="top"><div class="wrap">
  <div class="brand">
    <p class="eyebrow">Mappa concettuale · {len(caps)} capitoli su 39</p>
    <h1>Il controllo di gestione</h1>
    <p>Busco · Giovannoni · Riccaboni — V edizione, Wolters Kluwer.
       Gli schemi di sintesi del libro, capitolo per capitolo.</p>
  </div>
  <div class="tools">
    <input type="search" id="q" placeholder="Cerca concetto, autore, capitolo…" aria-label="Cerca">
    <button class="btn" id="tema">Tema</button>
    <button class="btn" onclick="window.print()">Stampa</button>
  </div>
</div></header>

<div class="wrap overview">
  <h2>Le quattro parti del libro</h2>
  <div class="parts">{"".join(parts_html)}</div>
</div>

<div class="wrap body">
  <nav class="idx" aria-label="Indice dei capitoli">{"".join(idx)}</nav>
  <main>{"".join(schede)}<p class="empty" id="vuoto" hidden>Nessun capitolo corrisponde alla ricerca.</p></main>
</div>

<footer class="wrap">Riassunto ragionato per lo studio. I numeri in grigio nella mappa
d'insieme sono capitoli non ancora elaborati.</footer>
<script>{JS}</script>
"""
    open(out, "w", encoding="utf-8").write(doc)
    salva_standalone(doc, "mappa-standalone.html")
    return out, len(caps), sum(len(c["schemi"]) for c in caps)

def salva_standalone(doc, out):
    """Versione apribile da disco: l'artifact aggiunge da sé doctype, head e reset."""
    pagina = ('<!doctype html>\n<html lang="it">\n<head>\n'
              '<meta charset="utf-8">\n' + doc.split("\n<style>", 1)[0] +
              '\n<style>*,*::before,*::after{box-sizing:border-box}'
              'body{margin:0}img{max-width:100%}</style>\n</head>\n<body>\n<style>' +
              doc.split("\n<style>", 1)[1] + "\n</body>\n</html>\n")
    open(out, "w", encoding="utf-8").write(pagina)

if __name__ == "__main__":
    print(pagina(raccogli()))
