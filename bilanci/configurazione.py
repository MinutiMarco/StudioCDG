"""Caricamento della configurazione (endpoint, credenziali, parametri di ricerca).

Gli URL degli endpoint stanno nel file di configurazione, non nel codice: il
piano sottoscritto su console.openapi.com determina quali servizi sono attivi e
con quale percorso. Se una chiamata risponde 404, si corregge qui.
"""
import os, tomllib
from pathlib import Path

PREDEFINITI = {
    "auth": {
        # Token generato in console (consigliato) oppure username+apikey per coniarlo.
        "token": "", "username": "", "apikey": "",
        "scopes": [
            "GET:imprese.openapi.it/advance",
            "GET:imprese.openapi.it/base",
        ],
    },
    "endpoint": {
        # Servizio "Imprese": anagrafica, ricerca avanzata, dati di bilancio sintetici.
        "imprese": "https://imprese.openapi.it",
        "ricerca_base": "/base",          # GET /base/{piva|cf}  e  GET /base?denominazione=...
        "ricerca_advance": "/advance",    # GET /advance/{piva}  e  GET /advance?codice_ateco=...
        "chiuse": "/closed",              # GET /closed/{piva}
        # Servizio "Visure camerali": bilancio ottico (PDF depositato) e allegati.
        "visure": "https://visurecamerali.openapi.it",
        "bilancio_ottico": "/bilancio-ottico",
        "allegati": "/bilancio-ottico/{id}/allegati",
        # Servizio "Bilancio riclassificato" (JSON con schemi riclassificati e indici).
        "riclassificato": "https://visurecamerali.openapi.it/bilancio-riclassificato",
    },
    "ricerca": {
        "limite_peer": 40,        # quante societa' confrontabili al massimo
        "pagina": 20,             # dimensione pagina della ricerca
        "solo_attive": True,
        "max_crediti": 0,         # 0 = nessun tetto; consigliato impostarlo
    },
    "percorsi": {
        "cache": "cache",
        "dati": "dati",
        "output": "output",
    },
}


def _fondi(base, sopra):
    out = {k: dict(v) if isinstance(v, dict) else v for k, v in base.items()}
    for k, v in (sopra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _fondi(out[k], v)
        else:
            out[k] = v
    return out


def carica(percorso="config.toml"):
    cfg = _fondi(PREDEFINITI, {})
    p = Path(percorso)
    if p.exists():
        cfg = _fondi(cfg, tomllib.loads(p.read_text(encoding="utf-8")))
    # le variabili d'ambiente vincono sempre: cosi' le credenziali non finiscono su git
    for chiave, env in (("token", "OPENAPI_TOKEN"), ("username", "OPENAPI_USERNAME"),
                        ("apikey", "OPENAPI_APIKEY")):
        if os.environ.get(env):
            cfg["auth"][chiave] = os.environ[env]
    return cfg


def url(cfg, servizio, percorso_chiave=None, **fmt):
    base = cfg["endpoint"][servizio].rstrip("/")
    if percorso_chiave is None:
        return base
    coda = cfg["endpoint"][percorso_chiave]
    if fmt:
        coda = coda.format(**fmt)
    return base + coda
