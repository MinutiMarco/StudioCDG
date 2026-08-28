# Riassunto — *Il controllo di gestione* (Busco, Giovannoni, Riccaboni, V ed., Wolters Kluwer)

Riassunto ragionato dei 39 capitoli con schemi visivi, in due formati:

- **`riassunto.docx`** — documento Word con indice, un capitolo per sezione, diagrammi e tabelle
- **`mappa.html`** — mappa concettuale navigabile del libro e dei singoli capitoli

## Struttura del repository

| Percorso | Contenuto |
|---|---|
| `riassunti/capNN.md` | riassunto di ciascun capitolo, con blocchi ```schema``` che descrivono i diagrammi |
| `manifest.tsv` | mappatura capitolo → file PDF di origine su Drive |
| `clean.py` | normalizzazione del testo estratto (accenti, marker di pagina, header/footer) |
| `view.py` | lettura del testo ripulito da header e footer correnti |
| `build_*.py` | generazione degli schemi, del Word e della mappa HTML |

I testi sorgente (`testi/`) non sono versionati: derivano dai PDF personali dell'utente.
