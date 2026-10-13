# Guida passo passo — benchmark di settore

Procedura completa, dal computer vuoto al report finito. L'esempio usa **Lodotruck S.r.l.**
(P.IVA `03242670168`, commercio di veicoli industriali): sostituisci la partita IVA con
quella che ti serve.

Convenzione: dove i comandi cambiano tra sistemi trovi due righe, **macOS/Linux** e
**Windows (PowerShell)**.

---

## Passo 1 — Prendi il codice

Se hai `git`:

```bash
git clone https://github.com/MinutiMarco/StudioCDG.git
cd StudioCDG
git checkout claude/openapi-bilanci-benchmark-amad3f
cd bilanci
```

Se non hai git: apri la pagina del branch su GitHub, **Code → Download ZIP**, scompatta e
entra nella cartella `bilanci`.

## Passo 2 — Verifica Python e installa l'unica dipendenza

```bash
python3 --version        # macOS/Linux — serve 3.11 o superiore
python  --version        # Windows
```

Se manca, si scarica da [python.org/downloads](https://www.python.org/downloads/) (su Windows
spunta **«Add Python to PATH»** durante l'installazione).

```bash
pip install -r requirements.txt
```

## Passo 3 — Prova a vuoto (nessun credito speso)

Prima di collegare l'account, verifica che la catena funzioni:

```bash
python3 demo.py          # Windows: python demo.py
```

Genera `esempio/benchmark_demo.html` con dati inventati. Aprilo con doppio clic: è
esattamente la forma che avrà il report vero. Se questo funziona, il resto è solo questione
di credenziali.

Facoltativo, per sicurezza: `python3 test_bilanci.py` → deve finire con `OK`.

## Passo 4 — Attiva i servizi e prendi il token su Openapi

Entra in [console.openapi.com](https://console.openapi.com) e verifica che siano **attivi**:

| Servizio | Serve per |
|---|---|
| **Imprese** (o *Company*) — ricerca avanzata | trovare la società e i concorrenti per ATECO e provincia |
| **Bilancio riclassificato** | il bilancio in JSON, da cui si calcolano gli indici |
| **Bilancio ottico** *(facoltativo)* | il PDF depositato, quando il riclassificato non copre l'anno |

Poi genera il **token**: nella console c'è la sezione dei token/OAuth, dove scegli gli
**scope**, cioè quali chiamate il token può fare. Servono questi:

```
GET:imprese.openapi.it/advance
GET:imprese.openapi.it/base
POST:visurecamerali.openapi.it/bilancio-riclassificato
GET:visurecamerali.openapi.it/bilancio-riclassificato
```

Copia il token e mettilo nell'ambiente (**non** incollarlo in chat, e non finisce su git):

```bash
export OPENAPI_TOKEN="incolla-qui-il-token"                  # macOS/Linux
$env:OPENAPI_TOKEN = "incolla-qui-il-token"                  # Windows PowerShell
```

Va rifatto a ogni nuova finestra del terminale. In alternativa, copia
`config.example.toml` in `config.toml` e scrivilo lì una volta per tutte: `config.toml` è
già escluso da git.

## Passo 5 — Prima chiamata vera: la scheda della società (1 credito)

```bash
python3 cli.py scheda 03242670168
```

Ti stampa denominazione, **codice ATECO**, sede, forma giuridica, fatturato e dipendenti.

**Guarda l'ATECO**: è il perno di tutto il resto. Per Lodotruck ci si aspetta `45.19.01`
(commercio all'ingrosso e al dettaglio di altri autoveicoli). Se esce un codice diverso,
il campione va costruito su quello.

Se qui prendi un errore, vai in fondo, alla sezione **Se qualcosa non torna**.

## Passo 6 — Dimensiona il campione (gratis)

```bash
python3 cli.py stima 03242670168 --ambito nord --cifre-ateco 6
```

Non spende crediti: usa il conteggio `dry_run`. Ti mostra quante imprese ci sono con lo
stesso ATECO a 6, 3 e 2 cifre, e poi il dettaglio **provincia per provincia** delle 47
province del Nord, con il totale.

Come leggerlo:

- **meno di 15 imprese** → il settore è troppo stretto: rilancia con `--cifre-ateco 4`,
  oppure togli il filtro dimensionale con `--banda 0`;
- **più di 150** → è troppo largo: stringi con `--banda 2`, o passa a `--ambito nordovest`;
- **tra 20 e 80** → sei nel punto giusto.

## Passo 7 — Scarica il campione di concorrenti

```bash
python3 cli.py peer 03242670168 --ambito nord --cifre-ateco 6 --banda 3 --limite 30 --conferma
```

Senza `--conferma` il comando ti dice solo cosa farebbe e quanto costa: usalo come prova.
Con `--conferma` esegue la ricerca, provincia per provincia dalla più popolata, e salva
tutto in `dati/peer.json`. A schermo vedi scorrere le imprese trovate.

**Alternativa — i concorrenti li scegli tu.** Se conosci già i nomi, scrivi le partite IVA
in un file di testo (una per riga, il nome dopo `;` è facoltativo) e salta la ricerca:

```bash
python3 cli.py peer 03242670168 --da-file esempio/peer_veicoli_industriali.csv --conferma
```

Il file `esempio/peer_veicoli_industriali.csv` contiene già tre comparabili del settore
veicoli industriali: puoi aggiungerne altri con un editor di testo.

**Passaggio che vale la pena fare**: apri `dati/peer.json` e scorri i nomi. Se dentro ci
sono officine, rivenditori di usato o filiali di costruttori, non sono concorrenti veri:
copia le partite IVA buone in un file tuo e rilancia `peer --da-file`. Il campione pulito
vale più di un campione numeroso.

## Passo 8 — Scarica i bilanci (è qui che si spende)

```bash
python3 cli.py scarica --anno 2024 --max-crediti 35 --conferma
```

Un bilancio per impresa, più quello della società analizzata. `--max-crediti` è il freno: al
raggiungimento del tetto si ferma da solo. Il comando stampa gli esercizi trovati per
ciascuna impresa e salva tutto in `dati/`.

Se si interrompe, **rilancialo**: i bilanci già scaricati sono su disco e non si ripagano.

Se per il 2024 molte imprese risultano senza bilancio, prova `--anno 2023`: i bilanci
vengono depositati tra la metà e la fine dell'anno successivo, quindi l'ultimo esercizio
disponibile è spesso quello di due anni prima.

## Passo 9 — Genera il benchmark

```bash
python3 cli.py benchmark --anno 2024
```

Non costa nulla: lavora sui dati già scaricati. Produce in `output/`:

- `benchmark_2024.html` — il report da aprire con doppio clic e da allegare alla relazione;
- `benchmark_2024.csv` — indice per indice: società, quartili, percentile, lettura;
- `imprese_2024.csv` — il dettaglio impresa per impresa, per i tuoi controlli in Excel.

## Passo 10 — Controlla prima di usarlo

Tre verifiche che evitano figuracce:

1. **La colonna `N`** di ogni riga del report: se un indice è calcolato su 4 imprese su 30,
   quel quartile non significa niente. Le PMI che depositano in forma abbreviata non
   espongono il dettaglio per ricostruire EBITDA e costo del lavoro.
2. **Apri due o tre concorrenti del campione** e chiediti se li metteresti davvero nella
   stessa slide della società analizzata.
3. **Dichiara i criteri** nella relazione: ATECO, ambito geografico, banda dimensionale,
   esercizio. Sono già scritti nella scheda «Criteri del campione» in cima al report.

Per il commercio di veicoli industriali, in particolare: ROE e utile su ricavi saranno
minuscoli per tutti — è la fisiologia del settore, non un problema della società. Le righe
che parlano davvero sono **EBITDA margin, giorni di magazzino, giorni di credito,
PFN/EBITDA e ricavi per dipendente**.

---

## Se qualcosa non torna

| Sintomo | Causa e rimedio |
|---|---|
| `401` o `403` | Token assente, scaduto o senza lo scope di quella chiamata. Rigeneralo nella console con gli scope del Passo 4. |
| `404` su una chiamata | Il percorso dell'endpoint del tuo piano è diverso. Aprilo nella documentazione del tuo account e correggi la sezione `[endpoint]` di `config.toml`: il codice legge da lì. |
| «Nessuna impresa trovata» sulla `scheda` | Partita IVA errata, oppure la società è cessata: prova `--base`. |
| Il report ha molte celle `—` | I nomi dei campi nel tuo payload sono diversi da quelli previsti. Lancia `python3 cli.py ispeziona dati/bilanci/riclassificato/<file>.json --filtro patrimonio`, leggi il nome vero e aggiungilo in `mappa_campi.json`. Poi rilancia `scarica`: i bilanci sono già in locale, non si ripagano. |
| `command not found: python3` | Su Windows il comando è `python`. |
| Ho speso più del previsto | Metti sempre `--max-crediti`. I conteggi (`stima`) sono gratuiti, i bilanci no: il costo è quasi tutto lì, un bilancio per concorrente. |

## Riepilogo dei comandi

```bash
export OPENAPI_TOKEN="..."                                                   # una volta per terminale
python3 cli.py scheda    03242670168                                         # 1 credito
python3 cli.py stima     03242670168 --ambito nord --cifre-ateco 6           # gratis
python3 cli.py peer      03242670168 --ambito nord --cifre-ateco 6 --banda 3 --limite 30 --conferma
python3 cli.py scarica   --anno 2024 --max-crediti 35 --conferma
python3 cli.py benchmark --anno 2024
```

---

## Riepilogo per Windows (PowerShell)

Apri **Start → PowerShell → Windows PowerShell** e incolla una riga alla volta, Invio dopo
ciascuna. Su Windows il comando di Python è `python`, non `python3`.

```powershell
cd ~\Documents
git clone https://github.com/MinutiMarco/StudioCDG.git
cd StudioCDG
git checkout claude/openapi-bilanci-benchmark-amad3f
cd bilanci

python --version                     # deve dire 3.11 o superiore
pip install -r requirements.txt
python demo.py                       # prova a vuoto, nessun credito

$env:OPENAPI_TOKEN = "incolla-qui-il-token"     # da rifare a ogni finestra nuova

python cli.py scheda    03242670168
python cli.py stima     03242670168 --ambito nord --cifre-ateco 6
python cli.py peer      03242670168 --ambito nord --cifre-ateco 6 --banda 3 --limite 30 --conferma
python cli.py scarica   --anno 2024 --max-crediti 35 --conferma
python cli.py benchmark --anno 2024
```

Per aprire il report finito senza cercarlo in Esplora file:

```powershell
start output\benchmark_2024.html
```

Se `git` non è installato, PowerShell risponde *«git : Termine 'git' non riconosciuto…»*:
installalo da [git-scm.com/download/win](https://git-scm.com/download/win) (va bene tutto
predefinito, poi **chiudi e riapri PowerShell**), oppure scarica lo ZIP del branch da GitHub.

Se digitando `python` si apre il Microsoft Store, Python non c'è: installalo da
[python.org/downloads](https://www.python.org/downloads/) ricordandoti di spuntare
**«Add python.exe to PATH»** nella prima schermata.
