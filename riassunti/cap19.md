# Capitolo 19 — Nuove tecnologie dell'informazione per il controllo di gestione
**Autrici:** Monica Bianchini e Maria Pia Maraghini · **Parte:** Pratiche innovative

**In una frase:** le nuove tecnologie non sono solo un supporto al controllo di gestione, ne sono **esse stesse una determinante** — ma «generano solo delle **potenzialità** di cambiamento», che si realizzano unicamente se si fa evolvere in parallelo il contesto organizzativo e culturale.

## Obiettivi di apprendimento
Riconoscere e imparare a gestire le principali criticità e potenzialità per il sistema di pianificazione e controllo derivanti dall'adozione dei sistemi informativi integrati **ERP** e delle soluzioni di **Business Intelligence** e **Strategic Performance Management**.

## Concetti chiave
- **OLTP** (*On-Line Transactional Processing*) — sistemi basati sul concetto di **transazione**: operazione atomica elementare di cui si segue passo per passo l'esecuzione (inserire o evadere un ordine). Se l'operazione non va a buon fine i dati **non vengono memorizzati** e il sistema è ripristinato alla condizione iniziale: è questa modalità a fondarne l'affidabilità.
- **ERP** (*Enterprise Resource Planning*) — pacchetti software standard che supportano, tramite **moduli**, i diversi processi operativi e gestionali. La caratteristica qualificante è l'integrazione, che qui è **«nativa»**: ogni componente nasce già integrata sotto il profilo dell'architettura informatica *e* della struttura logica.
- **Datawarehouse (DW)** — «magazzino dei dati»: struttura di memorizzazione evoluta che fa confluire dati da sorgenti eterogenee, li integra in un unico schema globale e li rende disponibili per analisi e valutazioni. Funge da **hub** dei flussi di dati aziendali, offrendo un patrimonio di dati **«semilavorati»** — originariamente eterogenei, poi certificati, documentati e resi coerenti.
- **OLAP** (*On-Line Analytical Processing*) — l'elaborazione **analitica**, separata da quella transazionale: è l'idea alla base del data warehousing.
- **Business Intelligence (BI)** — l'ampia gamma di strumenti ICT che estraggono, dalla mole dei dati operazionali, informazioni utili ai fini decisori. Detti anche **DSS** (*Decision Support System*): «richiedono la **simbiosi** tra utente e sistema».
- **Fatti e dimensioni** — i **fatti** sono gli avvenimenti di cui si tiene traccia, e la **misurabilità è una loro proprietà intrinseca** (numero di vendite, incassi); le **dimensioni** sono le grandezze attraverso cui si indaga sui fatti, organizzate **gerarchicamente** (negozio → città → provincia → regione).

## Sviluppo

### 19.1 Il rapporto è a doppio senso
Guardare alle tecnologie solo come supporto «è estremamente riduttivo». Tre precisazioni:
- **Possono ostacolare, non solo aiutare**: alcuni autori sostengono che l'introduzione di «sistemi esperti» basati su intelligenza artificiale possa produrre **una diminuzione della flessibilità e della capacità di problem solving**, per la rigidità della struttura del sistema.
- **Sono una determinante del cambiamento**, non solo il suo strumento: «tutte le diverse funzioni aziendali sono chiamate a **ridisegnare i propri modelli di gestione**» per sfruttarne le potenzialità.
- **La funzione più coinvolta è proprio il controllo**, perché «la sua attività si fonda proprio sulle informazioni».

Le tre direttrici lungo cui l'IT ha supportato pianificazione e controllo: (1) **mettere a disposizione** dati e informazioni di base; (2) **gestirli** ai fini delle decisioni; (3) **supportare la creazione di conoscenza** per il dominio del processo.

