"""Richiesta, attesa e scarico dei bilanci.

Le API di bilancio sono asincrone: si crea la richiesta (POST), si attende che
lo stato diventi completato, poi si legge il risultato o si scaricano gli
allegati. Ogni richiesta e' a pagamento, quindi l'esito viene sempre salvato su
disco in `dati/bilanci/` e riletto da li' alle esecuzioni successive.
"""
import json, time
from pathlib import Path

import campi
from configurazione import url
from imprese import normalizza_id

STATI_OK = {"completed", "complete", "completato", "done", "success", "evaso", "ok", "closed"}
STATI_KO = {"failed", "error", "errore", "rejected", "not_found", "annullato", "canceled"}


def _archivio(cfg, tipo, ident, anno):
    d = Path(cfg["percorsi"]["dati"]) / "bilanci" / tipo
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{normalizza_id(ident)}_{anno or 'ultimo'}.json"


def _stato(risposta):
    piatto = campi.appiattisci(risposta)
    s = campi.cerca(piatto, ["state", "stato", "status"])
    return str(s).lower().strip() if s is not None else None


def _id_richiesta(risposta):
    piatto = campi.appiattisci(risposta)
    return campi.cerca(piatto, ["id", "documentId", "document_id", "idRichiesta", "request_id"])


def attendi(client, cfg, base, id_richiesta, timeout=600, intervallo=10):
    """Interroga lo stato della richiesta finche' non e' completata o fallita.

    Il polling non consuma crediti: si paga la richiesta, non le letture.
    """
    scadenza = time.time() + timeout
    ultima = None
    while time.time() < scadenza:
        ultima = client.chiama("GET", f"{base}/{id_richiesta}", a_pagamento=False, usa_cache=False)
        st = _stato(ultima)
        if st in STATI_OK:
            return ultima
        if st in STATI_KO:
            raise RuntimeError(f"Richiesta {id_richiesta} fallita (stato: {st})")
        print(f"  ... in lavorazione ({st or 'stato ignoto'}), riprovo tra {intervallo}s")
        time.sleep(intervallo)
    raise TimeoutError(f"Richiesta {id_richiesta}: nessun esito entro {timeout}s")


def riclassificato(client, cfg, identificativo, anno=None, timeout=600, intervallo=10):
    """Bilancio riclassificato in JSON: la fonte migliore per il benchmark.

    Restituisce (dati, da_cache). Se il file esiste gia' non spende nulla.
    """
    ident = normalizza_id(identificativo)
    percorso = _archivio(cfg, "riclassificato", ident, anno)
    if percorso.exists():
        return json.loads(percorso.read_text(encoding="utf-8")), True

    base = url(cfg, "riclassificato")
    corpo = {"cf_piva_id": ident}
    if anno:
        corpo["anno_chiusura"] = int(anno)
    creata = client.chiama("POST", base, body=corpo, a_pagamento=True, usa_cache=False)
    esito = creata
    if _stato(creata) not in STATI_OK:
        rid = _id_richiesta(creata)
        if not rid:
            raise RuntimeError(f"Nessun id nella risposta: {json.dumps(creata)[:400]}")
        esito = attendi(client, cfg, base, rid, timeout, intervallo)
    percorso.write_text(json.dumps(esito, ensure_ascii=False, indent=1), encoding="utf-8")
    return esito, False


def ottico(client, cfg, identificativo, anno=None, timeout=900, intervallo=15):
    """Bilancio ottico: il PDF depositato in camera di commercio, con allegati.

    Serve quando il riclassificato non copre la societa' o l'anno; non e'
    direttamente elaborabile, va letto o estratto a parte.
    """
    ident = normalizza_id(identificativo)
    percorso = _archivio(cfg, "ottico", ident, anno)
    if percorso.exists():
        esito = json.loads(percorso.read_text(encoding="utf-8"))
    else:
        base = url(cfg, "visure", "bilancio_ottico")
        corpo = {"cf_piva_id": ident}
        if anno:
            corpo["anno_chiusura"] = int(anno)
        creata = client.chiama("POST", base, body=corpo, a_pagamento=True, usa_cache=False)
        rid = _id_richiesta(creata)
        esito = creata if _stato(creata) in STATI_OK else attendi(
            client, cfg, base, rid, timeout, intervallo)
        percorso.write_text(json.dumps(esito, ensure_ascii=False, indent=1), encoding="utf-8")

    rid = _id_richiesta(esito)
    allegati = client.chiama("GET", url(cfg, "visure", "allegati", id=rid),
                             a_pagamento=False, usa_cache=True)
    scaricati = []
    cartella = Path(cfg["percorsi"]["dati"]) / "bilanci" / "pdf"
    for i, a in enumerate(campi.elenco(allegati)):
        piatto = campi.appiattisci(a)
        link = campi.cerca(piatto, ["url", "link", "download_url", "file_url"])
        if not link:
            continue
        nome = campi.cerca(piatto, ["filename", "file_name", "nome"]) or f"{ident}_{anno or 'ultimo'}_{i}.pdf"
        scaricati.append(client.scarica_file(link, cartella / str(nome)))
    return esito, scaricati


def da_anagrafica(scheda_impresa):
    """Fallback gratuito: usa i dati di bilancio gia' presenti nella scheda advance.

    Copre solo fatturato e dipendenti, ma permette un primo posizionamento
    dimensionale senza acquistare un bilancio per ogni peer.
    """
    anno = scheda_impresa.get("anno_fatturato")
    return {
        "anno": int(anno) if anno else None,
        "ricavi": scheda_impresa.get("fatturato"),
        "dipendenti": scheda_impresa.get("dipendenti"),
        "fonte": "anagrafica",
    }
