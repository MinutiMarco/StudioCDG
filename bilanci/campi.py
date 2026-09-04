"""Estrazione tollerante di campi da JSON di struttura non garantita.

Le risposte Openapi cambiano forma tra servizi e tra piani (a volte i dati sono
in `data`, a volte in `data[0]`, i nomi variano tra italiano e inglese). Invece
di inseguire lo schema, si appiattisce il JSON e si cercano i campi per alias.
"""
import re, unicodedata


def appiattisci(oggetto, prefisso=""):
    """{'a': {'b': [1,2]}} -> {'a.b.0': 1, 'a.b.1': 2}"""
    piatto = {}
    if isinstance(oggetto, dict):
        for k, v in oggetto.items():
            piatto.update(appiattisci(v, f"{prefisso}.{k}" if prefisso else str(k)))
    elif isinstance(oggetto, list):
        for i, v in enumerate(oggetto):
            piatto.update(appiattisci(v, f"{prefisso}.{i}" if prefisso else str(i)))
    else:
        piatto[prefisso] = oggetto
    return piatto


def _slug(testo):
    t = unicodedata.normalize("NFKD", str(testo)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


def cerca(piatto, alias, solo_numerico=False):
    """Primo valore la cui chiave finale corrisponde a uno degli alias.

    Il confronto e' su slug: `Valore.della.produzione` == `valore_della_produzione`.
    L'ordine degli alias e' l'ordine di preferenza.
    """
    indice = {}
    for chiave, valore in piatto.items():
        foglia = _slug(chiave.split(".")[-1])
        indice.setdefault(foglia, []).append((chiave, valore))
    for a in alias:
        for chiave, valore in indice.get(_slug(a), []):
            if valore in (None, "", []):
                continue
            if solo_numerico:
                n = numero(valore)
                if n is not None:
                    return n
                continue
            return valore
    return None


def numero(valore):
    """Converte in float importi scritti come '1.234.567,89', '1234567.89', 1234567."""
    if valore is None or isinstance(valore, bool):
        return None
    if isinstance(valore, (int, float)):
        return float(valore)
    s = str(valore).strip().replace("€", "").replace(" ", "")
    if not s:
        return None
    negativo = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    if "," in s and "." in s:
        # l'ultimo separatore che compare e' quello decimale
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif re.fullmatch(r"-?[1-9]\d{0,2}(\.\d{3})+", s):
        s = s.replace(".", "")        # 8.400 / 1.234.567 -> migliaia all'italiana
    elif re.fullmatch(r"-?[1-9]\d{0,2}(,\d{3})+", s):
        s = s.replace(",", "")        # 8,400 -> migliaia all'inglese
    # nota: "0.085" resta 0.085, non 85: lo zero iniziale esclude i migliaia
    elif "," in s:
        s = s.replace(",", ".")
    try:
        n = float(s)
    except ValueError:
        return None
    return -n if negativo else n


def contenuto(risposta):
    """Estrae il payload utile: molte risposte incapsulano tutto in `data`."""
    if isinstance(risposta, dict):
        for chiave in ("data", "result", "results"):
            if chiave in risposta and risposta[chiave] not in (None, {}, []):
                return risposta[chiave]
    return risposta


def elenco(risposta):
    """Normalizza la risposta a lista di record."""
    dati = contenuto(risposta)
    if isinstance(dati, list):
        return dati
    if isinstance(dati, dict):
        for chiave in ("items", "records", "imprese", "companies"):
            if isinstance(dati.get(chiave), list):
                return dati[chiave]
        return [dati]
    return []
