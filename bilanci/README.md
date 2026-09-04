# Benchmark di settore da bilanci Openapi

Strumento per costruire il **confronto di mercato di una società con i suoi concorrenti**
partendo dai dati del Registro Imprese e dai bilanci depositati, scaricati via API
[Openapi](https://openapi.com).

Il flusso è: si parte dalla partita IVA della società da analizzare, si legge il suo
codice ATECO e la sua dimensione, si estrae dal Registro Imprese un campione di società
comparabili, si scaricano i bilanci, si calcolano gli indici e si guarda dove si colloca
la società nella distribuzione del settore (quartili, non medie).

## 1. Cosa serve sul lato Openapi

Sul tuo account [console.openapi.com](https://console.openapi.com) devono essere attivi:

| Servizio | A cosa serve qui | Endpoint usato |
|---|---|---|
| **Imprese / Company** (ricerca avanzata) | trovare la società e il campione di concorrenti per ATECO, provincia, fatturato, dipendenti | `GET imprese.openapi.it/advance` |
| **Bilancio riclassificato** | il bilancio in JSON, già riclassificato: è la fonte che rende possibile il calcolo degli indici | `POST/GET visurecamerali.openapi.it/bilancio-riclassificato` |
| **Bilancio ottico** *(opzionale)* | il PDF del bilancio depositato, quando il riclassificato non copre società o esercizio | `POST/GET visurecamerali.openapi.it/bilancio-ottico` |

Poi genera un **token** dalla console, con gli scope dei servizi che userai
(es. `GET:imprese.openapi.it/advance`), oppure usa `username` + `apikey` e lascia che sia
lo strumento a coniarlo via OAuth.

> I percorsi degli endpoint stanno in `config.toml`, non nel codice. Dipendono dal piano
> sottoscritto: se una chiamata risponde `404` o `401`, confronta con la documentazione del
> **tuo** account e correggi lì, senza toccare i sorgenti.

## 2. Installazione

```bash
cd bilanci
pip install -r requirements.txt          # solo `requests`
cp config.example.toml config.toml       # poi compila [auth]
```

Le credenziali si possono tenere fuori dal file, e vincono sul file:

```bash
export OPENAPI_TOKEN="il-tuo-token"
# oppure
export OPENAPI_USERNAME="..." OPENAPI_APIKEY="..."
```

`config.toml`, `cache/`, `dati/` e `output/` sono esclusi da git: contengono credenziali e
dati acquistati.

## 3. Come si usa

```bash
# 0. guarda com'è fatto il risultato, senza spendere nulla
python3 demo.py                                  # -> output/benchmark_demo.html

# 1. anagrafica della società da analizzare (1 credito)
python3 cli.py scheda 01234567890

# 2. quante concorrenti esistono, a diverse ampiezze di settore (gratis: dry_run)
python3 cli.py stima 01234567890 --ambito nazionale

# 3. scarica il campione di confronto
python3 cli.py peer 01234567890 --cifre-ateco 4 --limite 40 --banda 4 --conferma

# 4. scarica i bilanci e calcola gli indici (con tetto di spesa)
python3 cli.py scarica --anno 2024 --max-crediti 45 --conferma

# 5. statistiche di settore, CSV e report HTML
python3 cli.py benchmark --anno 2024
```

Oppure tutto in fila: `python3 cli.py tutto 01234567890 --conferma --max-crediti 60`.

Risultati in `output/`: `benchmark_<anno>.csv` (indice per indice: società, quartili,
percentile, lettura), `imprese_<anno>.csv` (il dettaglio impresa per impresa) e
`benchmark_<anno>.html`, una pagina autonoma apribile da disco e allegabile a una relazione.

## 4. Come si sceglie il campione (la parte che conta davvero)

Il numero finale vale quanto vale il gruppo di confronto. Tre leve:

- **`--cifre-ateco`** — ampiezza del settore: `2` divisione, `3` gruppo, `4` classe,
  `6` sottocategoria. Sei cifre danno concorrenti veri ma spesso pochissimi; due cifre
  danno numeri robusti ma mescolano attività diverse. Il compromesso usuale è **4**, con
  un controllo a 3 se il campione scende sotto ~15 imprese.
- **`--ambito`** — `nazionale`, `regione` o `provincia`. Il confine geografico conta se il
  mercato è locale (servizi, edilizia, distribuzione); non conta per chi esporta.
- **`--banda`** — confronta solo imprese di taglia paragonabile: con `--banda 4` entrano
  quelle con fatturato tra un quarto e quattro volte quello della società analizzata.
  Un benchmark tra una PMI e un gruppo industriale non misura la gestione, misura la taglia.
  `--banda 0` toglie il filtro dimensionale.

Usa `stima` prima di `peer`: il conteggio è gratuito e ti dice subito se il settore scelto
è troppo stretto o troppo largo.

## 5. Cosa viene calcolato

**Redditività** — EBITDA margin, ROS (EBIT/ricavi), ROI (EBIT/attivo), ROE, utile netto su
ricavi, valore aggiunto su ricavi.
**Struttura finanziaria** — PFN, PFN/EBITDA, debiti finanziari su patrimonio netto, leva,
oneri finanziari su ricavi, current ratio.
**Efficienza e produttività** — rotazione del capitale, giorni medi di credito e di
magazzino, incidenza del costo del lavoro, ricavi e valore aggiunto per dipendente,
costo medio per dipendente.

Per ciascun indice: **minimo, Q1, mediana, Q3, massimo, media, deviazione standard** del
campione, il valore della società e il suo **percentile**. Sulle grandezze assolute
(ricavi, EBITDA, attivo, dipendenti) la lettura parla di *dimensione*, non di performance:
fatturare meno della mediana non è un difetto gestionale.

## 6. Controllo dei costi

Ogni chiamata a pagamento è esplicita:

- niente si acquista senza **`--conferma`**;
- **`--max-crediti N`** interrompe l'esecuzione al raggiungimento del tetto;
- il conteggio delle imprese (`stima`) usa `dry_run` ed è **gratuito**;
- ogni risposta pagata è salvata in `cache/` e ogni bilancio in `dati/bilanci/`: **non si
  paga due volte lo stesso dato**, nemmeno rilanciando il comando;
- il polling sullo stato di una richiesta asincrona non consuma crediti.

Ordine di grandezza di un'analisi tipica: 1 scheda società + 2 pagine di ricerca +
N bilanci, con N = numero di concorrenti. Il costo cresce quasi tutto sul numero di bilanci:
40 concorrenti sono 40 bilanci. Se serve solo il posizionamento dimensionale,
`scarica --ripiego` usa fatturato e dipendenti già presenti nell'anagrafica.

## 7. Quando il payload non corrisponde

Le risposte cambiano forma tra servizi e piani, quindi i campi non si leggono per percorso
fisso ma per **alias**. Se un valore risulta mancante:

```bash
python3 cli.py ispeziona dati/bilanci/riclassificato/01234567890_2024.json --filtro patrimonio
```

stampa le chiavi reali del payload; aggiungi il nome che vedi in `mappa_campi.json` sotto la
voce giusta e rilancia `scarica` (il bilancio è già in locale, non si ripaga).

## 8. Limiti da tenere presenti nella relazione

- **Ritardo di deposito**: i bilanci dell'esercizio N sono disponibili tra la metà e la fine
  dell'anno N+1. Il benchmark più recente è quasi sempre su dati di due anni prima.
- **Bilanci in forma abbreviata e microimprese**: molte PMI depositano schemi ridotti, senza
  dettaglio sufficiente a ricostruire EBITDA o costo del lavoro. Quelle società entrano nel
  campione con meno indici valorizzati: guarda sempre la colonna `N` di ogni riga.
- **Codice ATECO**: è dichiarato dall'impresa e non sempre riflette l'attività prevalente
  reale. Con la revisione **ATECO 2025** molte codifiche sono cambiate: verifica che il
  codice del target sia quello giusto prima di fondarci sopra il campione.
- **Perimetro societario**: i bilanci d'esercizio non consolidati sottostimano i gruppi e
  risentono di politiche infragruppo. Un concorrente strutturato in più società appare più
  piccolo di quanto sia.
- **Politiche di bilancio** eterogenee (ammortamenti, capitalizzazioni, compensi agli
  amministratori nelle società familiari) rendono gli scostamenti *indizi*, non misure.
- I dati provengono dal Registro Imprese, che è pubblico; l'uso resta soggetto alle
  condizioni contrattuali di Openapi e alla disciplina sul riutilizzo dei dati.

## 9. File

| File | Contenuto |
|---|---|
| `cli.py` | riga di comando: `scheda`, `stima`, `peer`, `scarica`, `benchmark`, `tutto`, `ispeziona` |
| `openapi_client.py` | token OAuth, chiamate HTTP, backoff, cache su disco, tetto di spesa |
| `configurazione.py` | lettura di `config.toml` e degli endpoint |
| `imprese.py` | anagrafica della società e costruzione del campione di confronto |
| `bilanci.py` | richiesta asincrona, attesa e scarico dei bilanci |
| `campi.py` | estrazione tollerante dei campi da JSON di struttura variabile |
| `indicatori.py` | voci normalizzate e indici di bilancio |
| `benchmark.py` | quartili, percentili, lettura del posizionamento, export CSV |
| `report.py` | report HTML autonomo |
| `demo.py` | esempio completo con dati sintetici, senza rete |
| `test_bilanci.py` | test offline (`python3 test_bilanci.py`), nessun credito consumato |

## 10. Prima di consegnare l'analisi

Controlla `N` per ogni indice, apri due o tre bilanci del campione per verificare che siano
davvero concorrenti, e dichiara nella relazione i criteri del campione (ATECO, ambito, banda
dimensionale, esercizio): sono nella scheda «Criteri del campione» in cima al report HTML.