### 19.3 Gli ERP: le quattro caratteristiche funzionali
| Caratteristica | In che consiste |
|---|---|
| **Unicità della base dati** | Database unico automaticamente aggiornato: i dati di un'entità sono **immessi una sola volta** e restano a disposizione di tutte le applicazioni. Si separano nettamente i dati dalle procedure, evitando ridondanze, disallineamenti e «informazioni e reporting **non ufficiali** racchiusi in aree o compartimenti del sistema» |
| **Business model integrato** | Schema sintetico che ingloba tutte le interconnessioni logiche fra le parti; rappresentando **le best practice**, «può essere efficacemente utilizzato come riferimento per sviluppare l'attività di **reingegnerizzazione** dei processi» |
| **Configurabilità** | Possibilità di adattare il sistema alle proprie specificità: «continua ricerca di un **compromesso** fra le esigenze aziendali e le opzioni concesse dal sistema». Non è solo una possibilità ma **un obbligo**, propedeutico all'uso quotidiano |
| **Modularità** | Soluzioni applicative distinte per segmento del ciclo operativo, ma «originariamente concepite e funzionanti in modo unitario» |

**Il ribaltamento di paradigma.** «Con i sistemi ERP si ribalta il tradizionale paradigma per cui il sistema informativo deve aderire ai modelli di gestione dell'azienda: **è semmai quest'ultima che deve cercare di adattare i propri processi** alla gamma di modelli proposti». Ciò che sembra un vincolo «tende invece a risolversi in un elevato grado di libertà», perché le prassi codificate sono espressione di **modelli di eccellenza operativa**.

