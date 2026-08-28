# Capitolo 26 — Metodi «agili» per il controllo di gestione
**Autore:** Loredana G. Smaldore · **Pagine:** 961-972 · **Parte:** Pratiche innovative

**In una frase:** il budget può essere trattato come un insieme di piccoli progetti interdipendenti e gestito con il framework Scrum, ottenendo un processo più partecipativo, iterativo e capace di assorbire l'incertezza.

## Obiettivi di apprendimento
Capire se e come metodologie e strumenti agili — nati per lo sviluppo software — possano essere impiegati non solo nella gestione di progetti, ma anche a supporto dei tradizionali sistemi di pianificazione e controllo.

## Concetti chiave
- **Agile Manifesto (2001)** — quattro priorità: individui e interazione > processi e strumenti; working software > documentazione esaustiva; collaborazione col cliente > negoziazione contrattuale; risposta al cambiamento > pianificazione.
- **Scrum** — approccio flessibile di project management (Schwaber e Sutherland, primi anni '90): non un processo normativo ma un percorso iterativo e incrementale che rende continuamente visibile lo stato di avanzamento.
- **Ruoli Scrum** — *product owner* (verifica l'avanzamento rispetto alle esigenze di business), *scrum master* (garantisce il rispetto delle regole e coordina), *team* (7±2 membri, realizza il prodotto). Tutte le responsabilità sono ripartite fra questi tre ruoli.
- **Elementi Scrum** — *product backlog* (lista di item ordinati per priorità dal product owner), *sprint backlog* (task dello sprint), *burndown chart* (grafico del lavoro residuo).
- **Attività Scrum** — *sprint planning meeting*, *sprint review*, *scrum meeting* giornaliero di 15 minuti.
- **Sprint** — iterazione di 2-4 settimane che deve rilasciare un output valutabile dal cliente.
- **Beyond budgeting** — modello di budgeting collaborativo, partecipativo e decentralizzato (Hope & Fraser, 2003), in cui la dipendenza rigida dal senior management è sostituita da una rete che distribuisce le decisioni sui front-line manager.

## Sviluppo

### 26.2 Agile project management
Il capitolo ricostruisce la filosofia Agile e il framework Scrum come sistema di ruoli, elementi e attività fra loro collegati. La logica di fondo è la sostituzione di una pianificazione lunga e rigida con cicli brevi che producono output verificabili, così da rendere il cambiamento gestibile anziché subìto.

### 26.3 L'integrazione fra budgeting e Agile
L'autrice prende il processo classico di redazione del budget in otto step (definizione delle responsabilità al Budget Committee e nomina del Budget Officer; comunicazione delle linee guida; identificazione del *budget chiave* ossia del fattore limitante — di norma quantità vendute e ricavi; preparazione dei budget delle altre aree; coordinamento e revisione; redazione del Master Budget economico-finanziario-patrimoniale; condivisione; monitoraggio) e lo riscrive in chiave agile su **tre step**, ciascuno gestito con uno schema Scrum completo:

1. **Redazione dei budget delle singole aree** — product owner: responsabile Finanza e Controllo; scrum master: un accountant; team cross-funzionale di manager di area. Il *budget backlog* raccoglie dati e richieste ordinati per priorità (per il budget commerciale: analisi dei potenziali clienti, previsione volumi, prezzi, sconti).
2. **Coordinamento dei budget di area e collegamento al Master Budget** — competenza integrale della funzione Finanza e Controllo; si verifica coerenza, allineamento strategico e rispetto dei vincoli di interdipendenza. Product owner: il Budget Officer; scrum master: il manager di funzione; team: gli accountant.
3. **Redazione del Master Budget** — product owner: la carica aziendale più alta (imprenditore, presidente o AD); scrum master: il Budget Officer; team: il Budget Committee dei senior manager di funzione.

### 26.3.3 Il meccanismo di collegamento fra gli step
È il punto più originale del capitolo: **il product owner di uno step è lo scrum master dello step successivo**. Questa sovrapposizione deliberata dei ruoli crea continuità, fa passare in tempo reale gli output intermedi degli sprint da un livello all'altro e impedisce che i tre step diventino tre momenti indipendenti e scollegati.

## Punti da ricordare
- Il budget viene reinterpretato come **portafoglio di progetti interdipendenti**, non come documento unico.
- Benefici attesi: partecipazione dei manager di area, maggiore motivazione e consapevolezza dei target, più trasparenza delle dinamiche funzionali, minore incentivo a manomettere i risultati a consuntivo, adattamento rapido alla turbolenza.
- I target possono ancora essere assegnati top-down, ma vengono discussi e talvolta modificati nelle iterazioni: si scoraggia l'imposizione pura.
- **Limiti dichiarati dall'autrice:** la proposta è simulata su una grande azienda, capace di sostenere tre livelli di Scrum e di diversificare le figure nei ruoli; l'estensione a contesti minori richiede cautela, perché nelle piccole imprese il budgeting è meno articolato. L'implementazione effettiva richiede adattamenti a cultura interna, pratiche e sistemi informativi esistenti.

```schema
{"type":"flow","title":"Il processo di agile budgeting su tre step",
 "note":"Il product owner di ogni step è lo scrum master dello step successivo: è questo che tiene insieme il processo.",
 "steps":[
  {"label":"Step 1 — Budget delle aree","detail":"PO: resp. Finanza e Controllo\nSM: accountant\nTeam: manager di area"},
  {"label":"Step 2 — Coordinamento","detail":"PO: Budget Officer\nSM: resp. Finanza e Controllo\nTeam: accountant"},
  {"label":"Step 3 — Master Budget","detail":"PO: AD / presidente\nSM: Budget Officer\nTeam: Budget Committee"}]}
```

```schema
{"type":"hierarchy","title":"Il framework Scrum",
 "root":"SCRUM",
 "branches":[
  {"label":"Ruoli","children":["Product owner","Scrum master","Team (7±2)"]},
  {"label":"Elementi","children":["Product backlog","Sprint backlog","Burndown chart"]},
  {"label":"Attività","children":["Sprint planning","Sprint review","Scrum meeting (15')"]}]}
```
