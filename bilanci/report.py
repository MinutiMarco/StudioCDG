"""Report HTML del benchmark: una pagina autonoma, apribile da disco."""
import html, json
from datetime import date
from pathlib import Path

CSS = """
:root{--ink:#1c2733;--muted:#5b6b7c;--line:#c3ced9;--bg:#ffffff;--soft:#f4f7fa;--accent:#2c4a6b;
--pos:#2f7d55;--neg:#a5432f}
*{box-sizing:border-box}
body{margin:0;padding:2rem 1.25rem 4rem;background:var(--bg);color:var(--ink);
font:15px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
main{max-width:1100px;margin:0 auto}
h1{font-size:1.6rem;margin:0 0 .3rem}
h2{font-size:1.1rem;margin:2.2rem 0 .6rem;padding-bottom:.3rem;border-bottom:1px solid var(--line)}
.sub{color:var(--muted);margin:0 0 1.5rem}
.scheda{background:var(--soft);border:1px solid var(--line);border-radius:8px;padding:1rem 1.2rem}
.scheda dl{display:grid;grid-template-columns:auto 1fr;gap:.25rem 1rem;margin:0}
.scheda dt{color:var(--muted)}
.scheda dd{margin:0;font-weight:600}
.wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{padding:.45rem .55rem;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
th:first-child,td:first-child{text-align:left;white-space:normal}
thead th{background:var(--soft);color:var(--muted);font-weight:600;text-align:right}
thead th:first-child{text-align:left}
tbody tr:hover{background:var(--soft)}
.target{font-weight:700;color:var(--accent)}
.g-alto{color:var(--pos)}.g-basso{color:var(--neg)}
.nota{color:var(--muted);font-size:13px;margin-top:.6rem}
footer{margin-top:3rem;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:1rem}
"""


def _n(v, decimali=1):
    if v is None:
        return "—"
    if abs(v) >= 1_000_000:
        return f"{v/1_000_000:,.2f} mln".replace(",", "·").replace(".", ",").replace("·", ".")
    s = f"{v:,.{decimali}f}"
    return s.replace(",", "·").replace(".", ",").replace("·", ".")


def _barra(riga):
    """Mini box-plot: baffi min-max, box Q1-Q3, mediana, marcatore del target."""
    lo, hi = riga["min"], riga["max"]
    if hi == lo:
        return ""
    L, H, Y = 12, 168, 11

    def x(v):
        return L + (H - L) * max(0.0, min(1.0, (v - lo) / (hi - lo)))

    parti = [
        f'<line x1="{x(lo):.1f}" y1="{Y}" x2="{x(hi):.1f}" y2="{Y}" stroke="#c3ced9" stroke-width="1"/>',
        f'<rect x="{x(riga["q1"]):.1f}" y="{Y-5}" width="{max(1,x(riga["q3"])-x(riga["q1"])):.1f}" '
        f'height="10" fill="#e8eef5" stroke="#7d9bbd"/>',
        f'<line x1="{x(riga["mediana"]):.1f}" y1="{Y-7}" x2="{x(riga["mediana"]):.1f}" y2="{Y+7}" '
        f'stroke="#2c4a6b" stroke-width="2"/>',
    ]
    t = riga.get("target")
    if t is not None and lo <= t <= hi:
        parti.append(f'<circle cx="{x(t):.1f}" cy="{Y}" r="4.5" fill="#a5432f"/>')
    return f'<svg width="180" height="22" role="img">{"".join(parti)}</svg>'


def _classe(riga):
    """Colore della lettura: neutro sulle grandezze assolute, che dicono solo la taglia."""
    from indicatori import DIMENSIONALI, PEGGIO_SE_ALTO
    p = riga.get("percentile")
    if p is None or riga["indice"] in DIMENSIONALI:
        return ""
    q = 100 - p if riga["indice"] in PEGGIO_SE_ALTO else p
    return "g-alto" if q >= 60 else ("g-basso" if q <= 40 else "")


def genera(target, righe, peer, meta, percorso="output/benchmark.html"):
    e = html.escape
    nome = target.get("denominazione") or target.get("id") or "società analizzata"

    intestazione = "".join(
        f"<dt>{e(k)}</dt><dd>{e(str(v))}</dd>"
        for k, v in [
            ("Denominazione", nome),
            ("Partita IVA / CF", target.get("piva") or target.get("cf") or "—"),
            ("ATECO", f'{target.get("ateco") or "—"} — {target.get("descrizione_ateco") or ""}'.strip(" —")),
            ("Sede", f'{target.get("comune") or ""} ({target.get("provincia") or ""})'.strip()),
            ("Forma giuridica", target.get("forma_giuridica") or "—"),
        ] if v)

    corpo_tabella = "".join(
        f"<tr><td>{e(r['etichetta'])}</td>"
        f"<td class='target'>{_n(r.get('target'))}</td>"
        f"<td>{_n(r['q1'])}</td><td><b>{_n(r['mediana'])}</b></td><td>{_n(r['q3'])}</td>"
        f"<td>{_n(r['media'])}</td><td>{r['n']}</td>"
        f"<td>{_n(r['percentile'], 0) if r.get('percentile') is not None else '—'}</td>"
        f"<td class='{_classe(r)}'>{e(r['giudizio'])}</td>"
        f"<td>{_barra(r)}</td></tr>"
        for r in righe)

    elenco_peer = "".join(
        f"<tr><td>{e(str(p.get('denominazione') or p.get('id')))}</td>"
        f"<td>{e(str(p.get('piva') or p.get('id') or ''))}</td>"
        f"<td>{e(str(p.get('ateco') or ''))}</td>"
        f"<td>{e(str(p.get('provincia') or ''))}</td>"
        f"<td>{_n(p.get('fatturato'), 0)}</td>"
        f"<td>{_n(p.get('dipendenti'), 0)}</td></tr>"
        for p in peer)

    doc = f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Benchmark di settore — {e(nome)}</title><style>{CSS}</style></head><body><main>
<h1>Benchmark di settore</h1>
<p class="sub">{e(nome)} · confronto con {len(peer)} imprese comparabili · {date.today().strftime('%d/%m/%Y')}</p>
<div class="scheda"><dl>{intestazione}</dl></div>

<h2>Criteri del campione</h2>
<div class="scheda"><dl>{"".join(f"<dt>{e(str(k))}</dt><dd>{e(str(v))}</dd>" for k, v in meta.items())}</dl></div>

<h2>Posizionamento sugli indici</h2>
<div class="wrap"><table>
<thead><tr><th>Indice</th><th>Società</th><th>Q1</th><th>Mediana</th><th>Q3</th><th>Media</th>
<th>N</th><th>Perc.</th><th>Lettura</th><th>Distribuzione</th></tr></thead>
<tbody>{corpo_tabella}</tbody></table></div>
<p class="nota">Nel grafico: linea grigia min–max del settore, riquadro Q1–Q3, barra blu mediana,
punto rosso la società analizzata. «Perc.» è il percentile della società nel campione.</p>

<h2>Imprese del campione</h2>
<div class="wrap"><table>
<thead><tr><th>Denominazione</th><th>P.IVA</th><th>ATECO</th><th>Prov.</th><th>Fatturato</th><th>Dip.</th></tr></thead>
<tbody>{elenco_peer}</tbody></table></div>

<footer>Fonte dati: API Openapi (Registro Imprese / bilanci depositati). I bilanci depositati
scontano ritardi di pubblicazione e politiche di bilancio eterogenee: gli scostamenti vanno letti
come indizi, non come misure esatte.</footer>
</main></body></html>"""

    p = Path(percorso)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(doc, encoding="utf-8")
    return p
