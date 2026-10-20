#!/usr/bin/env python3
"""Prova completa della pipeline `tutto`, offline.

Serve a sapere che la sequenza stima -> peer -> scarica -> benchmark arriva
in fondo senza interrompersi: un errore scoperto a meta' corsa, con i bilanci
veri, sono crediti buttati.

    python3 test_pipeline.py
"""
import json, os, tempfile, unittest
from pathlib import Path

import cli
import imprese
from openapi_client import Client

ATECO = "45.19.01"


def _bilancio(ident, anno=2024, scala=1.0):
    return {"data": {"id": f"doc-{ident}", "state": "completed", "bilanci": [{
        "anno": anno,
        "conto_economico": {
            "ricavi_delle_vendite": 90_000_000 * scala,
            "valore_della_produzione": 91_000_000 * scala,
            "costi_della_produzione": 88_000_000 * scala,
            "ammortamenti": 900_000 * scala,
            "costo_del_personale": 3_800_000 * scala,
            "oneri_finanziari": 700_000 * scala,
            "utile_esercizio": 300_000 * scala},
        "stato_patrimoniale": {
            "totale_attivo": 60_000_000 * scala,
            "patrimonio_netto": 9_000_000 * scala,
            "debiti_verso_banche": 20_000_000 * scala,
            "disponibilita_liquide": 1_500_000 * scala,
            "rimanenze": 22_000_000 * scala,
            "crediti_verso_clienti": 12_000_000 * scala,
            "debiti_entro_esercizio": 30_000_000 * scala,
            "attivo_circolante": 36_000_000 * scala},
        "dipendenti": 60}]}}


class ClientSimulato(Client):
    """Risponde come l'API, senza rete: anagrafiche, conteggi e bilanci finti."""

    def __init__(self, **kw):
        super().__init__(token="finto", **kw)
        self.pagate = 0

    def chiama(self, metodo, url, params=None, body=None, a_pagamento=False, **kw):
        if a_pagamento:
            self._spendi(url)
            self.pagate += 1
        params = params or {}

        if "bilancio-riclassificato" in url:
            ident = (body or {}).get("cf_piva_id", "x")
            scala = 1.0 if ident == "03242670168" else 0.6 + (int(ident[-1]) % 5) * 0.4
            return _bilancio(ident, params.get("anno") or 2024, scala)

        if "/advance/" in url:                                  # scheda singola
            ident = url.rsplit("/", 1)[-1]
            return {"data": [{"denominazione": "Lodotruck S.r.l.", "piva": ident,
                              "codice_ateco": ATECO, "sede": {"provincia": "BG"},
                              "dati_bilancio": {"fatturato": 96_000_000, "anno_bilancio": 2024,
                                                "dipendenti": 60}}]}

        if url.endswith("/advance"):                            # ricerca
            pv = params.get("provincia")
            disponibili = {"BG": 3, "MI": 4, "VI": 2, None: 9}.get(pv, 0)
            if params.get("dry_run"):
                return {"data": {"count": disponibili}}
            quanti = min(disponibili, params.get("limit", 20))
            inizio = params.get("skip", 0)
            if inizio >= disponibili:
                return {"data": []}
            seme = {"BG": 1, "MI": 2, "VI": 3}.get(pv, 9) * 100
            return {"data": [{"denominazione": f"Concorrente {pv}{i}", "piva": f"{seme + i:011d}",
                              "codice_ateco": ATECO, "sede": {"provincia": pv},
                              "dati_bilancio": {"fatturato": 50_000_000 + i * 7_000_000,
                                                "anno_bilancio": 2024, "dipendenti": 40 + i}}
                             for i in range(inizio, min(inizio + quanti, disponibili))]}

        raise AssertionError(f"URL non previsto: {url} {params}")


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.precedente = os.getcwd()
        os.chdir(self.tmp.name)
        self.client = ClientSimulato(cache_dir=str(Path(self.tmp.name) / "cache"))
        self.originale = cli._client
        cli._client = lambda cfg, args: self.client

    def tearDown(self):
        cli._client = self.originale
        os.chdir(self.precedente)
        self.tmp.cleanup()

    def test_tutto_arriva_in_fondo(self):
        esito = cli.principale([
            "tutto", "03242670168", "--ambito", "nord", "--cifre-ateco", "6",
            "--banda", "3", "--limite", "9", "--anno", "2024",
            "--max-crediti", "40", "--conferma"])
        self.assertEqual(esito, 0)

        peer = json.loads(Path("dati/peer.json").read_text(encoding="utf-8"))["peer"]
        self.assertEqual(len(peer), 9)                      # 4 MI + 3 BG + 2 VI
        self.assertNotIn("03242670168", [p["id"] for p in peer])

        indici = json.loads(Path("dati/indici.json").read_text(encoding="utf-8"))
        self.assertEqual(len(indici), 10)                   # target + 9 concorrenti
        self.assertIn("2024", indici["03242670168"])

        html = Path("output/benchmark_2024.html").read_text(encoding="utf-8")
        self.assertIn("Lodotruck", html)
        self.assertIn("EBITDA margin", html)
        self.assertTrue(Path("output/benchmark_2024.csv").exists())
        self.assertTrue(Path("output/imprese_2024.csv").exists())

    def test_rilanciare_non_ripaga_i_bilanci(self):
        comune = ["--province", "BG", "--cifre-ateco", "6", "--limite", "3", "--conferma"]
        cli.principale(["peer", "03242670168"] + comune)
        cli.principale(["scarica", "--anno", "2024"] + comune)
        spese = self.client.pagate
        cli.principale(["scarica", "--anno", "2024"] + comune)   # secondo giro
        self.assertEqual(self.client.pagate, spese)         # nessun bilancio ricomprato


if __name__ == "__main__":
    unittest.main(verbosity=2)
