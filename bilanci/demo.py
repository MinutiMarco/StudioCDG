#!/usr/bin/env python3
"""Genera un benchmark di esempio con dati sintetici, senza chiamare le API.

Serve a vedere com'e' fatto il report (e a verificare la catena di calcolo)
prima di spendere un solo credito.
"""
import random
from pathlib import Path

import benchmark as mod_benchmark
import indicatori
import report

random.seed(7)


def _impresa(nome, piva, ricavi, margine, leva, dipendenti):
    ebitda = ricavi * margine
    amm = ricavi * 0.035
    ebit = ebitda - amm
    deb = ricavi * leva
    pn = max(ricavi * 0.28, 1)
    return {
        "denominazione": nome, "piva": piva, "id": piva, "ateco": "25.62",
        "provincia": random.choice(["BS", "BG", "MI", "VI", "TV"]),
        "fatturato": ricavi, "dipendenti": dipendenti,
        "voci": {
            "anno": 2024, "ricavi": ricavi, "valore_produzione": ricavi * 1.02,
            "costi_produzione": ricavi * 1.02 - ebit, "ammortamenti": amm,
            "costo_lavoro": ricavi * 0.24, "oneri_finanziari": deb * 0.05,
            "utile_netto": (ebit - deb * 0.05) * 0.72, "attivo_totale": ricavi * 0.95,
            "patrimonio_netto": pn, "debiti_finanziari": deb, "liquidita": ricavi * 0.06,
            "rimanenze": ricavi * 0.19, "crediti_clienti": ricavi * 0.26,
            "debiti_breve": ricavi * 0.31, "attivo_circolante": ricavi * 0.55,
            "dipendenti": dipendenti,
        },
    }


def dataset():
    target = _impresa("Alfa Meccanica S.r.l.", "00000000001", 8_400_000, 0.088, 0.42, 41)
    target["descrizione_ateco"] = "Lavori di meccanica generale"
    target["comune"] = "Lumezzane"
    target["forma_giuridica"] = "S.R.L."
    peer = [
        _impresa(f"Impresa {i:02d} S.r.l.", f"0000000{i:04d}",
                 ricavi=random.uniform(3.2e6, 22e6),
                 margine=random.gauss(0.115, 0.035),
                 leva=max(0.05, random.gauss(0.35, 0.18)),
                 dipendenti=random.randint(12, 95))
        for i in range(1, 29)
    ]
    return target, peer


def main():
    target, peer = dataset()
    ind_target = indicatori.indici(target["voci"])
    ind_peer = [indicatori.indici(p["voci"]) for p in peer]
    righe = mod_benchmark.confronta(ind_target, ind_peer)
    out = Path("esempio")   # versionato: serve da anteprima del report
    csv_out = mod_benchmark.esporta_csv(
        righe, out / "benchmark_demo.csv",
        colonne=["etichetta", "target", "percentile", "giudizio", "n", "min", "q1",
                 "mediana", "q3", "max", "media", "dev_std"])
    html_out = report.genera(
        target, righe, peer,
        {"Esercizio di riferimento": 2024, "Imprese nel campione": len(peer),
         "Filtri di ricerca": "codice_ateco=25.62 (dati dimostrativi)",
         "Fonte bilanci": "dati sintetici — nessuna chiamata alle API"},
        out / "benchmark_demo.html")
    for r in righe[:12]:
        print(f"  {r['etichetta']:34} {r['target']:>14,.1f}  mediana {r['mediana']:>14,.1f}  {r['giudizio']}")
    print(f"\n  CSV:  {csv_out}\n  HTML: {html_out}")


if __name__ == "__main__":
    main()
