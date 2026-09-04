"""Dal bilancio grezzo alle voci normalizzate e agli indici di bilancio.

La struttura JSON del bilancio non e' garantita: si individuano gli esercizi
(dizionari che contengono un anno e almeno una voce economica) e per ciascuno si
estraggono le voci per alias. Gli alias sono sovrascrivibili da `mappa_campi.json`,
cosi' l'adattamento al payload reale non richiede modifiche al codice.
"""
import json
from pathlib import Path

import campi

ALIAS_VOCI = {
    "ricavi": ["ricavi", "ricavi_vendite", "ricavi_delle_vendite", "ricavi_vendite_prestazioni",
               "fatturato", "revenue", "net_revenues", "totale_ricavi", "vendite"],
    "valore_produzione": ["valore_della_produzione", "valore_produzione", "totale_valore_produzione",
                          "production_value"],
    "costi_produzione": ["costi_della_produzione", "costi_produzione", "totale_costi_produzione"],
    "valore_aggiunto": ["valore_aggiunto", "added_value"],
    "costo_lavoro": ["costo_del_personale", "costi_personale", "costo_lavoro", "personale",
                     "labour_cost", "personnel_cost"],
    "ebitda": ["ebitda", "margine_operativo_lordo", "mol"],
    "ammortamenti": ["ammortamenti", "ammortamenti_svalutazioni", "depreciation", "amortization"],
    "ebit": ["ebit", "risultato_operativo", "reddito_operativo", "operating_income"],
    "oneri_finanziari": ["oneri_finanziari", "interessi_passivi", "financial_charges",
                         "proventi_e_oneri_finanziari"],
    "imposte": ["imposte", "imposte_sul_reddito", "taxes", "imposte_esercizio"],
    "utile_netto": ["utile_esercizio", "utile_netto", "risultato_esercizio", "risultato_netto",
                    "net_income", "net_profit", "utile_perdita_esercizio"],
    "attivo_totale": ["totale_attivo", "attivo_totale", "totale_attivita", "total_assets",
                      "capitale_investito"],
    "immobilizzazioni": ["immobilizzazioni", "totale_immobilizzazioni", "attivo_immobilizzato",
                         "fixed_assets"],
    "attivo_circolante": ["attivo_circolante", "totale_attivo_circolante", "current_assets"],
    "rimanenze": ["rimanenze", "totale_rimanenze", "magazzino", "inventories"],
    "crediti_clienti": ["crediti_verso_clienti", "crediti_clienti", "trade_receivables"],
    "liquidita": ["disponibilita_liquide", "liquidita", "cassa", "cash", "cash_and_equivalents"],
    "patrimonio_netto": ["patrimonio_netto", "totale_patrimonio_netto", "equity", "net_equity",
                         "mezzi_propri"],
    "debiti_totali": ["totale_debiti", "debiti", "total_liabilities", "totale_passivo_debiti"],
    "debiti_finanziari": ["debiti_verso_banche", "debiti_finanziari", "debiti_bancari",
                          "financial_debts", "debiti_verso_altri_finanziatori"],
    "debiti_fornitori": ["debiti_verso_fornitori", "debiti_fornitori", "trade_payables"],
    "debiti_breve": ["debiti_entro_esercizio", "debiti_a_breve", "passivita_correnti",
                     "current_liabilities"],
    "dipendenti": ["dipendenti", "numero_dipendenti", "employees", "addetti", "numero_medio_dipendenti"],
}

ALIAS_ANNO = ["anno", "anno_chiusura", "esercizio", "year", "fiscal_year", "balance_sheet_year",
              "data_chiusura", "balanceSheetDate", "chiusura"]


def carica_alias(percorso="mappa_campi.json"):
    """Unisce agli alias predefiniti quelli personalizzati dell'utente."""
    alias = {k: list(v) for k, v in ALIAS_VOCI.items()}
    p = Path(percorso)
    if p.exists():
        extra = json.loads(p.read_text(encoding="utf-8"))
        for k, v in extra.items():
            if k.startswith("_") or not isinstance(v, list):
                continue          # chiavi di commento
            alias[k] = list(v) + alias.get(k, [])
    return alias