**Se la configurabilità non basta,** due strade: la **personalizzazione** (modificare il sistema alla base nell'ambiente di sviluppo) — che però «può rendere problematiche le modalità di comunicazione fra le parti del sistema» e **compromettere l'acquisizione delle nuove release**; oppure applicativi distinti integrati con **interfacce** — che «ha il difetto di ridurre il grado di integrazione informativa».

**I vantaggi della modularità e il loro rovescio.** Consente di introdurre solo le funzionalità utili e di adottare **una copertura incrementale** delle aree aziendali. Ma esiste la **propedeuticità dei moduli**: «per alcuni di questi le possibilità di alimentazione risultano subordinate all'attivazione di altri moduli collegati», e la copertura incrementale «riduce i benefici derivanti dall'integrazione informativa, che risulta compromessa da una realizzazione **solo parziale**».

**Tre ambiti e due piani di integrazione.**
- *Ambiti:* **informativa** (standardizzazione delle modalità di definizione dei dati e armonizzazione di struttura e contenuto); **cognitiva** (schema cognitivo unitario di interpretazione, linguaggio comune, socializzazione delle conoscenze locali); **manageriale** (articolazione della responsabilità).
- *Piani:* **fra livelli gerarchici** — il vertice accede non solo agli aggregati ma «anche a livello di **informazione elementare**»; **fra unità coinvolte nei processi**, rendendo trasparenti e leggibili i processi gestionali «e una facile identificazione delle loro **disfunzioni**». **È questo secondo piano il vero e principale vantaggio dell'adozione di un ERP.**

**Il prezzo: la standardizzazione.** I benefici non derivano dalla semplice implementazione: richiedono la **preventiva standardizzazione** dei comportamenti tramite codifica delle procedure. Operazione difficile, «in quanto tende a **irrigidire** il funzionamento dell'organismo aziendale, che è invece costantemente chiamato a una crescente flessibilità». Ma se ben interpretata la standardizzazione dà maggiore efficienza organizzativa, agevola controllo e supervisione, **«mette un freno alla proliferazione incontrollata di prassi che non generano valore»** eliminando la complessità inutile — e così «permette invece di gestire **la complessità che genera valore**».
> **I timori legittimi:** che l'organizzazione «**rigetti** l'integrazione totale che i sistemi ERP propongono» e non riesca a risolvere la loro complessità intrinseca — tanto più che l'implementazione richiede impegni significativi di risorse.

**L'apertura verso l'esterno.** Con i protocolli internet gli ERP diventano **EERP** (o *xERP*), aggiungendo **CRM** (rapporti con i clienti), **PRM** (con i partner) e **SCM** (con il sistema logistico: fornitori, sub-fornitori, trasportatori, rivenditori, assistenza post-vendita). L'approdo è il **Collaborative Commerce**: «l'insieme delle modalità di cooperazione fra aziende che fanno leva sulle nuove tecnologie per integrare processi dai fornitori ai clienti finali».
> **Il punto teorico decisivo:** nell'economia dell'informazione «la fonte principale di vantaggio competitivo si sposta **dal controllo delle informazioni alla capacità di trasformarle rapidamente** in progetti innovativi e di qui in azioni decisive sul mercato». Chi concepisce la conoscenza come patrimonio esclusivo si dota «di una pericolosa **zavorra competitiva**»: se il valore della conoscenza è funzione della sua scambiabilità, essa **non può costituire il presupposto di un vantaggio competitivo**.

### 19.4 Datawarehouse e Business Intelligence
**Perché i sistemi gestionali non bastano per la pianificazione strategica.** «Il *contenuto strategico* delle informazioni aziendali non è immediatamente fruibile, perché **occultato sotto l'enorme mole di cifre e dati**». La pianificazione richiede dati **storici e prospettici**, da più sistemi transazionali e da **fonti esterne**, quantitativi e qualitativi, su ogni dimensione dell'agire aziendale — e richiede un **diverso accesso**: nei sistemi transazionali l'utente accede a pochi record selezionati, nei sistemi decisionali «deve poter **spaziare in un più vasto contesto**».
Un ambiente separato ha anche un vantaggio difensivo: evita accessi eccessivi ai dati transazionali, «che potrebbero venire danneggiati, anche involontariamente».

**Le quattro proprietà del DW (Inmon):**
- **Orientamento al soggetto** — i dati non sono strutturati per processo ma per **tipo di analisi** (controllo di gestione, marketing, logistica, clienti). Non tutti i dati operazionali confluiscono nel DW, solo quelli di supporto alle decisioni; **la ridondanza è ammessa se semplifica l'analisi**.
- **Integrazione** — codifica uniforme per garantire **omogeneità semantica**.
- **Variabilità nel tempo** — il DW memorizza una serie di **«fotografie»** (*snapshot* o *time stamp*), passate e attuali, eventualmente includendo previsioni a breve e medio termine; l'ampiezza dell'intervallo deve poter essere cambiata per consentire confronti.
- **Non volatilità** — una volta memorizzati, i dati **non possono subire modifiche**: il DW permette solo interrogazioni. Il riallineamento è periodico e **off-line**.

**Relazionale vs multidimensionale.** Nel modello **relazionale** i dati stanno in tabelle (colonne = attributi, righe = *tuple* o record, chiave primaria identificativa) e si interrogano in **SQL**. Per sapere quanto prodotto A001 è stato venduto a Firenze in giugno serve una query con `sum(quantità)` — l'informazione non è direttamente disponibile. Nel modello **multidimensionale** l'informazione si legge immediatamente come **cella di un «ipercubo»**, incrociando le dimensioni prodotto, punto vendita, mese.
Gli ipercubi sono alimentati con procedure **ETL**: *Extraction* (estrazione dei dati grezzi) → *Transformation* (perché siano agevolmente utilizzabili) → *Loading* (caricamento e aggiornamento).
**Data Mart (DM)** — «viste sui dati» concettualmente appartenenti al DW ma rivolte a specifiche aree o sottoinsiemi tematici (ordini, vendite, marketing). Spesso la realizzazione di piccoli DM «rappresenta il primo passo nel progetto di un DW completo».

**Le tre famiglie di strumenti di BI.**

**A) Accesso ai dati.** *Analisi multidimensionale interattiva* con le quattro funzioni OLAP:

| Funzione | Che cosa fa |
|---|---|
| **Roll up** | Risale la gerarchia: dal fatturato giornaliero al settimanale, al mensile, all'annuale |
| **Drill down** | Funzione opposta: «esplode» il dato aggregato — dal fatturato complessivo a quello per area, regione, provincia, punto vendita |
| **Slice & dice** | Analizza porzioni specifiche dell'ipercubo selezionando elementi in più dimensioni (settembre + prodotto X + Centro Italia + canale ingrosso); supporta il **drill across**, l'analisi trasversale su percorsi variabili |
| **Pivoting** | Ri-orienta l'ipercubo: da clienti-su-prodotti a prodotti-su-clienti |

