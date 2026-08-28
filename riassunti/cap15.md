# Capitolo 15 — Economic Value Added
**Autori:** Andrea Melis, Silvia Gaia, Giulia Leoni, Simone Aresu · **Parte:** Metodologie, strumenti ed esperienze

**In una frase:** l'EVA misura solo il reddito che **eccede il costo di tutto il capitale impiegato** — capitale proprio incluso — e per calcolarlo bisogna prima liberare i valori di bilancio dalle convenzioni prudenziali e fiscali che ne offuscano la logica economica.

## Obiettivi di apprendimento
Comprendere i benefici dell'EVA come strumento di misurazione delle performance e acquisire la capacità di calcolarlo a partire dai dati di bilancio, per esprimere un giudizio di valore su un'azienda, una sua divisione o un singolo investimento.

## Concetti chiave
- **EVA** — indicatore che stima la creazione di valore (**extra-profitto**) **normalizzata** che un'azienda genera in un periodo, **dopo che sono stati remunerati tutti i fattori produttivi** ed è stata attribuita una congrua remunerazione al capitale investito nell'attività operativa. `EVA = NOPAT − (WACC × CI)`.
- **«Normalizzata»** — esclude i riflessi derivanti da situazioni straordinarie.
- **NOPAT** (*Net Operating Profit After Taxes*) — reddito operativo netto normalizzato: reddito operativo rettificato per neutralizzare politiche fiscali e principi contabili prudenziali, meno le imposte **di sola competenza operativa** (non la voce «imposte» di bilancio, che comprende anche gestione finanziaria e straordinaria).
- **CI** — capitale investito nell'attività operativa: capitale proprio + capitale di terzi a titolo oneroso + altre fonti a onerosità esplicita, anch'essi rettificati.
- **Reddito residuale** — l'EVA ne è una specie: riconosce esplicitamente il **costo opportunità del capitale proprio**. Concetto non nuovo: Solomons (1965), ispirato alla prassi della General Electric, e Mauriel-Anthony (1966).
- **Formula alternativa** — `EVA = (r − WACC) × CI`, con `r = NOPAT / CI`. Matematicamente equivalente, ma rende visibile **l'EVA generato da un euro di investimento** (r − WACC) e separa la capacità di creare valore dalla dimensione del capitale impiegato.
- **WACC** — `WACC = Ke × E/(E+D) + Kd × (1−t) × D/(E+D)`. Esprime il **tasso di rendimento minimo** richiesto per remunerare il capitale investito.

## Sviluppo

### 15.2 La logica: tre situazioni
> **Situazione 1 — Ricavi = Costi:** l'azienda **distrugge valore**. Sembra in pareggio, ma copre solo i costi iscritti in bilancio, non quelli figurativi (il costo opportunità del capitale proprio su tutti).
> **Situazione 2 — Ricavi = Costi + Oneri figurativi:** **non crea né distrugge** valore. È l'effettivo pareggio.
> **Situazione 3 — Ricavi > Costi + Oneri figurativi:** l'azienda **crea valore**.

Il punto di fondo: rendere esplicito il costo opportunità del capitale proprio serve «affinché chi gestisce l'azienda **non consideri il capitale apportato dai soci** (e/o quello derivante da autofinanziamento) **come capitale a costo nullo**», in assenza di oneri espliciti come gli interessi passivi.
*Nota:* fra gli oneri figurativi l'EVA considera esplicitamente solo il costo del capitale proprio; nelle entità minori andrebbero considerati anche **fitti figurativi** e **salario direzionale**.

### 15.3 Perché il ROI porta a decidere male — tre casi
| | Caso 1: si investe distruggendo valore | Caso 2: non si investe rinunciando a valore | Caso 3: due divisioni con soglie diverse |
|---|---|---|---|
| Situazione | RO 100.000 su CI 1.000.000 → **ROI 10%**; WACC **13%** | RO 120.000 su CI 1.000.000 → **ROI 12%**; WACC **9%** | Divisione A: ROI 15%; Divisione B: ROI 6%; **WACC 10% per entrambe** |
| Progetto | 100.000 di capitale, rendimento atteso **11%** | 100.000 di capitale, rendimento atteso **11%** | A: 10.000 con rendimento 1.300; B: 20.000 con rendimento 1.600 |
| Decisione col ROI | **Accetta** (ROI sale a 10,09%) | **Rifiuta** (ROI scende a 11,91%) | A **rifiuta** tutto sotto il 15%; B **accetta** tutto sopra il 6% |
| Effetto reale sul valore | 11.000 − (100.000 × 13%) = **−2.000** | Mancata creazione di **+2.000** | A: ΔEVA **+300 perso**; B: ΔEVA **−400 distrutto** |

