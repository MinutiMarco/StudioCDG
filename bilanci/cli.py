#!/usr/bin/env python3
"""Riga di comando del benchmark di settore su dati Openapi.

Flusso tipico:
    python3 cli.py stima      12345678901          # gratis: quante imprese comparabili
    python3 cli.py peer       12345678901          # scarica il campione
    python3 cli.py scarica    --max-crediti 30     # bilanci riclassificati
    python3 cli.py benchmark  --anno 2024          # CSV + report HTML
"""
import argparse, json, sys
from pathlib import Path

import bilanci as mod_bilanci
import benchmark as mod_benchmark
import campi
import configurazione
import imprese
import indicatori
import report
from openapi_client import BudgetEsaurito, Client, ErroreOpenapi


# ---------- stato su disco ----------

def _file(cfg, nome):
    d = Path(cfg["percorsi"]["dati"]); d.mkdir(parents=True, exist_ok=True)
    return d / nome


def _leggi(cfg, nome, predefinito=None):
    p = _file(cfg, nome)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else predefinito


def _scrivi(cfg, nome, dati):
    p = _file(cfg, nome)
    p.write_text(json.dumps(dati, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def _client(cfg, args):
    return Client(
        token=cfg["auth"]["token"] or None,
        username=cfg["auth"]["username"] or None,
        apikey=cfg["auth"]["apikey"] or None,
        cache_dir=cfg["percorsi"]["cache"],
        max_crediti=getattr(args, "max_crediti", None) or cfg["ricerca"]["max_crediti"],
        verbose=not getattr(args, "silenzioso", False),
    )


# ---------- comandi ----------

def cmd_scheda(cfg, args):
    cl = _client(cfg, args)
    scheda, grezzo = imprese.scheda(cl, cfg, args.identificativo, avanzata=not args.base)
    if not scheda:
        print("Nessuna impresa trovata."); return 1
    scheda["id"] = imprese.normalizza_id(args.identificativo)
    _scrivi(cfg, "target.json", {"scheda": scheda, "grezzo": grezzo})
    for k, v in scheda.items():
        if v not in (None, ""):
            print(f"  {k:22} {v}")
    return 0


def _target(cfg, args):
    salvato = _leggi(cfg, "target.json")
    if args.identificativo:
        cl = _client(cfg, args)
        scheda, grezzo = imprese.scheda(cl, cfg, args.identificativo, avanzata=True)
        if not scheda:
            raise SystemExit("Impresa non trovata.")
        scheda["id"] = imprese.normalizza_id(args.identificativo)
        _scrivi(cfg, "target.json", {"scheda": scheda, "grezzo": grezzo})
        return scheda
    if not salvato:
        raise SystemExit("Nessun target salvato: indica una partita IVA.")
    return salvato["scheda"]


def _filtri(target, args):
    banda = None if args.banda == 0 else (1 / args.banda, args.banda)
    return imprese.filtri_da_target(target, cifre_ateco=args.cifre_ateco,
                                    ambito=args.ambito, banda_fatturato=banda)


def cmd_stima(cfg, args):
    """Conteggio gratuito: dimensiona il campione prima di spendere crediti."""
    target = _target(cfg, args)
    cl = _client(cfg, args)
    print(f"\nSocietà: {target.get('denominazione')} — ATECO {target.get('ateco')} — "
          f"fatturato {target.get('fatturato')}")
    for cifre in (args.cifre_ateco, 3, 2):
        a = argparse.Namespace(**vars(args)); a.cifre_ateco = cifre
        f = _filtri(target, a)
        n = imprese.conta(cl, cfg, f)
        print(f"  ATECO {cifre} cifre {f.get('codice_ateco','—'):>8} · {args.ambito:11} · "
              f"imprese: {n if n is not None else 'n/d'}   filtri={f}")
    print("\nIl conteggio (dry_run) non consuma crediti. La ricerca vera sì: "
          f"circa {args.limite} record.")
    return 0


def cmd_peer(cfg, args):
    target = _target(cfg, args)
    cl = _client(cfg, args)
    filtri = _filtri(target, args)
    n = imprese.conta(cl, cfg, filtri)
    print(f"Imprese che soddisfano i filtri: {n if n is not None else 'n/d'} — ne scarico {args.limite}")
    if not args.conferma:
        print("Aggiungi --conferma per eseguire la ricerca (consuma crediti).")
        return 0
    peer = imprese.cerca_peer(cl, cfg, filtri, limite=args.limite,
                              pagina=cfg["ricerca"]["pagina"],
                              escludi=[target.get("piva"), target.get("cf"), target.get("id")])
    _scrivi(cfg, "peer.json", {"filtri": filtri, "peer": peer})
    print(f"Salvate {len(peer)} imprese in {_file(cfg,'peer.json')} "
          f"({cl.crediti_spesi} chiamate a pagamento).")
    for p in peer[:15]:
        print(f"  · {p.get('denominazione')} — {p.get('provincia')} — fatt. {p.get('fatturato')}")
    return 0


def cmd_scarica(cfg, args):
    """Scarica i bilanci riclassificati di target e peer, con tetto di spesa."""
    stato = _leggi(cfg, "peer.json", {"peer": []})
    target = _target(cfg, args)
    elenco = ([target] if not args.solo_peer else []) + stato["peer"]
    if args.limite:
        elenco = elenco[: args.limite + (0 if args.solo_peer else 1)]
    alias = indicatori.carica_alias()
    cl = _client(cfg, args)
    indici = _leggi(cfg, "indici.json", {})
    if not args.conferma:
        print(f"Da scaricare: {len(elenco)} bilanci. Aggiungi --conferma per procedere "
              f"(ogni bilancio consuma crediti).")
        return 0

    for i, imp in enumerate(elenco, 1):
        ident = imp.get("id") or imprese.normalizza_id(imp.get("piva") or imp.get("cf") or "")
        if not ident:
            continue
        if ident in indici and not args.riscarica:
            print(f"[{i}/{len(elenco)}] {imp.get('denominazione')} — già presente"); continue
        print(f"[{i}/{len(elenco)}] {imp.get('denominazione') or ident}")
        try:
            esito, da_cache = mod_bilanci.riclassificato(cl, cfg, ident, anno=args.anno)
        except BudgetEsaurito as e:
            print(f"  ! {e}"); break
        except (ErroreOpenapi, RuntimeError, TimeoutError) as e:
            print(f"  ! bilancio non disponibile: {str(e)[:180]}")
            if args.ripiego:
                base = mod_bilanci.da_anagrafica(imp)
                if base["anno"] and base["ricavi"]:
                    indici[ident] = {str(base["anno"]): indicatori.indici(base)}
                    print("    ripiego sui dati anagrafici (solo ricavi e dipendenti)")
            continue
        per_anno = indicatori.voci(esito, alias)
        indici[ident] = {str(a): indicatori.indici(v) for a, v in per_anno.items()}
        print(f"  esercizi: {sorted(per_anno)}{' [da cache]' if da_cache else ''}")
        _scrivi(cfg, "indici.json", indici)

    _scrivi(cfg, "indici.json", indici)
    print(f"\nIndici salvati per {len(indici)} imprese. Chiamate a pagamento in questa sessione: "
          f"{cl.crediti_spesi}.")
    return 0


def cmd_benchmark(cfg, args):
    indici = _leggi(cfg, "indici.json", {})
    if not indici:
        print("Nessun indice: esegui prima `scarica`."); return 1
    target = _target(cfg, args)
    id_target = target.get("id") or imprese.normalizza_id(target.get("piva") or "")
    stato_peer = _leggi(cfg, "peer.json", {"peer": [], "filtri": {}})

    anni = sorted({int(a) for v in indici.values() for a in v}, reverse=True)
    anno = args.anno or (anni[0] if anni else None)
    if anno is None:
        print("Nessun esercizio disponibile."); return 1

    ind_target = indici.get(id_target, {}).get(str(anno))
    ind_peer = [v[str(anno)] for k, v in indici.items() if k != id_target and str(anno) in v]
    if not ind_peer:
        print(f"Nessun peer con bilancio {anno}. Anni disponibili: {anni}"); return 1

    righe = mod_benchmark.confronta(ind_target or {}, ind_peer)
    csv_out = mod_benchmark.esporta_csv(
        righe, Path(cfg["percorsi"]["output"]) / f"benchmark_{anno}.csv",
        colonne=["etichetta", "target", "percentile", "giudizio", "n", "min", "q1",
                 "mediana", "q3", "max", "media", "dev_std"])

    dettaglio = []
    for ident, per_anno in indici.items():
        riga = {"id": ident, "target": ident == id_target}
        riga.update({k: v for k, v in (per_anno.get(str(anno)) or {}).items()})
        dettaglio.append(riga)
    mod_benchmark.esporta_csv(dettaglio, Path(cfg["percorsi"]["output"]) / f"imprese_{anno}.csv")

    peer_con_bilancio = [p for p in stato_peer["peer"] if p.get("id") in indici]
    meta = {
        "Esercizio di riferimento": anno,
        "Imprese nel campione": len(ind_peer),
        "Filtri di ricerca": ", ".join(f"{k}={v}" for k, v in stato_peer.get("filtri", {}).items()) or "—",
        "Fonte bilanci": "bilancio riclassificato Openapi",
    }
    html_out = report.genera(target, righe, peer_con_bilancio or stato_peer["peer"], meta,
                             Path(cfg["percorsi"]["output"]) / f"benchmark_{anno}.html")

    print(f"\nBenchmark esercizio {anno} — {len(ind_peer)} imprese di confronto\n")
    for r in righe:
        if r.get("target") is not None:
            print(f"  {r['etichetta']:34} {r['target']:>14,.1f}   mediana {r['mediana']:>14,.1f}"
                  f"   {r['giudizio']}")
    print(f"\n  CSV:  {csv_out}\n  HTML: {html_out}")
    return 0


def cmd_ispeziona(cfg, args):
    """Stampa le chiavi appiattite di una risposta grezza.

    Serve quando un campo non viene riconosciuto: si legge il nome reale e lo si
    aggiunge a `mappa_campi.json` senza toccare il codice.
    """
    dati = json.loads(Path(args.file).read_text(encoding="utf-8"))
    piatto = campi.appiattisci(dati)
    filtro = (args.filtro or "").lower()
    for k, v in sorted(piatto.items()):
        if filtro and filtro not in k.lower():
            continue
        print(f"  {k:70} = {str(v)[:60]}")
    print(f"\n{len(piatto)} chiavi.")
    return 0


def cmd_tutto(cfg, args):
    for f in (cmd_stima, cmd_peer, cmd_scarica, cmd_benchmark):
        esito = f(cfg, args)
        if esito:
            return esito
        args.identificativo = None      # i passi successivi riusano il target salvato
    return 0


# ---------- parser ----------

def principale(argv=None):
    p = argparse.ArgumentParser(description="Benchmark di settore da bilanci Openapi")
    p.add_argument("--config", default="config.toml")
    p.add_argument("--silenzioso", action="store_true")
    sub = p.add_subparsers(dest="comando", required=True)

    def comune(sp, con_identificativo=True):
        if con_identificativo:
            sp.add_argument("identificativo", nargs="?", help="partita IVA o codice fiscale")
        sp.add_argument("--cifre-ateco", type=int, default=4,
                        help="ampiezza del settore: 2 divisione, 3 gruppo, 4 classe, 6 sottocategoria")
        sp.add_argument("--ambito", choices=["nazionale", "provincia", "regione"], default="nazionale")
        sp.add_argument("--banda", type=float, default=4.0,
                        help="ampiezza dimensionale: fatturato tra 1/N e N volte quello del target (0 = nessun filtro)")
        sp.add_argument("--limite", type=int, default=40)
        sp.add_argument("--max-crediti", type=int, default=None, help="tetto di chiamate a pagamento")
        sp.add_argument("--conferma", action="store_true", help="autorizza le chiamate a pagamento")
        return sp

    s = sub.add_parser("scheda", help="anagrafica di una singola impresa")
    s.add_argument("identificativo"); s.add_argument("--base", action="store_true")
    s.add_argument("--max-crediti", type=int, default=None)
    s.set_defaults(fn=cmd_scheda)

    comune(sub.add_parser("stima", help="quante imprese comparabili (gratis)")).set_defaults(fn=cmd_stima)
    comune(sub.add_parser("peer", help="scarica il campione di confronto")).set_defaults(fn=cmd_peer)

    s = comune(sub.add_parser("scarica", help="scarica i bilanci e calcola gli indici"))
    s.add_argument("--anno", type=int, default=None, help="anno di chiusura (default: ultimo disponibile)")
    s.add_argument("--solo-peer", action="store_true")
    s.add_argument("--riscarica", action="store_true")
    s.add_argument("--ripiego", action="store_true",
                   help="se il bilancio manca, usa fatturato e dipendenti dell'anagrafica")
    s.set_defaults(fn=cmd_scarica)

    s = comune(sub.add_parser("benchmark", help="statistiche di settore e report"))
    s.add_argument("--anno", type=int, default=None)
    s.set_defaults(fn=cmd_benchmark)

    s = comune(sub.add_parser("tutto", help="stima, peer, scarica e benchmark in sequenza"))
    s.add_argument("--anno", type=int, default=None)
    s.add_argument("--solo-peer", action="store_true")
    s.add_argument("--riscarica", action="store_true")
    s.add_argument("--ripiego", action="store_true")
    s.set_defaults(fn=cmd_tutto)

    s = sub.add_parser("ispeziona", help="elenca le chiavi di una risposta salvata")
    s.add_argument("file"); s.add_argument("--filtro", default="")
    s.set_defaults(fn=cmd_ispeziona)

    args = p.parse_args(argv)
    cfg = configurazione.carica(args.config)
    try:
        return args.fn(cfg, args)
    except ErroreOpenapi as e:
        print(f"\nErrore Openapi: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(principale())