Più il *reporting* (formato tabellare, grafico, cartografico; i report possono essere prodotti e inviati automaticamente via e-mail o fax, anche in **briefing book** personalizzati per il management) e l'**interrogazione ad hoc**, anche tramite **EIS** (*Executive Information System*): analisi «preconfezionate» con interfacce intuitive per decisori meno esperti, ma con viste e livelli di aggregazione predefiniti, quindi **poco flessibili**.

**B) Creazione di conoscenza.**
*Modelling, scenari e simulazione* — tre strumenti in sequenza: **mappe** (approccio logico-qualitativo che esplicita e formalizza le conoscenze possedute, dalle semplici check-list ai *causal loop diagrams* agli *stock and flow diagrams*); **modelli matematici di simulazione**; **micromondi o simulatori di volo**, «ambienti protetti di simulazione, sperimentazione e verifica». Metodologia di riferimento: la **System Dynamics**.
Tre tipi di analisi: **what if** (l'effetto delle variazioni delle ipotesi su fatturato, margine operativo, utile netto, PFN, investimenti: serve a valutare il rischio di una politica e identificarne i fattori critici); **goal seeking** (si indica l'obiettivo e le variabili su cui lavorare — «una sorta di processo di *reverse engineering*, si effettua una ricerca nello **spazio delle possibili condizioni iniziali**»); **analisi di sensitività** (estensione della what if su più variabili simultanee, con scenari a diverso grado di rischio e tasso di probabilità associato).
> **Il beneficio vero non è la previsione:** i decisori «sono soprattutto spinti a **mettere in discussione i propri modelli mentali**», portati alla cooperazione e alla condivisione, e stimolati a un processo di apprendimento autonomo.

*KDD (Knowledge Data Discovery)* — processo interattivo e iterativo di identificazione di relazioni fra dati che siano **valide, nuove, potenzialmente utili e comprensibili**. «Si assume che il processo sia **non banale**, cioè che le relazioni scoperte non siano già note»; e devono valere, con un grado di certezza prefissato, **anche su dati diversi** da quelli usati per scoprirle.
Le fasi: *selezione* (dai dati grezzi ai **target data**) → *preprocessing* con **data cleaning** (eliminare errori, definire il comportamento in caso di dati mancanti) → *trasformazione* (conversioni di tipo, codifica omogenea di fonti diverse) → **data mining** → *interpretazione e valutazione*.
Quattro famiglie di tecniche di data mining, con i loro usi:

| Tecnica | Applicazione tipica |
|---|---|
| **Clustering** e reti neurali non supervisionate | Raggruppare dati omogenei: *database marketing*, gruppi omogenei di acquirenti per comportamento d'acquisto e caratteristiche socio-demografiche |
| **Classificazione** (reti neurali supervisionate, metodi kernel, alberi di decisione) | Classificare nuovi oggetti o prevedere eventi: le compagnie telefoniche individuano **in anticipo gli utenti che diventeranno morosi** |
| **Regole di associazione** | *Basket analysis*: quali prodotti vengono acquistati congiuntamente, per migliorare la disposizione sugli scaffali |
| **Similarity search** | Società con comportamento simile di crescita, prodotti con profilo simile di vendita, azioni con andamento simile |

Tutte rientrano nel **soft-computing**, che «a differenza dell'*hard computing* è **tollerante rispetto a imprecisione, incertezza e verità parziale**. Di fatto, il modello di riferimento del soft-computing è la **mente umana**» (Zadeh).

**C) Impostazione strategica: BPM/SPM.** I sistemi di **Business (o Strategic) Performance Management** «si avvalgono di tutte le precedenti funzionalità della BI — correlate e composte in un disegno unitario». Destinati al vertice, mettono a disposizione «le *informazioni strategiche* di cui è alla ricerca, **senza preoccuparsi dei sistemi di gestione da cui vengono estrapolati i dati**». Si concretizzano nei cruscotti: **Tableau de Bord, Strategical Scorecard, Balanced Scorecard**.