**Il difetto di fondo:** il messaggio del ROI è «massimizza il tuo tasso di rendimento percentuale», **senza considerare adeguatamente il costo del capitale** usato per l'investimento. Il tasso minimo di accettazione dovrebbe essere il **costo del capitale**, non il livello corrente di redditività: «l'aumento dell'EVA è solitamente da ritenersi più importante dell'incremento del rendimento del ritorno sugli investimenti».
**Il difetto in più del ROE:** può crescere, *ceteris paribus*, **al crescere dell'indebitamento** — scelta che innalza il rischio finanziario e quindi il costo del capitale, con un effetto netto potenzialmente **negativo** sulla creazione di valore.
**Il vantaggio organizzativo dell'EVA:** con il ROI il metro di valutazione **cambia da divisione a divisione**; con l'EVA tutte le unità hanno lo **stesso obiettivo** e lo **stesso parametro di accettazione** — il costo del capitale impiegato.

**Ma attenzione al valore assoluto (caso 4).** Due aziende dello stesso gruppo:

| | Azienda A | Azienda B |
|---|---|---|
| EVA | 100.000 € | 20.000 € |
| NOPAT | 190.000 € | 27.000 € |
| CI | 1.000.000 € | 100.000 € |
| WACC | 9% | 7% |
| **r = NOPAT/CI** | **19%** | **27%** |
| **r − WACC** | **10%** | **20%** |

L'azienda A crea più valore in assoluto, ma **solo perché ha più capitale investito**, non perché sia più capace: un nuovo investimento di 10.000 € con reddito 1.500 € genera **+600 €** in A e **+800 €** in B. Guardare solo il valore totale dell'EVA «favorisce situazioni aziendali in cui è investito un maggior ammontare di capitale», **a discapito di entità sottocapitalizzate**.

**Le quattro leve per creare valore** (leggibili nella formula `(r − WACC) × CI`):
1. **Incrementare l'efficienza operativa** — aumentare il NOPAT a parità (o senza aumento proporzionale) di CI. *Cautela:* accettare una riduzione di NOPAT per una più che proporzionale riduzione di CI migliora r, ma riduce anche il **fattore moltiplicativo CI**, a danno dell'EVA complessivo.
2. **Crescere in modo profittevole** — nuovi investimenti o acquisizioni con **r > WACC**.
3. **Razionalizzare gli investimenti** — disinvestire dalle attività con **r < WACC**.
4. **Ridurre il WACC** — agire sul rapporto fra capitale di terzi e capitale proprio, considerando la rispettiva onerosità e la **deducibilità fiscale degli interessi passivi**.

### 15.4 Le nove rettifiche ai valori di bilancio
**Criterio guida:** le rettifiche vanno determinate **caso per caso**, e apportate **solo** quando hanno impatto rilevante sull'EVA e quando il **costo di reperimento dei dati è inferiore al beneficio informativo atteso** — lo stesso criterio costi-benefici che governa tutta la contabilità direzionale. Steward III ne ha identificate moltissime, ma raccomanda di non applicarle tutte.
*Nota di metodo:* qui si parte dalle rettifiche **reddituali** e se ne derivano gli effetti sul CI (cultura contabile italiana, «reddituale»); la cultura anglo-americana «patrimonialistica» fa il contrario. **Il risultato finale è immutato.**
*Nota IAS/IFRS:* poiché gli standard internazionali hanno un **principio di prudenza meno forte**, le loro valutazioni sono spesso già più coerenti con la logica EVA e **richiedono meno rettifiche**.

