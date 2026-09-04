"""Anagrafica della societa' target e costruzione del gruppo di confronto (peer)."""
import re

import campi
from configurazione import url

ALIAS = {
    "denominazione": ["denominazione", "ragione_sociale", "company_name", "nome"],
    "piva": ["piva", "partita_iva", "vat_number", "partitaIva"],
    "cf": ["cf", "codice_fiscale", "tax_code", "codiceFiscale"],
    "ateco": ["codice_ateco", "ateco", "ateco_code", "codiceAteco", "atecoCode"],
    "descrizione_ateco": ["descrizione_ateco", "ateco_description", "attivita", "descrizioneAteco"],
    "provincia": ["provincia", "sigla_provincia", "province", "pv"],
    "comune": ["comune", "city", "citta"],
    "regione": ["regione", "region"],
    "forma_giuridica": ["forma_giuridica", "natura_giuridica", "legal_form"],
    "data_iscrizione": ["data_iscrizione", "data_costituzione", "registration_date"],
    "stato_attivita": ["stato_attivita", "stato", "status", "sede_stato_attivita"],
    "fatturato": ["fatturato", "revenue", "ricavi", "fatturato_annuo", "turnover"],
    "anno_fatturato": ["anno_fatturato", "anno_bilancio", "year", "anno"],
    "dipendenti": ["dipendenti", "numero_dipendenti", "employees", "addetti"],
    "cciaa": ["cciaa"],
    "rea": ["rea", "numero_rea", "nrea"],
}


def normalizza_id(identificativo):
    """Ripulisce partita IVA / codice fiscale: 'IT 01234567890 ' -> '01234567890'."""
    s = re.sub(r"[^0-9A-Za-z]", "", str(identificativo)).upper()
    return s[2:] if s.startswith("IT") and len(s) == 13 else s


def anagrafica(record):
    """Record grezzo -> dizionario con i campi che servono al benchmark."""
    piatto = campi.appiattisci(record)
    out = {}
    for nome, alias in ALIAS.items():
        numerico = nome in ("fatturato", "dipendenti", "anno_fatturato")
        out[nome] = campi.cerca(piatto, alias, solo_numerico=numerico)
    if out["ateco"]:
        out["ateco"] = str(out["ateco"]).strip()
    return out


def scheda(client, cfg, identificativo, avanzata=True):
    """Scheda della singola impresa. La versione `advance` consuma un credito."""
    chiave = "ricerca_advance" if avanzata else "ricerca_base"
    u = f"{url(cfg, 'imprese', chiave)}/{normalizza_id(identificativo)}"
    risposta = client.chiama("GET", u, a_pagamento=avanzata)
    record = campi.elenco(risposta)
    if not record:
        return None, risposta
    return anagrafica(record[0]), risposta


def _filtri(ateco=None, provincia=None, regione=None, fatturato_min=None,
            fatturato_max=None, dipendenti_min=None, dipendenti_max=None,
            denominazione=None):
    f = {
        "codice_ateco": ateco, "provincia": provincia, "regione": regione,
        "fatturato_min": fatturato_min, "fatturato_max": fatturato_max,
        "dipendenti_min": dipendenti_min, "dipendenti_max": dipendenti_max,
        "denominazione": denominazione,
    }
    return {k: v for k, v in f.items() if v not in (None, "")}


def filtri_da_target(target, cifre_ateco=4, ambito="nazionale",
                     banda_fatturato=(0.25, 4.0), banda_dipendenti=None):
    """Deriva i filtri del peer group dalla scheda della societa' analizzata.

    - `cifre_ateco`: 2 = divisione, 3 = gruppo, 4 = classe, 6 = sottocategoria.
      Meno cifre = piu' imprese, settore piu' largo.
    - `ambito`: "nazionale" | "provincia" | "regione".
    - `banda_fatturato`: moltiplicatori sul fatturato del target, per confrontare
      imprese di dimensione paragonabile (un benchmark tra taglie diverse mente).
    """
    ateco = (target.get("ateco") or "").replace(" ", "")
    ateco_troncato = re.sub(r"[^0-9]", "", ateco)[:cifre_ateco] or None
    arg = {"ateco": ateco_troncato}
    if ambito == "provincia" and target.get("provincia"):
        arg["provincia"] = target["provincia"]
    elif ambito == "regione" and target.get("regione"):
        arg["regione"] = target["regione"]
    fatt = target.get("fatturato")
    if fatt and banda_fatturato:
        arg["fatturato_min"] = int(fatt * banda_fatturato[0])
        arg["fatturato_max"] = int(fatt * banda_fatturato[1])
    dip = target.get("dipendenti")
    if dip and banda_dipendenti:
        arg["dipendenti_min"] = max(1, int(dip * banda_dipendenti[0]))
        arg["dipendenti_max"] = int(dip * banda_dipendenti[1])
    return _filtri(**arg)


def conta(client, cfg, filtri):
    """Quante imprese soddisfano i filtri. `dry_run` non consuma crediti."""
    params = dict(filtri); params["dry_run"] = 1
    risposta = client.chiama("GET", url(cfg, "imprese", "ricerca_advance"),
                             params=params, a_pagamento=False)
    piatto = campi.appiattisci(risposta)
    n = campi.cerca(piatto, ["count", "numero", "total", "totale", "records", "risultati"],
                    solo_numerico=True)
    return int(n) if n is not None else None


def cerca_peer(client, cfg, filtri, limite=40, pagina=20, escludi=()):
    """Ricerca paginata delle imprese confrontabili. Ogni pagina consuma crediti."""
    escludi = {normalizza_id(x) for x in escludi if x}
    trovate, skip = [], 0
    while len(trovate) < limite:
        params = dict(filtri)
        params.update({"limit": min(pagina, limite - len(trovate)), "skip": skip})
        risposta = client.chiama("GET", url(cfg, "imprese", "ricerca_advance"),
                                 params=params, a_pagamento=True)
        record = campi.elenco(risposta)
        if not record:
            break
        for r in record:
            a = anagrafica(r)
            ident = normalizza_id(a.get("piva") or a.get("cf") or "")
            if not ident or ident in escludi:
                continue
            escludi.add(ident)
            a["id"] = ident
            trovate.append(a)
        skip += len(record)
        if len(record) < params["limit"]:
            break
    return trovate[:limite]