### 19.5 Perché le PMI restano indietro (e perché sta cambiando)
Due ragioni: la **mancanza di una cultura della pianificazione** — «mancano le capacità di selezione dei dati rilevanti, di analisi e interpretazione ai fini di scelte strategiche»; e l'**elevato costo**, non solo economico-finanziario ma «in termini di tempo, di sforzi e di risorse umane dedicate».
Ma l'offerta si sta spostando: «la progressiva **saturazione del mercato delle multinazionali**» ha spinto produttori e distributori verso le PMI, con **pacchetti preconfigurati** implementabili con maggiore semplicità, rapidità e costi inferiori.

### 19.6 La gestione del cambiamento
**Il principio di fondo:** l'adozione «genera solo delle **potenzialità** di cambiamento, ma non può essere, per sé, promotrice di modificazioni predefinite, da attendersi in modo **meccanicistico**». L'espressione di tali potenzialità è legata allo specifico contesto organizzativo, culturale e sociale, alla sua storia: il cambiamento nei sistemi di controllo è un processo **«path-dependent»**.

**Le dieci «buone regole»:**
1. Assicurarsi il **commitment del vertice**, sostenerlo per tutta la durata e comunicarlo a tutti i livelli.
2. Far avvertire l'adozione come **un'importante occasione di cambiamento**.
3. Adottare un approccio **euristico**, attento alle variabili sociali, politiche, culturali e istituzionali che compongono «la **dimensione immateriale** del controllo».
4. Pianificare e gestire con cura gli aspetti relativi alle **risorse umane**.
5. Far precedere alla scelta del sistema un'accurata **analisi organizzativa (as is)**.
6. Anticipare e accompagnare l'adozione predisponendo le condizioni organizzative: modifica della struttura, **BPR**, gruppi di lavoro interni.
7. **Partecipare attivamente** alla configurazione e all'implementazione.
8. Farsi affiancare da risorse esterne **ma non dipenderne**.
9. Accompagnare con **comunicazione costante e formazione**.
10. Stimolare sempre attenzione e motivazione al cambiamento.

**La causa numero uno di fallimento nelle PMI: la «fretta nell'implementazione».** Le tecnologie vengono implementate «in contesti aziendali **impreparati** al cambiamento, i quali si trovano a dover recuperare *in corsa* la loro situazione di svantaggio». Anche quando non porta a un esito negativo, «non consente comunque di cogliere appieno le opportunità, facendo nascere un generale **senso di sfiducia**».

**Le resistenze e come trattarle.** Nascono perché il personale «si trova non solo a dover imparare a utilizzare un nuovo applicativo, ma anche e soprattutto **a dover cambiare il proprio modo di essere e di lavorare**»; e ancora dai cambiamenti nella **distribuzione del potere interno**, dalla minaccia al proprio *status*, dallo stress dell'implementazione. Vanno affrontate subito: «se non sciolte in modo corretto e fermo al loro sorgere, diventano in seguito difficilmente gestibili». La prima mossa è **portarle alla luce**: «una resistenza **aperta** al cambiamento è sempre preferibile a una resistenza **occulta e passiva**».

**La formazione.** Deve iniziare **prima** dell'adozione — «il mancato investimento in tal senso costituisce una delle principali cause di fallimento» — e continuare anche a regime. E non deve fermarsi all'addestramento al software: deve arrivare a trasferire «le **logiche** attraverso le quali lo stesso supporta i processi aziendali». L'obiettivo: «ciascun individuo deve riuscire a comprendere **tutti gli effetti generati da ogni sua singola operazione** sul sistema».

**Il nuovo profilo richiesto alle persone.** Il passaggio «da una logica impostata per insiemi di compiti omogenei e circoscritti a una visione per processi» richiede **risorse polivalenti**, capaci di intervenire con competenza su segmenti ampi di processi, con spirito d'iniziativa e capacità di lavorare in gruppo: «**flessibilità, proattività, creatività, estroversione** debbono costituire i nuovi paradigmi dell'agire aziendale».

