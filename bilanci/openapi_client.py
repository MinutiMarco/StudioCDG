"""Client HTTP per le API Openapi (openapi.com / *.openapi.it).

Tre preoccupazioni, tutte a pagamento se sbagliate:
  1. autenticazione  -> token Bearer (generato in console o coniato via OAuth)
  2. costo           -> ogni chiamata che consuma crediti passa da `_spendi`
  3. ripetizione     -> cache su disco: un bilancio pagato non si ripaga mai due volte
"""
import base64, hashlib, json, os, time, urllib.parse
from pathlib import Path

import requests

OAUTH_TOKEN_URL = "https://oauth.openapi.it/token"
UA = "StudioCDG-bilanci/1.0"


class ErroreOpenapi(RuntimeError):
    pass


class BudgetEsaurito(ErroreOpenapi):
    pass


class Client:
    """Wrapper sottile su requests con token, cache, budget e backoff."""

    def __init__(self, token=None, username=None, apikey=None, cache_dir="cache",
                 max_crediti=0, timeout=60, verbose=True):
        self.token = token or os.environ.get("OPENAPI_TOKEN")
        self.username = username or os.environ.get("OPENAPI_USERNAME")
        self.apikey = apikey or os.environ.get("OPENAPI_APIKEY")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_crediti = int(max_crediti)      # numero massimo di chiamate a pagamento
        self.crediti_spesi = 0
        self.timeout = timeout
        self.verbose = verbose
        self.sess = requests.Session()
        self.sess.headers.update({"User-Agent": UA, "Accept": "application/json"})

    # ---------- autenticazione ----------

    def assicura_token(self, scopes=None, ttl=86400):
        """Restituisce un token Bearer valido.

        Preferenza: token gia' pronto (env OPENAPI_TOKEN o config). In alternativa
        lo conia via OAuth con username + apikey; gli scope vanno indicati nella
        forma documentata da Openapi, es. "GET:imprese.openapi.it/advance".
        """
        if self.token:
            return self.token
        if not (self.username and self.apikey):
            raise ErroreOpenapi(
                "Nessun token: imposta OPENAPI_TOKEN oppure OPENAPI_USERNAME + OPENAPI_APIKEY."
            )
        basic = base64.b64encode(f"{self.username}:{self.apikey}".encode()).decode()
        r = self.sess.post(
            OAUTH_TOKEN_URL,
            headers={"Authorization": f"Basic {basic}", "Content-Type": "application/json"},
            json={"scopes": scopes or [], "ttl": ttl},
            timeout=self.timeout,
        )
        if r.status_code >= 400:
            raise ErroreOpenapi(f"OAuth {r.status_code}: {r.text[:400]}")
        dati = r.json()
        tok = dati.get("token") or dati.get("data", {}).get("token")
        if not tok:
            raise ErroreOpenapi(f"Token assente nella risposta OAuth: {json.dumps(dati)[:400]}")
        self.token = tok
        return tok

    # ---------- cache ----------

    def _chiave(self, metodo, url, params, body):
        crudo = json.dumps([metodo, url, params or {}, body or {}], sort_keys=True, default=str)
        return hashlib.sha1(crudo.encode()).hexdigest()

    def _percorso_cache(self, chiave):
        return self.cache_dir / f"{chiave}.json"

    def leggi_cache(self, metodo, url, params=None, body=None):
        p = self._percorso_cache(self._chiave(metodo, url, params, body))
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
        return None

    def _scrivi_cache(self, metodo, url, params, body, dati):
        p = self._percorso_cache(self._chiave(metodo, url, params, body))
        p.write_text(json.dumps(dati, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---------- budget ----------

    def _spendi(self, descrizione):
        if self.max_crediti and self.crediti_spesi >= self.max_crediti:
            raise BudgetEsaurito(
                f"Budget di {self.max_crediti} chiamate a pagamento esaurito ({descrizione})."
            )
        self.crediti_spesi += 1

    # ---------- richieste ----------

    def chiama(self, metodo, url, params=None, body=None, a_pagamento=False,
               usa_cache=True, tentativi=4):
        """Esegue la chiamata. `a_pagamento=True` scala il budget locale."""
        if usa_cache:
            cached = self.leggi_cache(metodo, url, params, body)
            if cached is not None:
                if self.verbose:
                    print(f"  [cache] {metodo} {url}")
                return cached
        if a_pagamento:
            self._spendi(f"{metodo} {url}")
        headers = {"Authorization": f"Bearer {self.assicura_token()}"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        attesa = 2
        for tentativo in range(1, tentativi + 1):
            if self.verbose:
                q = "?" + urllib.parse.urlencode(params, doseq=True) if params else ""
                print(f"  [http] {metodo} {url}{q}")
            try:
                r = self.sess.request(metodo, url, params=params, json=body,
                                      headers=headers, timeout=self.timeout)
            except requests.RequestException as e:
                if tentativo == tentativi:
                    raise ErroreOpenapi(f"Rete: {e}") from e
                time.sleep(attesa); attesa *= 2
                continue
            if r.status_code in (429, 500, 502, 503, 504) and tentativo < tentativi:
                time.sleep(attesa); attesa *= 2
                continue
            if r.status_code >= 400:
                raise ErroreOpenapi(f"{metodo} {url} -> {r.status_code}: {r.text[:600]}")
            try:
                dati = r.json()
            except ValueError:
                dati = {"_raw": r.text}
            if usa_cache:
                self._scrivi_cache(metodo, url, params, body, dati)
            return dati
        raise ErroreOpenapi(f"{metodo} {url}: tentativi esauriti")

    def scarica_file(self, url, destinazione, a_pagamento=False):
        """Scarica un allegato (PDF/XBRL) saltando la cache JSON."""
        destinazione = Path(destinazione)
        if destinazione.exists() and destinazione.stat().st_size > 0:
            if self.verbose:
                print(f"  [cache] {destinazione.name}")
            return destinazione
        if a_pagamento:
            self._spendi(f"GET {url}")
        r = self.sess.get(url, headers={"Authorization": f"Bearer {self.assicura_token()}"},
                          timeout=self.timeout, stream=True)
        if r.status_code >= 400:
            raise ErroreOpenapi(f"GET {url} -> {r.status_code}: {r.text[:300]}")
        destinazione.parent.mkdir(parents=True, exist_ok=True)
        with open(destinazione, "wb") as f:
            for chunk in r.iter_content(65536):
                f.write(chunk)
        return destinazione
