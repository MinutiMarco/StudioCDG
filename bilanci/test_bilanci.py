#!/usr/bin/env python3
"""Test offline: nessuna chiamata di rete, nessun credito consumato.

    python3 test_bilanci.py
"""
import json, tempfile, unittest
from pathlib import Path

import benchmark as mod_benchmark
import bilanci as mod_bilanci
import campi
import configurazione
import imprese
import indicatori
import report
from openapi_client import BudgetEsaurito, Client


# ---- risposte finte, con le due forme piu' probabili (dati in `data`, nomi misti) ----

RISPOSTA_ADVANCE = {
    "success": True,
    "data": [{
        "denominazione": "Alfa Meccanica S.r.l.",
        "piva": "01234567890", "cf": "01234567890",
        "codice_ateco": "25.62", "descrizione_ateco": "Lavori di meccanica generale",
        "sede": {"comune": "Lumezzane", "provincia": "BS", "regione": "Lombardia"},
        "forma_giuridica": "S.R.L.",
        "dati_bilancio": {"fatturato": "8.400.000,00", "anno_bilancio": 2024, "dipendenti": 41},
    }],
}

RISPOSTA_RICLASSIFICATO = {
    "data": {
        "id": "abc123", "state": "completed",
        "bilanci": [
            {"anno": 2024, "conto_economico": {
                "ricavi_delle_vendite": 8400000, "valore_della_produzione": 8568000,
                "costi_della_produzione": 8122800, "ammortamenti": 294000,
                "costo_del_personale": 2016000, "oneri_finanziari": 176400,
                "utile_esercizio": 193536},
             "stato_patrimoniale": {
                "totale_attivo": 7980000, "patrimonio_netto": 2352000,
                "debiti_verso_banche": 3528000, "disponibilita_liquide": 504000,
                "rimanenze": 1596000, "crediti_verso_clienti": 2184000,
                "debiti_entro_esercizio": 2604000, "attivo_circolante": 4620000},
             "dipendenti": 41},
            {"anno": 2023, "conto_economico": {
                "ricavi_delle_vendite": 7600000, "valore_della_produzione": 7700000,
                "costi_della_produzione": 7350000, "ammortamenti": 260000,
                "utile_esercizio": 150000},
             "stato_patrimoniale": {
                "totale_attivo": 7400000, "patrimonio_netto": 2150000,
                "debiti_verso_banche": 3300000, "disponibilita_liquide": 400000},
             "dipendenti": 38},
        ],
    },
}


class ClientFinto(Client):
    """Non tocca la rete: restituisce risposte preparate e conta le chiamate."""

    def __init__(self, risposte, **kw):
        super().__init__(token="finto", cache_dir=kw.pop("cache_dir", "cache"), **kw)
        self.risposte = risposte
        self.chiamate = []

    def chiama(self, metodo, url, params=None, body=None, a_pagamento=False, **kw):
        self.chiamate.append((metodo, url, params, body))
        if a_pagamento:
            self._spendi(url)
        for frammento, risposta in self.risposte.items():
            if frammento in url:
                return risposta
        raise AssertionError(f"URL non previsto nel test: {url}")


class TestCampi(unittest.TestCase):
    def test_numero_formati_italiani(self):
        self.assertEqual(campi.numero("1.234.567,89"), 1234567.89)
        self.assertEqual(campi.numero("1234567.89"), 1234567.89)
        self.assertEqual(campi.numero("8.400"), 8400.0)
        self.assertEqual(campi.numero("(1.500,00)"), -1500.0)
        self.assertEqual(campi.numero("0.085"), 0.085)      # non e' un separatore di migliaia
        self.assertEqual(campi.numero("1.5"), 1.5)
        self.assertIsNone(campi.numero("n/d"))
        self.assertIsNone(campi.numero(None))

    def test_alias_insensibile_a_forma(self):
        piatto = campi.appiattisci({"a": {"Valore Della Produzione": "1.000,50"}})
        self.assertEqual(campi.cerca(piatto, ["valore_della_produzione"], solo_numerico=True), 1000.5)

    def test_elenco_normalizza(self):
        self.assertEqual(len(campi.elenco({"data": [1, 2, 3]})), 3)
        self.assertEqual(len(campi.elenco({"data": {"x": 1}})), 1)