## Punti da ricordare
- ERP e BI rispondono a esigenze diverse: i primi rendono disponibili dati **affidabili e integrati**, i secondi li trasformano in conoscenza per decidere.
- Nell'ERP l'integrazione è nativa; il suo vero vantaggio è rendere leggibili i processi trasversali e le loro disfunzioni, non solo unificare gli archivi.
- L'ERP ribalta il rapporto azienda-software: è l'azienda che si adatta ai modelli del sistema, e questo può essere un beneficio se quei modelli sono best practice.
- Personalizzare troppo un ERP compromette la comunicazione fra le parti e blocca l'aggiornamento alle nuove release.
- La differenza fra OLTP e OLAP non è tecnica ma di scopo: registrare correttamente le transazioni vs esplorare grandi volumi per decidere.
- La conoscenza tenuta segreta non genera vantaggio competitivo: il vantaggio sta nella velocità con cui la si traduce in azione.
- Il fattore critico di successo non è tecnologico: è la gestione del cambiamento, e la fretta è la prima causa di fallimento nelle PMI.

```schema
{"type":"flow","title":"Le tre direttrici del supporto ICT alla pianificazione e al controllo",
 "steps":[
  {"label":"1. Mettere a disposizione i dati di base","detail":"sistemi transazionali OLTP e sistemi integrati ERP\ntempestività, integrità, integrazione"},
  {"label":"2. Gestire dati e informazioni per le decisioni","detail":"Datawarehouse e Business Intelligence\naccesso multidimensionale, reporting, analisi ad hoc"},
  {"label":"3. Supportare la creazione di conoscenza","detail":"modelling e simulazione, Knowledge Data Discovery,\nStrategic Performance Management"}]}
```

```schema
{"type":"hierarchy","title":"Le quattro caratteristiche funzionali dei sistemi ERP","root":"ERP\nintegrazione «nativa»",
 "branches":[
  {"label":"Unicità della base dati","children":["Il dato è immesso una sola volta","e resta a disposizione di tutti","Separazione fra dati e procedure","Niente ridondanze né reporting non ufficiali"]},
  {"label":"Business model integrato","children":["Schema che ingloba tutte","le interconnessioni logiche","Rappresenta le best practice","→ base per la reingegnerizzazione"]},
  {"label":"Configurabilità","children":["Adattare il sistema alle proprie specificità","È una possibilità ma anche un obbligo","Compromesso fra esigenze aziendali","e opzioni concesse dal sistema"]},
  {"label":"Modularità","children":["Applicativi distinti per area","ma concepiti in modo unitario","Copertura incrementale possibile","ma attenzione alla propedeuticità dei moduli"]}],
 "note":"Il vero vantaggio è l'integrazione fra le unità coinvolte nei processi: rende leggibili i processi gestionali e le loro disfunzioni."}
```

```schema
{"type":"compare","title":"Sistemi OLTP e sistemi OLAP",
 "columns":["OLTP — transazionali","OLAP — analitici"],
 "rows":[
  ["Attività supportate","Di tipo operativo","Di tipo direzionale e strategico"],
  ["Orientamento","Process oriented","Subject oriented"],
  ["Utenti","Molti, interni ed esterni, simultaneamente","Pochi, interni, top e middle management"],
  ["Database","Prevalentemente relazionale","Prevalentemente multidimensionale"],
  ["Interrogazioni","Numerose, semplici e ripetitive","Poche, anche molto complesse"],
  ["Modalità di accesso","Inserimento, aggiornamento, cancellazione, lettura","Sola lettura"],
  ["Storicità dei dati","Dati attuali","Dati attuali e storici"],
  ["Aggiornamenti","Numerosi e frequenti","Poco frequenti, eseguiti off-line"],
  ["Affidabilità","Integrità e completezza delle transazioni","Completezza e accuratezza delle informazioni"]]}
```