| Voce | Il problema contabile | La rettifica EVA |
|---|---|---|
| **Avviamento** | Ammortizzato **entro 5 anni** (max 20 secondo OIC 24): riduce sistematicamente sia il capitale investito sia l'utile per pure convenzioni | Considerarlo **parte permanente del capitale investito**: stornare la quota di ammortamento dal CE e non ridurre il CI |
| **Costi pluriennali** (impianto, R&S, formazione, pubblicità) | Capitalizzazione è una **facoltà**, non un obbligo (talvolta si spesa tutto per benefici fiscali); vita utile max 5 anni; **divieto assoluto** di ricapitalizzare in seguito | Capitalizzarli e ammortizzarli lungo il periodo in cui **producono effettivamente benefici**, riprendendoli anche se già spesati |
| **Oneri di ristrutturazione** | Iscritti nell'**area straordinaria** (OIC 29) e non capitalizzati per prudenza | Se migliorano durevolmente la capacità di produrre reddito: **portarli nell'area operativa**, capitalizzarli e ammortizzarli |
| **Rideterminazione di valore delle immobilizzazioni** | La svalutazione per perdita durevole è obbligatoria, ma la **rivalutazione è vietata** (salvo leggi speciali) | Se il valore corrente supera significativamente il netto contabile, **incrementare il CI** della differenza. Nessun effetto su NOPAT né fiscale |
| **Leasing** | Chi applica i principi nazionali usa obbligatoriamente il **metodo patrimoniale**: il bene sta nei conti d'ordine, non in bilancio | Conta la **disponibilità economica**: applicare il **metodo finanziario** — bene nell'attivo, debito nel passivo, canone scomposto in quota interessi e quota capitale |
| **TFR** | Accantonato interamente fra i **costi del personale** | È un **debito verso i dipendenti a onerosità esplicita**: stornare dal NOPAT la **quota di rivalutazione** (l'onere finanziario) e includere il fondo iniziale nei debiti onerosi. È una riclassificazione: **non incide sul capitale proprio** |
| **Rimanenze** | Ammessi FIFO, costo medio ponderato, LIFO | Solo il **FIFO** avvicina le rimanenze al valore corrente: se si è usato altro, riportare reddito operativo e CI a valutazione FIFO |
| **Fondi rischi e fondi oneri** | Entrambi trattati come passività | **Fondi oneri** (evento certo, ammontare/data incerti): coerenti con la competenza economica → **nessuna rettifica**. **Fondi rischi** (evento incerto — contenziosi, svalutazione crediti): frutto del principio di prudenza → non sono vere passività ma **riserve di capitale netto**, da remunerare come capitale proprio |
| **Compensi basati su azioni** | I principi nazionali **non li disciplinano**: nulla in CE, solo conti d'ordine | Sono un costo di prestazioni lavorative: **imputarli all'area operativa** al *fair value*, ripartito sul periodo di maturazione. *Equity-settled:* rettifica in diminuzione del RO, con riserva di PN in contropartita (il CI cambia solo per l'eventuale beneficio fiscale). *Cash-settled:* rettifiche diverse a seconda che si sia in fase di assegnazione, maturazione o esercizio |

### 15.5 Il costo del capitale
**Costo del capitale proprio (Ke).** Per le **non quotate**: somma dei flussi di dividendi attualizzati rapportati al capitale versato — e un analista *interno* dispone direttamente delle informazioni sui rendimenti attesi da imprenditore e soci. Per le **quotate**: il **CAPM**, `Ke = Rf + β(Rm − Rf)`.
- **Rf** — rendimento di titoli di Stato a lunga scadenza di Paesi a valuta forte (es. Germania).
- **Rm − Rf** — premio al rischio, stimato sulla media dei rendimenti di lungo periodo di un paniere o indice di borsa.
- **β** — rischio sistematico: **>1** più rischiosa della media di mercato, **<1** meno rischiosa, **=1** pari alla media. Facilmente reperibile per le quotate (data provider, regressione lineare); per le non quotate va **costruito da società comparabili**, scomponendo e ricomponendo per business nel caso di aziende diversificate.
Nessun modello, per quanto robusto, fornisce «una misura matematicamente esatta»: il CAPM garantisce un **«range ragionevole»**.

**Costo del capitale di debito (Kd).** Poiché il debito non è quasi mai interamente negoziato sul mercato (prevalgono finanziamenti bancari iscritti al **valore di libro**), si calcola come **oneri finanziari / capitale di debito a onerosità esplicita**. Si considerano gli interessi espliciti (più quelli emersi dalle rettifiche su leasing e TFR); si **escludono gli interessi impliciti** delle dilazioni commerciali, per ragioni di costo-beneficio. Va poi ridotto per lo **scudo fiscale (1−t)**.

**I fattori di ponderazione.** Semplici da calcolare, ma colgono la struttura finanziaria **in un istante**, rendendola apparentemente statica; e in teoria si dovrebbe usare la struttura finanziaria **ottimale** — quella che minimizza il costo del capitale — mentre «nella pratica ci si limita a cogliere la struttura finanziaria nel momento attuale».

## Casi

**Gamma e Omega** — due imprese dello stesso settore industriale:

| | Gamma | Omega |
|---|---|---|
| Ke | 5,23% | 6,33% |
| Kd | 5,45% | 9,02% |
| E/(E+D) | 0,47 | 0,28 |
| D/(E+D) | 0,53 | 0,72 |
| **WACC** | **5,35%** | **8,27%** |
| **r** | **6,52%** | **8,10%** |
| **r − WACC** | **+1,17%** | **−0,17%** |
| **EVA** | **+53.776,15 €** | **−9.951,86 €** |

**Il ribaltamento del giudizio.** Guardando la sola redditività del capitale investito, un manager preferirebbe Omega (**8,10% > 6,52%**). Includendo il costo del capitale la valutazione è **diametralmente opposta**: Omega, pur più redditizia, **distrugge valore** perché r < WACC; Gamma, meno redditizia, **crea valore** perché r > WACC.
**Perché.** Il punto di forza di Gamma è la **gestione del costo del capitale**: β = 0,9 (meno rischiosa della media) contro β = 1,3 di Omega, e un rapporto di indebitamento 0,53 contro 0,72. L'alto indebitamento di Omega agisce **due volte** contro di lei: alza il Kd (maggior rischio percepito) **e** dà più peso alla fonte più onerosa — infatti in Omega il debito costa **più del capitale proprio** (9,02% vs 6,33%), mentre in Gamma le due fonti sono quasi equivalenti (5,45% vs 5,23%).
**Le tre azioni consigliate a Omega:** incrementare ulteriormente l'efficienza operativa fino a coprire il costo del capitale; **modificare la struttura finanziaria** ricorrendo di più al capitale proprio (che nel suo caso è la fonte **meno** onerosa, e che riducendo il rischio percepito abbasserebbe anche il Kd); valutare la redditività dei singoli investimenti in essere, eliminando quelli con rendimento inferiore al costo del capitale.

### 15.7 I limiti dell'EVA
L'EVA «è una sommatoria di stime soggettivamente determinate»: una **quantità economica congetturata**, come il reddito d'esercizio e tutti gli indicatori che ne derivano. Differisce dal reddito operativo per tre ragioni: **integra** economicamente i valori di bilancio (considerando anche il reddito *potenziale* non evidenziato per prudenza o convenienza fiscale); è un **reddito residuale** che sottrae il costo del capitale; **tiene conto** sia del costo opportunità del capitale proprio sia del beneficio fiscale degli interessi passivi.

**I due limiti principali:**
- **Orientamento al breve periodo.** Come ROI e ROA, può indurre a **ridurre gli investimenti** per migliorare l'EVA di periodo compromettendo la posizione competitiva. È il caso degli **investimenti strategici** a rendimento differito, la cui inclusione sottostima il valore creato. Rimedi: **escluderli** dal calcolo del periodo e riammetterli progressivamente, oppure **estendere il periodo di riferimento**.
- **Rischio nell'uso come metrica di incentivazione.** Amministratori e alti dirigenti sarebbero remunerati su un valore prossimo al reddito **«potenziale»**, mentre i soci ricevono dividendi calcolati sul reddito **«prodotto»** secondo i principi contabili, in maniera più prudente. Rimedi: inserire l'EVA **in un sistema di indicatori** e/o usare le **variazioni** dell'EVA anziché il valore assoluto.

La conclusione: mai usare l'EVA come unico indicatore di sintesi, ma includerlo in un sistema che comprenda anche stime di performance intermedia non economico-finanziarie (efficienza ed efficacia dei processi interni, rapporti con i clienti) — l'approccio di Drucker (1995) e della **balanced scorecard** di Kaplan e Norton.

## Punti da ricordare
- L'EVA non è un indicatore di redditività, è un indicatore di **redditività residuale**: risponde alla domanda «quanto ho guadagnato *oltre* a quello che il capitale mi costava?».
- Il ROI porta a decidere male in due modi simmetrici: fa accettare progetti sotto il costo del capitale (se sopra il ROI corrente) e fa rifiutare progetti sopra il costo del capitale (se sotto il ROI corrente).
- La soglia di accettazione di un investimento deve essere il **WACC**, uguale per tutte le divisioni, non il ROI corrente della divisione che decide.
- Non confrontare EVA assoluti fra aziende di dimensione diversa: usare `r − WACC` per isolare la capacità di creare valore dal capitale impiegato.
- Le rettifiche non sono un rito completo da eseguire tutte: si fanno solo quando il beneficio informativo supera il costo di reperimento dei dati.
- I fondi rischi, secondo la logica EVA, non sono passività ma **riserve di capitale proprio** da remunerare; i fondi oneri invece vanno bene così come sono.
- Un'alta redditività con una struttura finanziaria squilibrata può distruggere valore: è il caso Omega.

```schema
{"type":"flow","title":"La logica dell'EVA: quando si crea davvero valore",
 "steps":[
  {"label":"Situazione 1: Ricavi = Costi","detail":"copre solo i costi iscritti in bilancio\n→ l'azienda DISTRUGGE valore"},
  {"label":"Situazione 2: Ricavi = Costi + Oneri figurativi","detail":"copre anche il costo opportunità del capitale proprio\n→ NÉ crea NÉ distrugge: è il vero pareggio"},
  {"label":"Situazione 3: Ricavi > Costi + Oneri figurativi","detail":"eccede la remunerazione di tutti i fattori\n→ l'azienda CREA valore"}],
 "note":"Rendere esplicito il costo del capitale proprio evita che chi gestisce lo consideri capitale a costo nullo."}
```

```schema
{"type":"compare","title":"ROI ed EVA a confronto: due decisioni sbagliate",
 "columns":["CASO 1: si investe","CASO 2: non si investe"],
 "rows":[
  ["Situazione di partenza","ROI 10% (RO 100.000 / CI 1.000.000)","ROI 12% (RO 120.000 / CI 1.000.000)"],
  ["Costo del capitale (WACC)","13%","9%"],
  ["Rendimento atteso del progetto","11%","11%"],
  ["Confronto con il ROI corrente","11% > 10% → il ROI sale a 10,09%","11% < 12% → il ROI scende a 11,91%"],
  ["Decisione presa guardando il ROI","ACCETTA","RIFIUTA"],
  ["Confronto con il WACC","11% < 13%","11% > 9%"],
  ["Effetto reale sul valore","− 2.000 € distrutti","+ 2.000 € non creati"]]}
```

```schema
{"type":"hierarchy","title":"Le quattro leve per creare valore economico","root":"EVA = (r − WACC) × CI",
 "branches":[
  {"label":"Efficienza operativa","children":["Aumentare il NOPAT","a parità di capitale investito","o senza aumento proporzionale","Cautela: ridurre CI riduce anche","il fattore moltiplicativo"]},
  {"label":"Crescita profittevole","children":["Nuovi investimenti","o acquisizioni di aziende","e rami d'azienda","con r > WACC"]},
  {"label":"Razionalizzazione","children":["Disinvestire dalle attività","che distruggono valore","cioè quelle con r < WACC"]},
  {"label":"Efficienza delle fonti","children":["Ridurre il WACC","orientando il rapporto","fra capitale di terzi e proprio","tenendo conto dell'onerosità","e dello scudo fiscale"]}]}
```

```schema
{"type":"matrix","title":"Le rettifiche principali ai valori di bilancio",
 "rows":["Avviamento","Costi pluriennali","Oneri di ristrutturazione","Leasing","TFR","Rimanenze","Fondi rischi","Compensi in azioni"],
 "cols":["Problema contabile","Rettifica ai fini EVA"],
 "cells":[
  ["Ammortizzato entro 5 anni per convenzione prudenziale","Parte permanente del capitale investito: stornare l'ammortamento"],
  ["Capitalizzazione facoltativa, vita utile max 5 anni, divieto di ripresa","Capitalizzare e ammortizzare sull'effettiva utilità economica"],
  ["Iscritti nell'area straordinaria, non capitalizzati","Portarli nell'area operativa, capitalizzare e ammortizzare"],
  ["Metodo patrimoniale obbligatorio: bene nei conti d'ordine","Metodo finanziario: conta la disponibilità economica del bene"],
  ["Accantonato interamente fra i costi del personale","È un debito oneroso: stornare la quota di rivalutazione dal NOPAT"],
  ["Ammessi FIFO, costo medio ponderato e LIFO","Riportare tutto a FIFO: è il criterio più vicino al valore corrente"],
  ["Trattati come passività (principio di prudenza)","Sono riserve di capitale netto, da remunerare come capitale proprio"],
  ["Non disciplinati dai principi nazionali: solo conti d'ordine","Imputare il fair value della prestazione fra i costi operativi"]],
 "note":"Regola generale: rettificare solo quando l'impatto è rilevante e il costo dei dati è inferiore al beneficio informativo."}
```

```schema
{"type":"hierarchy","title":"La costruzione del WACC","root":"WACC = Ke·E/(E+D) + Kd(1−t)·D/(E+D)",
 "branches":[
  {"label":"Ke — costo del capitale proprio","children":["NON quotate: flussi di dividendi attualizzati","QUOTATE: CAPM","Ke = Rf + β(Rm − Rf)","Rf = titoli di Stato a valuta forte","β>1 più rischiosa del mercato","β<1 meno rischiosa"]},
  {"label":"Kd — costo del capitale di debito","children":["Oneri finanziari / debito oneroso","Il debito è quasi sempre a valore di libro","Esclusi gli interessi impliciti commerciali","Inclusi gli oneri emersi da leasing e TFR"]},
  {"label":"(1−t) — scudo fiscale","children":["La deducibilità degli interessi passivi","riduce il costo effettivo del debito","Il capitale proprio non ne beneficia"]},
  {"label":"Fattori di ponderazione","children":["Pesi di capitale proprio e debito","Colgono la struttura finanziaria","in un solo istante","In teoria servirebbe quella ottimale"]}]}
```

```schema
{"type":"compare","title":"Caso applicativo: Gamma e Omega",
 "columns":["GAMMA","OMEGA"],
 "rows":[
  ["Costo del capitale proprio (Ke)","5,23%","6,33%"],
  ["Costo del capitale di debito (Kd)","5,45%","9,02%"],
  ["Beta","0,9 (meno rischiosa del mercato)","1,3 (più rischiosa del mercato)"],
  ["Peso del debito D/(E+D)","0,53","0,72"],
  ["WACC","5,35%","8,27%"],
  ["Redditività del capitale investito (r)","6,52%","8,10%"],
  ["r − WACC","+ 1,17%","− 0,17%"],
  ["EVA","+ 53.776 € : CREA valore","− 9.952 € : DISTRUGGE valore"]]}
```

```schema
{"type":"tradeoff","title":"I limiti dell'EVA e i rimedi",
 "left":{"label":"ORIENTAMENTO AL BREVE PERIODO","points":["Ridurre gli investimenti migliora l'EVA di periodo","ma compromette la posizione competitiva","Gli investimenti strategici a rendimento differito","fanno sottostimare il valore creato"]},
 "right":{"label":"RISCHIO NELL'INCENTIVAZIONE","points":["I manager sarebbero pagati sul reddito «potenziale»","i soci ricevono dividendi sul reddito «prodotto»","calcolato in maniera più prudente"]},
 "note":"Rimedi: escludere e riammettere progressivamente gli investimenti strategici, estendere l'orizzonte, usare le variazioni dell'EVA anziché il valore assoluto, e inserire l'EVA in un sistema di indicatori (balanced scorecard)."}
```