class TestImprese(unittest.TestCase):
    def test_normalizza_id(self):
        self.assertEqual(imprese.normalizza_id("IT 01234567890"), "01234567890")
        self.assertEqual(imprese.normalizza_id("0123-4567890"), "01234567890")

    def test_anagrafica_e_filtri(self):
        a = imprese.anagrafica(RISPOSTA_ADVANCE["data"][0])
        self.assertEqual(a["denominazione"], "Alfa Meccanica S.r.l.")
        self.assertEqual(a["ateco"], "25.62")
        self.assertEqual(a["provincia"], "BS")
        self.assertEqual(a["fatturato"], 8400000.0)
        self.assertEqual(a["dipendenti"], 41.0)

        f = imprese.filtri_da_target(a, cifre_ateco=4, ambito="provincia",
                                     banda_fatturato=(0.5, 2.0))
        self.assertEqual(f["codice_ateco"], "2562")
        self.assertEqual(f["provincia"], "BS")
        self.assertEqual(f["fatturato_min"], 4200000)
        self.assertEqual(f["fatturato_max"], 16800000)

        f2 = imprese.filtri_da_target(a, cifre_ateco=2, ambito="nazionale", banda_fatturato=None)
        self.assertEqual(f2["codice_ateco"], "25")
        self.assertNotIn("provincia", f2)
        self.assertNotIn("fatturato_min", f2)

    def test_conta_non_paga(self):
        cfg = configurazione.carica("config.inesistente.toml")
        cl = ClientFinto({"/advance": {"data": {"count": 137}}})
        self.assertEqual(imprese.conta(cl, cfg, {"codice_ateco": "2562"}), 137)
        self.assertEqual(cl.crediti_spesi, 0)
        self.assertEqual(cl.chiamate[0][2]["dry_run"], 1)


class TestIndicatori(unittest.TestCase):
    def setUp(self):
        self.per_anno = indicatori.voci(RISPOSTA_RICLASSIFICATO, indicatori.ALIAS_VOCI)

    def test_riconosce_gli_esercizi(self):
        self.assertEqual(sorted(self.per_anno), [2023, 2024])
        self.assertEqual(self.per_anno[2024]["ricavi"], 8400000)
        self.assertEqual(self.per_anno[2024]["patrimonio_netto"], 2352000)

    def test_indici_derivati(self):
        i = indicatori.indici(self.per_anno[2024])
        self.assertAlmostEqual(i["ebit"], 445200, places=0)          # VP - CP
        self.assertAlmostEqual(i["ebitda"], 739200, places=0)        # EBIT + ammortamenti
        self.assertAlmostEqual(i["pfn"], 3024000, places=0)          # debiti fin. - liquidita'
        self.assertAlmostEqual(i["ebitda_margin_pct"], 8.8, places=1)
        self.assertAlmostEqual(i["roe_pct"], 8.23, places=1)
        self.assertAlmostEqual(i["ricavi_per_dipendente"], 204878, places=0)
        self.assertAlmostEqual(i["current_ratio"], 1.774, places=2)

    def test_voci_mancanti_non_esplodono(self):
        i = indicatori.indici({"anno": 2024, "ricavi": None, "patrimonio_netto": 0})
        self.assertIsNone(i["ebitda_margin_pct"])
        self.assertIsNone(i["roe_pct"])