```schema
{"type":"hierarchy","title":"Le quattro proprietà del Datawarehouse (Inmon)","root":"DATAWAREHOUSE\nhub dei flussi di dati aziendali",
 "branches":[
  {"label":"Orientamento al soggetto","children":["Dati strutturati per tipo di analisi","non per processo che li genera","Solo ciò che serve alle decisioni","La ridondanza è ammessa se semplifica"]},
  {"label":"Integrazione","children":["Dati da più ambienti transazionali","e da fonti esterne","Codifica uniforme","per omogeneità semantica"]},
  {"label":"Variabilità nel tempo","children":["Memorizza una serie di «fotografie»","snapshot o time stamp","Passato, presente e previsioni","L'ampiezza dell'intervallo è modificabile"]},
  {"label":"Non volatilità","children":["I dati non possono essere modificati","Sono ammesse solo interrogazioni","Riallineamento periodico off-line","con aggiornamento incrementale"]}]}
```

```schema
{"type":"matrix","title":"Le quattro funzioni OLAP di navigazione dei dati",
 "rows":["Roll up","Drill down","Slice & dice","Pivoting"],
 "cols":["Che cosa fa","Esempio"],
 "cells":[
  ["Risale la gerarchia delle dimensioni: aggregazione crescente","Dal fatturato giornaliero al settimanale, al mensile, all'annuale"],
  ["Esplode il dato aggregato in maggiore dettaglio","Dal fatturato complessivo a quello per area, regione, provincia, punto vendita"],
  ["Analizza porzioni specifiche dell'ipercubo su più dimensioni","Fatturato di settembre, prodotto X, Centro Italia, canale ingrosso"],
  ["Ri-orienta l'ipercubo offrendo viste diverse","Da clienti-su-prodotti a prodotti-su-clienti"]],
 "note":"Il drill across estende lo slice & dice: analisi trasversali su percorsi che variano di volta in volta."}
```

```schema
{"type":"flow","title":"Il processo KDD: dai dati grezzi alla conoscenza",
 "steps":[
  {"label":"Selezione","detail":"dai dati grezzi ai target data,\nsegmentati secondo criteri predefiniti"},
  {"label":"Preprocessing e data cleaning","detail":"eliminare errori, definire il comportamento\nin caso di dati mancanti, campionare"},
  {"label":"Trasformazione","detail":"conversioni di tipo, nuove variabili,\ncodifica omogenea di fonti diverse"},
  {"label":"DATA MINING","detail":"il cuore del processo: clustering, classificazione,\nregole di associazione, similarity search"},
  {"label":"Interpretazione e valutazione","detail":"non basta leggere i risultati:\nservono a validare dati e algoritmi"}],
 "note":"Processo interattivo (dialogo costante utente-software) e iterativo: si può tornare alle fasi preliminari."}
```

```schema
{"type":"tradeoff","title":"Adottare le nuove tecnologie: le due strade",
 "left":{"label":"LA FRETTA NELL'IMPLEMENTAZIONE","points":["Contesti aziendali impreparati al cambiamento","Competenze da recuperare «in corsa»","Rischio di sistemi troppo rigidi","Maggiori costi, inefficienze e forzature","Genera sfiducia verso lo strumento"]},
 "right":{"label":"L'APPROCCIO COME PROGETTO","points":["Analisi organizzativa as-is prima della scelta","Sensibilizzazione e formazione PRIMA dell'avvio","Tempi e responsabilità esplicitati","Investimento continuo nel capitale umano","Partecipazione attiva alla configurazione"]},
 "note":"L'adozione genera solo potenzialità di cambiamento: si realizzano se evolve in parallelo il contesto organizzativo e culturale."}
```

```schema
{"type":"cycle","title":"Le dieci buone regole per gestire il cambiamento",
 "steps":[
  {"label":"Commitment del vertice","detail":"sostenuto per tutta la durata e comunicato a ogni livello"},
  {"label":"Il cambiamento come occasione","detail":"non come imposizione tecnica"},
  {"label":"Approccio euristico","detail":"attento alle variabili sociali, politiche e culturali"},
  {"label":"Analisi organizzativa as-is","detail":"prima di scegliere il sistema"},
  {"label":"Condizioni organizzative","detail":"struttura, BPR, gruppi di lavoro interni"},
  {"label":"Partecipazione attiva","detail":"alla configurazione e all'implementazione"},
  {"label":"Comunicazione e formazione","detail":"che iniziano prima e continuano a regime"},
  {"label":"Motivazione continua","detail":"stimolare sempre attenzione e coinvolgimento"}]}
```