def _anno(valore):
    if valore is None:
        return None
    s = str(valore)
    for pezzo in (s[:4], s[-4:]):
        if pezzo.isdigit() and 1990 <= int(pezzo) <= 2100:
            return int(pezzo)
    n = campi.numero(valore)
    return int(n) if n and 1990 <= n <= 2100 else None


def _nodi_esercizio(dati, alias):
    """Dizionari che sembrano un esercizio: hanno un anno e almeno tre voci note."""
    trovati = []

    def visita(nodo):
        if isinstance(nodo, dict):
            piatto = campi.appiattisci(nodo)
            anno = _anno(campi.cerca(piatto, ALIAS_ANNO))
            if anno:
                presenti = sum(1 for a in alias.values()
                               if campi.cerca(piatto, a, solo_numerico=True) is not None)
                if presenti >= 3:
                    trovati.append((anno, piatto))
            for v in nodo.values():
                visita(v)
        elif isinstance(nodo, list):
            for v in nodo:
                visita(v)

    visita(dati)
    # tiene il nodo piu' ricco per ciascun anno (i nidificati ripetono gli stessi anni)
    migliori = {}
    for anno, piatto in trovati:
        if anno not in migliori or len(piatto) > len(migliori[anno]):
            migliori[anno] = piatto
    return migliori


def voci(esito, alias=None):
    """Bilancio grezzo -> {anno: {voce: valore}} con le voci normalizzate."""
    alias = alias or carica_alias()
    dati = campi.contenuto(esito)
    esercizi = _nodi_esercizio(dati, alias)
    if not esercizi:
        piatto = campi.appiattisci(dati)
        anno = _anno(campi.cerca(piatto, ALIAS_ANNO))
        esercizi = {anno or 0: piatto}
    out = {}
    for anno, piatto in esercizi.items():
        riga = {v: campi.cerca(piatto, a, solo_numerico=True) for v, a in alias.items()}
        riga["anno"] = anno
        out[anno] = riga
    return out


def _div(a, b):
    if a is None or not b:
        return None
    return a / b


def _pct(a, b):
    r = _div(a, b)
    return None if r is None else r * 100


def _giorni(a, b):
    r = _div(a, b)
    return None if r is None else r * 365


