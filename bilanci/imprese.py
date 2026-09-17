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


# Le API filtrano per provincia, non per macroarea: "Nord Italia" va espanso.
PROVINCE_REGIONE = {
    "valle d'aosta": ["AO"],
    "piemonte": ["TO", "VC", "NO", "CN", "AT", "AL", "BI", "VB"],
    "liguria": ["IM", "SV", "GE", "SP"],
    "lombardia": ["VA", "CO", "SO", "MI", "BG", "BS", "PV", "CR", "MN", "LC", "LO", "MB"],
    "trentino-alto adige": ["BZ", "TN"],
    "veneto": ["VR", "VI", "BL", "TV", "VE", "PD", "RO"],
    "friuli-venezia giulia": ["UD", "GO", "TS", "PN"],
    "emilia-romagna": ["PC", "PR", "RE", "MO", "BO", "FE", "RA", "FC", "RN"],
}

MACROAREE = {
    "nordovest": ["valle d'aosta", "piemonte", "liguria", "lombardia"],
    "nordest": ["trentino-alto adige", "veneto", "friuli-venezia giulia", "emilia-romagna"],
}
MACROAREE["nord"] = MACROAREE["nordovest"] + MACROAREE["nordest"]


def province_di(ambito=None, regioni=None, province=None):
    """Elenco di sigle provinciali da ambito, regioni o elenco esplicito.

    Restituisce [] quando la ricerca e' nazionale o limitata a una sola provincia
    passata direttamente nei filtri.
    """
    if province:
        return [p.strip().upper() for p in province if p.strip()]
    nomi = []
    if regioni:
        nomi = [r.strip().lower() for r in regioni if r.strip()]
    elif ambito in MACROAREE:
        nomi = MACROAREE[ambito]
    fuori = [n for n in nomi if n not in PROVINCE_REGIONE]
    if fuori:
        raise ValueError(f"Regioni non riconosciute: {', '.join(fuori)}. "
                         f"Valide: {', '.join(sorted(PROVINCE_REGIONE))}")
    return [sigla for n in nomi for sigla in PROVINCE_REGIONE[n]]


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
    - `ambito`: "nazionale" | "provincia" | "regione" | "nord" | "nordovest" | "nordest".
      Gli ambiti multi-provincia non entrano nei filtri: la provincia viene
      aggiunta una alla volta da chi esegue la ricerca (vedi `province_di`).
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


def conta_per_provincia(client, cfg, filtri, province):
    """Conteggio gratuito provincia per provincia: dice dov'e' il settore.

    Serve a non sprecare chiamate a pagamento su province vuote e a capire se
    l'ambito scelto e' abbastanza capiente.
    """
    esito = {}
    for sigla in province:
        f = dict(filtri); f["provincia"] = sigla
        try:
            esito[sigla] = conta(client, cfg, f)
        except Exception as e:                      # una provincia muta non ferma il giro
            print(f"  ! {sigla}: {str(e)[:120]}")
            esito[sigla] = None
    return esito


def cerca_peer_province(client, cfg, filtri, province, limite=40, pagina=20,
                        escludi=(), conteggi=None):
    """Ricerca su piu' province, dalla piu' popolata alla meno.

    Le province senza imprese vengono saltate: il conteggio e' gratuito, la
    ricerca no.
    """
    conteggi = conteggi or conta_per_provincia(client, cfg, filtri, province)
    ordinate = sorted((p for p in province if (conteggi.get(p) or 0) > 0),
                      key=lambda p: -(conteggi.get(p) or 0))
    trovate, visti = [], {normalizza_id(x) for x in escludi if x}
    for sigla in ordinate:
        if len(trovate) >= limite:
            break
        f = dict(filtri); f["provincia"] = sigla
        quota = limite - len(trovate)
        parziali = cerca_peer(client, cfg, f, limite=quota, pagina=pagina, escludi=visti)
        for imp in parziali:
            visti.add(imp["id"])
        trovate.extend(parziali)
        print(f"  {sigla}: {len(parziali)} imprese (totale {len(trovate)}/{limite})")
    return trovate[:limite]


def leggi_elenco(percorso):
    """Partite IVA da file: una per riga, oppure CSV con la P.IVA nella prima colonna.

    Righe vuote e righe che iniziano con # vengono ignorate; dopo la prima
    colonna si puo' mettere il nome dell'impresa, che viene conservato.
    """
    voci = []
    for riga in open(percorso, encoding="utf-8-sig"):
        riga = riga.strip()
        riga = re.split(r"\s#", riga, maxsplit=1)[0].strip()   # commento a fine riga
        if not riga or riga.startswith("#"):
            continue
        pezzi = [p.strip() for p in re.split(r"[;,\t]", riga)]
        ident = normalizza_id(pezzi[0])
        if not ident or not ident[0].isdigit():
            continue                                 # intestazione del CSV
        voci.append({"id": ident, "denominazione": pezzi[1] if len(pezzi) > 1 else None})
    return voci


def peer_da_elenco(client, cfg, voci, con_anagrafica=True):
    """Costruisce il campione da una lista di partite IVA gia' scelta.

    Con `con_anagrafica` si paga una scheda per impresa e si ottengono ATECO,
    sede, fatturato e dipendenti; senza, restano solo gli identificativi e il
    confronto si basa unicamente sui bilanci.
    """
    peer = []
    for voce in voci:
        if not con_anagrafica:
            peer.append({"id": voce["id"], "piva": voce["id"],
                         "denominazione": voce.get("denominazione")})
            continue
        try:
            a, _ = scheda(client, cfg, voce["id"], avanzata=True)
        except Exception as e:
            print(f"  ! {voce['id']}: {str(e)[:150]}")
            continue
        if not a:
            print(f"  ! {voce['id']}: non trovata nel Registro Imprese")
            continue
        a["id"] = voce["id"]
        a["denominazione"] = a.get("denominazione") or voce.get("denominazione")
        peer.append(a)
        print(f"  · {a['denominazione']} — {a.get('provincia')} — ATECO {a.get('ateco')} "
              f"— fatt. {a.get('fatturato')}")
    return peer