class TestBenchmark(unittest.TestCase):
    def test_quartili(self):
        q = mod_benchmark.quartili([1, 2, 3, 4, 5])
        self.assertEqual((q["n"], q["min"], q["q1"], q["mediana"], q["q3"], q["max"]),
                         (5, 1, 2, 3, 4, 5))
        self.assertIsNone(mod_benchmark.quartili([None, None]))

    def test_percentile_e_giudizio(self):
        valori = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(mod_benchmark.percentile(10, valori), 95.0)
        self.assertEqual(mod_benchmark.percentile(0, valori), 0.0)
        # su un indice dove alto = peggio il giudizio si rovescia
        self.assertIn("sotto", mod_benchmark.giudizio("pfn_ebitda", 95.0))
        self.assertIn("sopra", mod_benchmark.giudizio("roe_pct", 95.0))
        # le grandezze assolute parlano di taglia, non di performance
        self.assertIn("grandi", mod_benchmark.giudizio("ricavi", 95.0))

    def test_confronto_completo(self):
        target = indicatori.indici({"ricavi": 1000, "ebitda": 80, "patrimonio_netto": 500,
                                    "utile_netto": 40, "attivo_totale": 900, "ebit": 60})
        peer = [indicatori.indici({"ricavi": 1000 + i, "ebitda": 100 + i, "patrimonio_netto": 500,
                                   "utile_netto": 70, "attivo_totale": 900, "ebit": 90})
                for i in range(8)]
        righe = mod_benchmark.confronta(target, peer)
        per_indice = {r["indice"]: r for r in righe}
        self.assertEqual(per_indice["ebitda_margin_pct"]["n"], 8)
        self.assertLess(per_indice["ebitda_margin_pct"]["percentile"], 10)
        self.assertIn("sotto", per_indice["roe_pct"]["giudizio"])

    def test_cagr(self):
        self.assertAlmostEqual(mod_benchmark.crescita_pct({2022: 100, 2024: 121}), 10.0, places=2)
        self.assertIsNone(mod_benchmark.crescita_pct({2024: 100}))


class TestBudgetECache(unittest.TestCase):
    def test_budget_blocca(self):
        with tempfile.TemporaryDirectory() as d:
            cl = ClientFinto({"/advance": {"data": []}}, cache_dir=d, max_crediti=2)
            for _ in range(2):
                cl.chiama("GET", "https://x/advance", a_pagamento=True)
            with self.assertRaises(BudgetEsaurito):
                cl.chiama("GET", "https://x/advance", a_pagamento=True)

    def test_bilancio_gia_scaricato_non_si_ripaga(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = configurazione.carica("config.inesistente.toml")
            cfg["percorsi"]["dati"] = d
            cl = ClientFinto({"bilancio-riclassificato": RISPOSTA_RICLASSIFICATO}, cache_dir=d)
            _, da_cache = mod_bilanci.riclassificato(cl, cfg, "01234567890", anno=2024)
            self.assertFalse(da_cache)
            self.assertEqual(cl.crediti_spesi, 1)
            _, da_cache = mod_bilanci.riclassificato(cl, cfg, "01234567890", anno=2024)
            self.assertTrue(da_cache)
            self.assertEqual(cl.crediti_spesi, 1)      # nessuna spesa aggiuntiva


class TestReport(unittest.TestCase):
    def test_html_autonomo(self):
        target = imprese.anagrafica(RISPOSTA_ADVANCE["data"][0])
        per_anno = indicatori.voci(RISPOSTA_RICLASSIFICATO, indicatori.ALIAS_VOCI)
        ind_target = indicatori.indici(per_anno[2024])
        peer = [indicatori.indici(dict(per_anno[2024], ricavi=8400000 * k, ebitda=700000 * k))
                for k in (0.7, 1.1, 1.4, 2.0)]
        righe = mod_benchmark.confronta(ind_target, peer)
        with tempfile.TemporaryDirectory() as d:
            p = report.genera(target, righe, [target], {"Esercizio": 2024}, Path(d) / "r.html")
            testo = p.read_text(encoding="utf-8")
        self.assertIn("Alfa Meccanica", testo)
        self.assertIn("<svg", testo)
        self.assertNotIn("http://", testo.replace("http://www.w3.org", ""))   # nessuna risorsa esterna


if __name__ == "__main__":
    unittest.main(verbosity=2)