def indici(v):
    """Indici di redditivita', struttura e produttivita' da una riga di voci.

    Le voci mancanti vengono ricostruite quando l'identita' contabile lo consente
    (EBITDA da valore della produzione e costi, PFN da debiti e liquidita').
    """
    v = dict(v)
    if v.get("ricavi") is None:
        v["ricavi"] = v.get("valore_produzione")
    if v.get("ebit") is None and v.get("valore_produzione") is not None and v.get("costi_produzione") is not None:
        v["ebit"] = v["valore_produzione"] - v["costi_produzione"]
    if v.get("ebitda") is None and v.get("ebit") is not None and v.get("ammortamenti") is not None:
        v["ebitda"] = v["ebit"] + v["ammortamenti"]
    if v.get("valore_aggiunto") is None and v.get("ebitda") is not None and v.get("costo_lavoro") is not None:
        v["valore_aggiunto"] = v["ebitda"] + v["costo_lavoro"]

    pfn = None
    if v.get("debiti_finanziari") is not None:
        pfn = v["debiti_finanziari"] - (v.get("liquidita") or 0)

    ric, pn, att = v.get("ricavi"), v.get("patrimonio_netto"), v.get("attivo_totale")
    attivo_corrente = None
    if v.get("attivo_circolante") is not None:
        attivo_corrente = v["attivo_circolante"]
    elif None not in (v.get("rimanenze"), v.get("crediti_clienti"), v.get("liquidita")):
        attivo_corrente = v["rimanenze"] + v["crediti_clienti"] + v["liquidita"]

    return {
        "ricavi": ric,
        "ebitda": v.get("ebitda"),
        "ebit": v.get("ebit"),
        "utile_netto": v.get("utile_netto"),
        "patrimonio_netto": pn,
        "attivo_totale": att,
        "pfn": pfn,
        "dipendenti": v.get("dipendenti"),
        "ebitda_margin_pct": _pct(v.get("ebitda"), ric),
        "ros_pct": _pct(v.get("ebit"), ric),
        "roi_pct": _pct(v.get("ebit"), att),
        "roe_pct": _pct(v.get("utile_netto"), pn),
        "ros_netto_pct": _pct(v.get("utile_netto"), ric),
        "valore_aggiunto_pct": _pct(v.get("valore_aggiunto"), ric),
        "incidenza_lavoro_pct": _pct(v.get("costo_lavoro"), ric),
        "leva_finanziaria": _div(att, pn),
        "debt_equity": _div(v.get("debiti_finanziari"), pn),
        "pfn_ebitda": _div(pfn, v.get("ebitda")),
        "oneri_su_ricavi_pct": _pct(v.get("oneri_finanziari"), ric),
        "current_ratio": _div(attivo_corrente, v.get("debiti_breve")),
        "rotazione_capitale": _div(ric, att),
        "giorni_credito": _giorni(v.get("crediti_clienti"), ric),
        "giorni_magazzino": _giorni(v.get("rimanenze"), ric),
        "ricavi_per_dipendente": _div(ric, v.get("dipendenti")),
        "valore_agg_per_dipendente": _div(v.get("valore_aggiunto"), v.get("dipendenti")),
        "costo_medio_dipendente": _div(v.get("costo_lavoro"), v.get("dipendenti")),
    }


ETICHETTE = {
    "ricavi": "Ricavi (€)",
    "ebitda": "EBITDA (€)",
    "ebit": "EBIT (€)",
    "utile_netto": "Utile netto (€)",
    "patrimonio_netto": "Patrimonio netto (€)",
    "attivo_totale": "Totale attivo (€)",
    "pfn": "Posizione finanziaria netta (€)",
    "dipendenti": "Dipendenti",
    "ebitda_margin_pct": "EBITDA margin %",
    "ros_pct": "ROS % (EBIT/Ricavi)",
    "roi_pct": "ROI % (EBIT/Attivo)",
    "roe_pct": "ROE % (Utile/PN)",
    "ros_netto_pct": "Utile netto / Ricavi %",
    "valore_aggiunto_pct": "Valore aggiunto / Ricavi %",
    "incidenza_lavoro_pct": "Costo lavoro / Ricavi %",
    "leva_finanziaria": "Leva (Attivo/PN)",
    "debt_equity": "Debiti fin. / PN",
    "pfn_ebitda": "PFN / EBITDA",
    "oneri_su_ricavi_pct": "Oneri finanziari / Ricavi %",
    "current_ratio": "Current ratio",
    "rotazione_capitale": "Rotazione del capitale",
    "giorni_credito": "Giorni medi di credito",
    "giorni_magazzino": "Giorni medi di magazzino",
    "ricavi_per_dipendente": "Ricavi per dipendente (€)",
    "valore_agg_per_dipendente": "Valore aggiunto per dipendente (€)",
    "costo_medio_dipendente": "Costo medio per dipendente (€)",
}

# indici per cui un valore alto e' peggio: il percentile va letto al contrario
PEGGIO_SE_ALTO = {"pfn", "pfn_ebitda", "debt_equity", "leva_finanziaria", "oneri_su_ricavi_pct",
                  "incidenza_lavoro_pct", "giorni_credito", "giorni_magazzino",
                  "costo_medio_dipendente"}

# grandezze assolute: dicono la taglia dell'impresa, non la sua qualita' gestionale
DIMENSIONALI = {"ricavi", "ebitda", "ebit", "utile_netto", "patrimonio_netto",
                "attivo_totale", "pfn", "dipendenti"}
