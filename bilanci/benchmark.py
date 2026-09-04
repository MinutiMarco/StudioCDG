"""Statistiche di settore e posizionamento della societa' analizzata.

Il confronto e' su quartili, non su medie: in un settore con poche imprese
grandi la media e' dominata dagli estremi, la mediana no.
"""
import csv, statistics
from pathlib import Path

from indicatori import DIMENSIONALI, ETICHETTE, PEGGIO_SE_ALTO


def _validi(valori):
    return [v for v in valori if isinstance(v, (int, float)) and v == v]


def quartili(valori):
    v = sorted(_validi(valori))
    if not v:
        return None
    n = len(v)

    def q(p):
        if n == 1:
            return v[0]
        pos = p * (n - 1)
        basso = int(pos)
        alto = min(basso + 1, n - 1)
        return v[basso] + (v[alto] - v[basso]) * (pos - basso)

    return {
        "n": n, "min": v[0], "q1": q(0.25), "mediana": q(0.5), "q3": q(0.75), "max": v[-1],
        "media": statistics.fmean(v),
        "dev_std": statistics.stdev(v) if n > 1 else 0.0,
    }


def percentile(valore, valori):
    """Quota di imprese del campione con valore inferiore (0-100)."""
    v = _validi(valori)
    if valore is None or not v:
        return None
    sotto = sum(1 for x in v if x < valore)
    pari = sum(1 for x in v if x == valore)
    return 100.0 * (sotto + 0.5 * pari) / len(v)


def giudizio(indice, perc):
    """Traduce il percentile in un giudizio, girandolo dove alto = peggio.

    Sulle grandezze assolute il giudizio parla di taglia, non di performance:
    fatturare meno della mediana non e' un difetto gestionale.
    """
    if perc is None:
        return "—"
    if indice in DIMENSIONALI:
        if perc >= 75:
            return "tra le più grandi del campione"
        if perc >= 55:
            return "sopra la mediana per dimensione"
        if perc >= 45:
            return "dimensione mediana"
        if perc >= 25:
            return "sotto la mediana per dimensione"
        return "tra le più piccole del campione"
    p = 100 - perc if indice in PEGGIO_SE_ALTO else perc
    if p >= 75:
        return "molto sopra la media di settore"
    if p >= 55:
        return "sopra la mediana"
    if p >= 45:
        return "in linea con la mediana"
    if p >= 25:
        return "sotto la mediana"
    return "molto sotto la media di settore"


def confronta(indici_target, indici_peer):
    """Per ogni indice: statistiche del settore, valore target, percentile, giudizio.

    `indici_peer` e' una lista di dizionari indice->valore (uno per impresa).
    """
    righe = []
    for indice, etichetta in ETICHETTE.items():
        valori = [p.get(indice) for p in indici_peer]
        stat = quartili(valori)
        if not stat:
            continue
        valore = indici_target.get(indice) if indici_target else None
        perc = percentile(valore, valori)
        righe.append({
            "indice": indice, "etichetta": etichetta, "target": valore,
            "percentile": perc, "giudizio": giudizio(indice, perc), **stat,
        })
    return righe


def serie_storica(per_impresa, indice):
    """{impresa: {anno: indici}} -> {anno: [valori]} per l'indice richiesto."""
    per_anno = {}
    for anni in per_impresa.values():
        for anno, ind in anni.items():
            if ind.get(indice) is not None:
                per_anno.setdefault(anno, []).append(ind[indice])
    return dict(sorted(per_anno.items()))


def crescita_pct(serie_ricavi):
    """CAGR % dai ricavi per anno {anno: valore}, None se non calcolabile."""
    anni = sorted(a for a, v in serie_ricavi.items() if v)
    if len(anni) < 2:
        return None
    primo, ultimo = serie_ricavi[anni[0]], serie_ricavi[anni[-1]]
    periodi = anni[-1] - anni[0]
    if primo <= 0 or ultimo <= 0 or periodi <= 0:
        return None
    return ((ultimo / primo) ** (1 / periodi) - 1) * 100


def esporta_csv(righe, percorso, colonne=None):
    percorso = Path(percorso)
    percorso.parent.mkdir(parents=True, exist_ok=True)
    if not righe:
        percorso.write_text("", encoding="utf-8")
        return percorso
    colonne = colonne or list(righe[0].keys())
    with open(percorso, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=colonne, delimiter=";", extrasaction="ignore")
        w.writeheader()
        for r in righe:
            w.writerow({c: _fmt(r.get(c)) for c in colonne})
    return percorso


def _fmt(v):
    if isinstance(v, float):
        return f"{v:.2f}".replace(".", ",")   # separatore italiano, per Excel
    return "" if v is None else v
