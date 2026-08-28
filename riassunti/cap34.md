# Capitolo 34 — La Business Intelligence a supporto del controllo di gestione

**Parte:** Parte IV — Casi ed esperienze

**In una frase:** La Business Intelligence si colloca sopra il datawarehouse e sotto le decisioni: integra i dati provenienti da fonti eterogenee, li trasforma in informazione tempestiva e univoca, e restituisce al controllo di gestione la capacità di analisi predittiva e di *data discovery* che i sistemi transazionali da soli non offrono — come mostra il caso ENTERPRISE-MEDIA S.p.A.

## Obiettivi di apprendimento

- Distinguere **dato** e **informazione**, e comprendere perché la gestione dell'informazione sia un asset intangibile critico.
- Classificare i sistemi informativi aziendali in **direzionali** e **operativi** secondo il modello Anthony-Simon, e conoscerne i principali applicativi.
- Definire la Business Intelligence, il suo ruolo nel controllo di gestione e i suoi rapporti con il BPM.
- Valutare vantaggi e ostacoli dell'implementazione di un sistema di BI.
- Ricostruire un percorso reale di *software selection* e implementazione, dalle sue motivazioni ai risultati attesi.

## Concetti chiave

- **Business Intelligence (definizione Gartner)** — «un sistema di modelli, metodi, processi, persone e strumenti che rendono possibile la raccolta regolare ed organizzata del patrimonio dei dati generato da un'azienda, permettendo mediante elaborazioni, analisi ed aggregazioni, la trasformazione in informazioni, la loro conseguente conservazione, reperibilità e presentazione in forma semplice, flessibile, personalizzata ed efficace, tale da costituire un supporto alle decisioni strategiche, tattiche, ma anche operative».
- **Dato vs informazione** — il dato è «materia prima ancora grezza e non lavorata»; l'informazione è il risultato di un processo di elaborazione e affinamento che ne svela il significato economico e strategico.
- **Sistemi informativi direzionali** — supportano decisioni mediamente strutturate (programmazione) e non strutturabili, usando dati e modelli matematici: **KMS**, **DSS**, **BI**.
- **Sistemi informativi operativi** — supportano attività completamente strutturate con strumenti standardizzati: **ERP**, **SCM**, **CRM**, **PDM**.
- **BPM — Business Performance Management** — termine spesso usato come sinonimo di BI: strumento di ottimizzazione dei risultati di business attraverso il miglioramento dei processi e il monitoraggio costante dei **KPI** (o KSI) definiti dal management.
- **Datawarehouse** — archivio informatico alimentato da tutti gli altri sistemi, progettato per produrre analisi e relazioni a fini decisionali. La BI si colloca **al di sopra** del datawarehouse.
- **Data discovery** — individuazione di legami e connessioni fra variabili complesse altrimenti impossibili da riscontrare, perché celate nell'immensa quantità di dati generati.
- **Text Mining / Agile BI / Social BI** — le tre direzioni evolutive: analisi di dati destrutturati con *semantic intelligence*; metodologia agile applicata ai progetti di BI per ridurre il *time-to-value*; analisi delle relazioni e delle conversazioni social per segmentare la clientela.

## Sviluppo

### 34.1 — Perché la BI incontra il controllo di gestione

Le sfide competitive tradizionali riguardavano costi, efficienza dei processi, qualità del prodotto, tempi di consegna. Con l'aumentare della complessità dei mercati le variabili rilevanti si sono moltiplicate: **gestione dei rischi e delle informazioni** e **tasso di innovazione** sono diventati priorità assolute. Diventa quindi fondamentale dotarsi di strumenti efficaci di gestione e controllo delle informazioni, tanto in sede di pianificazione quanto di verifica dei risultati.

Il legame con il controllo di gestione è diretto: il controllo si basa per sua natura su un sistema di dati costantemente in crescita e necessariamente dinamico; la BI **integra tutti i sistemi informativi presenti in azienda**, alimentandoli con dati e informazioni che costituiscono la base dei report a supporto delle decisioni e del monitoraggio.

### 34.2 — I sistemi informativi a supporto delle decisioni

Le fonti del vantaggio competitivo (Porter, 1985) si sono spostate da elementi materiali a risorse immateriali, investendo non solo i processi operativi ma le attività di **gestione dei dati e delle informazioni**. La corretta gestione, interpretazione e rendicontazione delle informazioni — interne ed esterne — può rappresentare un asset intangibile critico.

Gestire l'informazione comprende quattro attività: **elaborazione** dei dati per produrre informazioni significative; **archiviazione** dei dati grezzi e delle informazioni finali; **trasmissione**; **presentazione**. Questi flussi sono spesso una voce di costo rilevante in bilancio, ma contribuiscono in maniera significativa ai risultati di gestione, economico-finanziari e di efficienza/efficacia dei processi.

**Il modello Anthony-Simon.** Anthony (1965), integrato da Simon (1967), classifica i sistemi informativi in base al tipo di attività supportata:

| | Attività strategiche | Attività operative |
|---|---|---|
| **Competenza** | Alta Direzione | Middle management e base operativa |
| **Orizzonte** | Medio-lungo periodo | Breve periodo |
| **Natura delle decisioni** | Non strutturate (di cambiamento), in condizioni di rischio e incertezza | Non strutturate ma continuative (middle management); strutturate (unità operative) |
| **Discrezionalità** | Alta: richiede attitudine all'analisi e intuito | Scarsa |
| **Esempi** | Piano strategico, struttura organizzativa, rapporti con banche, acquisizione di commesse, decisioni di investimento | Fatturazione, gestione ordini e magazzino, rendicontazione dei costi |
| **Fabbisogno informativo** | Informazioni esterne (mercato, dinamiche macroeconomiche, trend di settore) e interne, consuntive e preventive | Prevalentemente interne: dati aziendali, di processo e di risultato; analitiche, tempestive, programmate, standardizzate |

**Gli applicativi direzionali:**

- **KMS** — *Knowledge Management System*: strumenti a sostegno di ricerca, identificazione e strutturazione del patrimonio informativo aziendale (per esempio i software di gestione documentale).
- **DSS** — *Decision Support System*: supporto al controllo direzionale e alla pianificazione strategica tramite informazioni di sintesi e cruscotti modificabili dagli utenti per formato e contenuto.
- **BI** — *Business Intelligence*: «l'insieme delle applicazioni, dell'infrastruttura, degli strumenti e delle migliori pratiche che consentono l'accesso e l'analisi delle informazioni per migliorare e ottimizzare le decisioni e le prestazioni» (Pasini, 2004).

**Gli applicativi operativi** (Camussone, 1990):

- **ERP** — *Enterprise Resource Planning*: forte integrazione fra tutte le aree, dagli ordini al bilancio, dalla fatturazione alla contabilità, dai pagamenti alle paghe.
- **SCM** — *Supply Chain Management*: automazione della catena di fornitura, trasmissione degli ordini, ottimizzazione delle scorte, analisi della domanda, piani di produzione, evasione e consegna.
- **CRM** — *Customer Relationship Management*: campagne di marketing, gestione vendite, post-vendita e customer service.
- **PDM** — *Product Development Management*: gestione dello sviluppo del prodotto.

**Il quadro sinottico per area aziendale** (Tavola 34.1) mostra che **la BI compare in tutte le aree**, mentre gli altri applicativi si distribuiscono per specializzazione:

| Area | Attività del sistema informativo | Applicativi |
|---|---|---|
| Amministrazione e Controllo | Informazioni amministrative; sintesi per il controllo dell'andamento; informazioni per stakeholder esterni | BI, ERP, DSS, KMS |
| Finanza | Calcolo della liquidità disponibile; valutazione degli impieghi; supporto alle decisioni di investimento; controllo della gestione finanziaria | BI, ERP, DSS |
| R&S | Monitoraggio delle operazioni con metodi di Project Management; informazioni ai ricercatori su innovazioni tecnologiche | BI, KMS |
| Logistica | Database e report acquisti, dalla selezione fornitori al controllo consegne; gestione magazzino (scorta ottima, riordino, lotto di sicurezza); scelta dei trasportatori | BI, ERP, SCM |
| Produzione | Progettazione industriale e dati tecnici via BOM; programmazione via MRP; lancio e avanzamento; manutenzione impianti | BI, ERP, SCM, PDM |
| Commerciale | Analisi delle vendite; report sull'andamento del mercato; previsioni con modelli intrinseci (serie storiche) o estrinseci (correlazione) | BI, ERP, CRM |
| Risorse Umane | Calcolo di paghe e stipendi | BI, ERP |

### 34.3 — La Business Intelligence nel controllo di gestione

La BI è uno strumento strategico di **integrazione dei processi**, che supporta il management nelle decisioni e consente simulazioni, analisi e previsioni di natura economico-finanziaria, strategica, di efficienza interna e anche qualitativa. È usata anche per prevedere i trend di mercato individuando legami fra le variabili complesse dei diversi business.

Chi la usa e chi la gestisce sono soggetti distinti: **i principali utilizzatori sono i manager**, mentre i gestori del sistema di reportistica e analisi sono **gli uffici di Programmazione e Controllo**, che fanno da ponte fra l'impresa e i manager selezionando le informazioni più rilevanti per il processo decisorio.

Il fattore critico di successo è la **tempestività**: un controllo capillare e *in real time* dell'andamento del business consente rapide azioni correttive (Azvine et al., 2006). La BI permette un'attività di controllo semi-automatica, a basso costo, professionale, adattabile alle specifiche esigenze della gestione e fortemente flessibile.

Più nel dettaglio, la BI (Falduto e Ruscica, 2005): assiste i vertici nel comprendere il reale stato di salute dell'impresa; supporta il processo decisionale direzionale; rintraccia in quale area potrebbero nascondersi criticità; traccia la reale efficienza dei processi produttivi. Ne discende la possibilità di gestire più facilmente operazioni come il controllo dei costi di prodotto, l'apertura di una nuova linea, il mantenimento o l'eliminazione di prodotti dalla gamma, le scelte di *make or buy*.

**Vantaggi dell'implementazione:**

- **Monitoraggio del mercato** — visione analitica e integrata, con analisi che incrociano variabili da fonti differenti; velocizzazione dell'accesso a report e analisi.
- **Supporto al processo decisionale** — maggiore tempestività nell'implementazione di scelte di successo; **analisi predittive** per minimizzare i rischi e massimizzare la performance.
- **Gestione del patrimonio informativo** — grazie al datawarehouse, ciascun report esprime **una visione univoca**: uniformità delle informazioni, niente duplicazioni, razionalizzazione del patrimonio informativo.
- **Automazione** di processi e strumenti di reporting: risparmio di tempo e di costi.
- **Indipendenza degli utenti finali dal dipartimento IT** nella produzione della reportistica, grazie a cruscotti personalizzabili su istanza e a interfacce intuitive.
- **Vantaggi tecnici** — gestione del magazzino, individuazione dei colli di bottiglia nei processi, riallocazione efficiente delle risorse, miglioramento del servizio alla clientela.

**Ostacoli:**

- **Mancato commitment del top management** e **resistenza culturale al cambiamento** del personale: le organizzazioni sono per natura restie a interventi tecnologicamente *disruptive*, che creano problemi di adattamento ad alcune fasce di dipendenti (Fontana, 1993).
- **Percezione iniziale di costi eccessivi e onerosità in termini di tempo**: la sola creazione del datawarehouse richiede **più di un anno**, dovendo comprendere la pulizia dei dati e la costruzione dei nuovi database operativi — con possibili differimenti che «potrebbero anche minare il raggiungimento degli obiettivi prefissati» (Pasini et al., 2004).
- **Ingenti competenze specialistiche** richieste in fase di avvio e di gestione del progetto, sia all'IT sia a tutto il personale.

**Le tre prospettive evolutive:**

- **Text Mining** — data mining su dati destrutturati configurati in testi liberi; l'attenzione si concentra sulla risoluzione delle ambiguità linguistiche (parole omonime) con sistemi di *semantic intelligence* che scompongono le frasi nelle parti elementari e lemmatizzano parole ed espressioni.
- **Agile BI** — applicazione della metodologia agile ai progetti di BI per ridurre il *time-to-value*. Funziona per iterazioni: le nuove funzionalità arrivano agli utenti finali prima che nel processo a cascata tradizionale, i requisiti e la progettazione si sovrappongono allo sviluppo, i cicli di consegna si accorciano. Favorisce pianificazione adattiva, sviluppo evolutivo e consegna incrementale, con un basso **Total Change Cost**.
- **Social BI** — identifica relazioni e transazioni con i clienti raggruppandoli per legami altrimenti sommersi, e fornisce automaticamente informazioni su gusti e discussioni social. Consente di: comprendere la percezione che clienti e stakeholder hanno dell'impresa; individuare e influenzare gli *opinion leader*; sfruttare il marketing virale per sviluppare il business e contenere il rischio; segmentare meglio la clientela; aumentare la fedeltà dei clienti ad alto valore e basso rischio a costi inferiori; acquisire nuova clientela.

### 34.4 — Il caso ENTERPRISE-MEDIA S.p.A.

**Chi è.** Grande impresa italiana del settore media (nome fittizio), **concessionaria di pubblicità**: intermedia fra editori e agenzie, vendendo ai centri media — o talvolta direttamente agli inserzionisti — gli spazi pubblicitari messi a disposizione dai mezzi di comunicazione. Nel contesto italiano coesistono concessionarie **verticalmente integrate** con il gruppo editoriale (come questa, nata da un processo di esternalizzazione) e soggetti indipendenti.

*Mission*: valorizzare i contenuti del proprio editore esaltandone le potenzialità pubblicitarie, ottimizzando costantemente l'offerta in funzione della migliore redditività degli investimenti e della coerenza con i contenuti editoriali. Il piano strategico ha posto al centro **innovazione e sperimentazione**.

*Contesto*: trend economico-finanziario negativo negli ultimi anni, severa contrazione degli investimenti pubblicitari, ingresso di nuovi player che ha inasprito la competizione minacciando la solidità degli incumbent. Le strutture specializzate per mezzo consentono economie di scala ma «talvolta generano una sovrabbondanza di informazioni spesso difficili da gestire».

**Il sistema informativo preesistente**, articolato in quattro aree:

| Area | Contenuto |
|---|---|
| **Sistemi contabili** | **SAP** (ERP) per contabilità generale, clienti e fornitori, gestione del credito, del patrimonio e degli approvvigionamenti; gestito centralmente dalla controllante per omogeneità e comparabilità del dato. Si interfaccia con **Sipert** per i costi del personale (unico pacchetto di mercato acquistato direttamente, usato dalle Risorse Umane) |
| **Sistemi commerciali** | «Il cuore dell'attività»: distinti per mezzo, sono veri e propri magazzini di spazi — misurati **in secondi** — disponibili alla vendita. Il processo "produttivo" li prenota, pulisce, ordina e li consegna alla messa in onda; i dati alimentano poi la fatturazione e quindi le provvigioni degli agenti |
| **Anagrafiche e supporto** | Nomi e riferimenti di clienti, prodotti pubblicitari, venditori, agenti, intermediari (Centri Media e agenzie). A queste si affianca l'anagrafica **Nielsen**: recepita automaticamente, va mappata e confrontata con le informazioni interne perché le codifiche differiscono, per estrarre dati incrociati utili ad analisi prospettiche, differenziali e valutazioni strategiche |
| **Datawarehouse** | Organizzato in quattro moduli: supporto alle vendite; analisi della concorrenza; reporting e monitoraggio andamenti; analisi del credito. È la fonte di tutte le analisi consuntive e di pianificazione |

Dal 1998 la Società ha investito nella **customizzazione** dei sistemi — soprattutto quelli commerciali TV e le anagrafiche — non ritenendo i pacchetti standard idonei alle esigenze del mercato. Ma alcuni dati e flussi non sono direttamente tracciati nel datawarehouse: è **questa lacuna** una delle ragioni alla base dell'adozione della BI.

**Le motivazioni del progetto (2016).**

1. **Complessità crescente del contesto competitivo.** Il mercato pubblicitario è fortemente dinamico e i nuovi media hanno eroso le marginalità dei settori tradizionali. Soprattutto è cambiato l'utente: dal sistema classico dei media — mezzi separati, flusso unidirezionale, tempi di consumo chiari come gli orari del palinsesto lineare — si è passati a un **ecosistema digitale iper-connesso**, in cui l'utente sta al centro di un sistema integrato di media audiovisivi, di un'offerta esponenzialmente più ampia, di una «rete di reti» fissa e mobile e di una pluralità di social network che rendono **orizzontale** la circolazione della comunicazione.
2. **La politica della capogruppo**, che investe per divenire una vera *Media-Company*, agendo su linguaggio, layout e applicazioni.
3. **L'esigenza di una gestione univoca dell'informazione.** Nelle parole del management: serve una reportistica che dica «la stessa cosa» e sappia guardare al numero con lo «stesso occhio». Il progetto passa da una valutazione **segmentata e a volte non dialogante** del business a una **olistica e integrata**.

**Il percorso di implementazione**, articolato in tre macro-attività parallele:

**Fase 1 — Mappatura dell'intera reportistica.** Interviste a tutti gli *owner* dei processi di reportistica; analisi di tutti i report per comprendere le criticità del sistema attuale; reingegnerizzazione del sistema di reporting. Per ogni report si è indagato contenuto, KPI misurati, **grado di automazione**, lista di distribuzione e sistemi informativi usati per l'estrazione. Obiettivo: individuare sovrapposizioni, duplicazioni e lacune prima della migrazione.

**Fase 2 — Software selection.** Non avendo esperienza pregressa in materia, la Società è partita dal **Quadrante Magico di Gartner** e dalla **Forrester Wave** per una panoramica dei provider, con confronto diretto con gli analisti Gartner. Il campo è stato circoscritto a tre sistemi: **Qlik Sense, Tableau, Microsoft BI**, valutati con indicatori di performance pesati per rilevanza. Fra gli indicatori: scalabilità della piattaforma con ottimizzazione delle performance; capacità di usare dati strutturati e non; facilità d'uso; strumenti per condividere lo stesso sistema di record, gli stessi modelli semantici e metadati; output grafici, chart e tabelle interattive; piena fruibilità su smartphone e tablet; **indipendenza degli utenti** nella realizzazione di report e analisi; funzioni di accesso, interazione, trasformazione e caricamento dei dati in uno strato di archiviazione autonomo con indicizzazione e pianificazione degli aggiornamenti.

> Un esito significativo: **Microsoft BI** risulta più adatto se si desidera una BI **centralizzata**; **Qlik Sense** e **Tableau** se si cerca l'**indipendenza degli utenti dal dipartimento IT** nella produzione dei report e nell'esplorazione di trend e dati.

Un'analisi dei costi — distinti in fissi e variabili, per acquisto, manutenzione e numero di utenze simultanee — ha completato la valutazione. Nell'ottica di bilanciamento fra esigenze degli utenti e necessità dell'IT è stato scelto **Qlik Sense**.

**Fase 3 — Benchmark internazionale.** Questionario di 9 domande inviato dall'International Relations Manager ai membri dell'Associazione Europea per il Marketing di Soluzioni Pubblicitarie: quale tool è usato e in quale versione; perché è stato scelto; come lo si valuta; ambiti e finalità (reportistica, data discovery, analisi predittive); aree oggetto di analisi; settori e figure aziendali che lo usano; da quanto tempo è attivo; quanto è autonoma l'utenza finale; risultati e benefici misurabili.

Hanno risposto **18 aziende** da Austria, Canada, Repubblica Ceca, Germania, Francia, Croazia, Islanda, Kazakhistan, Lettonia, Paesi Bassi, Norvegia, Polonia, Svezia, Ucraina e a livello europeo. Emerge che le imprese esaminate avevano avviato i primi sistemi già a inizio anni Duemila con ERP integrati che prevedevano soluzioni di BI (**Oracle BI**, **SAS**): funzionali per i report consolidati, ma non per la **data discovery**, che richiede software più agili e flessibili.

Risultati del benchmark:

- Nelle **11 imprese** che hanno adottato la BI si è registrato un sensibile incremento dell'autonomia dell'utenza finale nella realizzazione di report e dashboard; nel **73%** dei casi l'autosufficienza è **totale**.
- Aree di utilizzo: **Vendite 45%**, l'**intera società 24%**, **Marketing 18%**, **Finanza 10%**, altre funzioni 3%.
- Benefici misurabili: incremento della trasparenza fra dipartimenti; condivisione di KPI e dati in tutta l'impresa; maggiore consapevolezza delle proprie attività; miglior focus strategico sulla programmazione dei flussi finanziari; miglior controllo dell'*inventory*; miglioramento delle vendite; monitoraggio analitico delle attività; creazione di sinergie e **riduzione dell'organico dedicato al reporting**.
- Tutte le aziende intervistate si sono dichiarate **fortemente soddisfatte** e pronte a espandere gli applicativi.

**I risultati attesi.** Il primo risultato raggiunto è stato **razionalizzare l'informazione prodotta**, che presentava limiti evidenti: ridondanza e sovrapposizione; tempi di produzione troppo lunghi e non allineati alle esigenze dei decisori; report che, pur misurando variabili identiche, usavano criteri e strumenti fortemente differenti, «creando una forte disomogeneità nel dato finale». L'obiettivo è un'**uniformità che non vada a discapito della specializzazione dei singoli dipartimenti**.

Sul piano analitico, la BI abilita: *Analytics Predictions* — previsioni su serie temporali per anticipare l'andamento delle vendite, profilare meglio la clientela, prevedere l'andamento delle campagne incrociando serie storiche, valori del listino e andamento del mercato; e *Data Discovery* — miglior visualizzazione grafica e individuazione di legami fra variabili complesse celati nella massa dei dati.

Sul piano organizzativo: una volta **automatizzata la reportistica operativa**, le risorse liberate possono essere formate per sviluppare nuove competenze di gestione e interpretazione del software e dei dati.

### 34.5 — Riflessioni conclusive

La BI è diventata uno strumento **strategico**: integra i processi aziendali per trarre il massimo beneficio dal patrimonio informativo, risorsa intangibile ormai imprescindibile per la competitività e per la performance. I vantaggi non sono solo di integrazione dei sistemi ma **strategici**: la visione analitica e integrata incrementa attenzione ed efficacia del management, incrociando variabili di fonti differenti e individuando relazioni di dipendenza e prospettive previsionali.

Il progetto in ENTERPRISE-MEDIA è stato **avviato dal top management**, profondamente convinto dei vantaggi. Il punto di partenza sono state le lacune nella gestione dell'informazione: non efficace, ridondante, non univoca, generatrice di report «mal utilizzati e mai condivisi». La risposta è stata **ridisegnare il sistema di reporting** rendendolo coerente con la vision aziendale, introducendo Qlik Sense per comprimere i tempi di produzione dei report standard, statici e a basso valore aggiunto e per rendere condivisibile una maggiore quantità di dati.

Tre linee di risultato attese:

1. **Risorse umane** — sostituzione delle attività a bassa marginalità con attività a maggior valore aggiunto, con riposizionamenti e percorsi di formazione: se ne attende un forte incremento di soddisfazione e motivazione.
2. **Architettura informativa** — un sistema realmente integrato: il software si colloca **al di sopra degli ERP e dei sistemi gestionali**, e alla sua base sta il datawarehouse. Molte analisi oggi irrealizzabili diventano possibili, con maggior dettaglio e profondità e percorsi di data discovery.
3. **Controllo di gestione** — strumenti completi e dinamici anche per analisi prospettiche: le analisi previsionali abilitano un **controllo ex ante** sulle principali dinamiche di interesse, con azioni correttive immediate.

In definitiva, il sistema informativo può fornire un supporto reale alle decisioni strategiche solo in presenza di una **vision aziendale realmente condivisa** fra tutti i membri dell'organizzazione.

## Casi

- **ENTERPRISE-MEDIA S.p.A.** — concessionaria di pubblicità italiana di grandi dimensioni, verticalmente integrata con il proprio gruppo editoriale. Progetto BI avviato nel 2016; sistemi preesistenti SAP + Sipert + sistemi commerciali customizzati + anagrafiche interne e Nielsen + datawarehouse a quattro moduli. Software selezionato: **Qlik Sense**, dopo confronto con Tableau e Microsoft BI.
- **Benchmark internazionale** — 18 broadcaster e concessionarie europee ed extra-europee: prime adozioni a inizio anni Duemila con Oracle BI e SAS integrati negli ERP; limite comune, l'inadeguatezza alla data discovery.

## Punti da ricordare

- **Il dato non è informazione**: fra i due c'è un processo di elaborazione che ne svela il significato economico e strategico. Gestire quel processo è ormai attività critica nella creazione di valore.
- Il modello **Anthony-Simon** separa attività strategiche (decisioni non strutturate, orizzonte lungo, informazioni anche esterne) e operative (decisioni strutturate, orizzonte breve, informazioni interne, analitiche e standardizzate) — e con esse i sistemi che le supportano.
- **Direzionali** (KMS, DSS, BI) e **operativi** (ERP, SCM, CRM, PDM): la BI è l'unico applicativo presente in *tutte* le aree aziendali.
- La BI si colloca **sopra il datawarehouse e sopra gli ERP**: non li sostituisce, li integra e ne estrae ciò che essi da soli non producono — data discovery e analisi predittiva.
- Il fattore critico è la **tempestività**: un controllo *real time* consente azioni correttive rapide e trasforma il controllo di gestione da consuntivo a **ex ante**.
- Il beneficio più citato non è tecnico ma organizzativo: **una visione univoca del dato** — report che «dicono la stessa cosa» — e l'**indipendenza degli utenti dall'IT**.
- Gli ostacoli sono anch'essi organizzativi prima che tecnici: **mancato commitment del vertice** e **resistenza culturale**; sul piano tecnico, un datawarehouse richiede più di un anno e competenze specialistiche significative.
- **Mappare la reportistica esistente prima di migrare** è il passaggio metodologico decisivo: senza reingegnerizzazione, la BI automatizza le ridondanze invece di eliminarle.
- La scelta del software non è neutra rispetto al modello organizzativo: **BI centralizzata** (Microsoft BI) contro **autonomia dell'utente finale** (Qlik Sense, Tableau).
- Le direzioni evolutive — **Text Mining, Agile BI, Social BI** — spostano la BI verso i dati destrutturati, i cicli di rilascio brevi e le fonti esterne conversazionali.
- L'automazione della reportistica operativa libera risorse: il risultato atteso non è solo il risparmio, ma la **riqualificazione del personale** verso attività a maggior valore aggiunto.

```schema
{
  "type": "hierarchy",
  "title": "I sistemi informativi aziendali secondo il modello Anthony-Simon",
  "root": "SISTEMI INFORMATIVI AZIENDALI",
  "branches": [
    {"label": "DIREZIONALI\n(attività strategiche)", "children": ["KMS — Knowledge Management System", "DSS — Decision Support System", "BI — Business Intelligence"]},
    {"label": "OPERATIVI\n(attività operative)", "children": ["ERP — Enterprise Resource Planning", "SCM — Supply Chain Management", "CRM — Customer Relationship Management", "PDM — Product Development Management"]}
  ],
  "note": "La BI è l'unico applicativo che compare in tutte le aree aziendali del quadro sinottico (Tavola 34.1)."
}
```

```schema
{
  "type": "compare",
  "title": "Attività strategiche e attività operative: due fabbisogni informativi",
  "columns": ["Attività strategiche", "Attività operative"],
  "rows": [
    {"label": "Competenza", "cells": ["Alta Direzione", "Middle management e base operativa"]},
    {"label": "Orizzonte temporale", "cells": ["Medio-lungo periodo", "Breve periodo"]},
    {"label": "Tipo di decisione", "cells": ["Non strutturate, di cambiamento, in rischio e incertezza", "Non strutturate continuative; strutturate"]},
    {"label": "Discrezionalità", "cells": ["Alta: analisi e intuito", "Scarsa"]},
    {"label": "Fonte delle informazioni", "cells": ["Esterne (mercato, macro, trend di settore) e interne", "Prevalentemente interne: processo e risultato"]},
    {"label": "Qualità richieste", "cells": ["Consuntive e preventive, di sintesi", "Analitiche, tempestive, programmate, standardizzate"]},
    {"label": "Esempi", "cells": ["Piano strategico, struttura organizzativa, investimenti, rapporti con le banche", "Fatturazione, ordini, magazzino, rendicontazione dei costi"]}
  ]
}
```

```schema
{
  "type": "flow",
  "title": "Dal dato alla decisione: dove si colloca la Business Intelligence",
  "steps": [
    {"label": "Sistemi transazionali", "detail": "ERP, SCM, CRM, PDM: generano il dato grezzo della gestione corrente"},
    {"label": "Fonti esterne", "detail": "anagrafiche di mercato (es. Nielsen), dinamiche macro, trend di settore, social"},
    {"label": "Datawarehouse", "detail": "archivio unico alimentato da tutti i sistemi, progettato per l'analisi"},
    {"label": "Business Intelligence", "detail": "si colloca al di sopra: elaborazione, aggregazione, data discovery, analisi predittiva"},
    {"label": "Reportistica e cruscotti", "detail": "visione univoca, personalizzabile, indipendente dal dipartimento IT"},
    {"label": "Decisioni e azioni correttive", "detail": "controllo ex ante, concomitante e consuntivo in tempo reale"}
  ]
}
```

```schema
{
  "type": "tradeoff",
  "title": "Implementare un sistema di BI: vantaggi e ostacoli",
  "left": {
    "label": "VANTAGGI",
    "points": [
      "Visione analitica e integrata: incrocio di variabili da fonti differenti",
      "Tempestività delle decisioni e analisi predittive",
      "Visione univoca del dato: niente duplicazioni, patrimonio informativo razionalizzato",
      "Automazione del reporting: risparmio di tempo e di costi",
      "Indipendenza degli utenti finali dal dipartimento IT",
      "Vantaggi tecnici: magazzino, colli di bottiglia, riallocazione risorse, servizio al cliente"
    ]
  },
  "right": {
    "label": "OSTACOLI",
    "points": [
      "Mancato commitment del top management",
      "Resistenza culturale al cambiamento del personale",
      "Percezione iniziale di costi di gestione eccessivi",
      "Il datawarehouse richiede più di un anno: pulizia dei dati e nuovi database",
      "Imprevisti che possono minare gli obiettivi prefissati",
      "Ingenti competenze specialistiche, all'IT e a tutto il personale"
    ]
  }
}
```

```schema
{
  "type": "cycle",
  "title": "Le quattro attività della gestione dell'informazione",
  "nodes": [
    "Elaborazione\ndai dati grezzi\nalle informazioni significative",
    "Archiviazione\ndati grezzi\ne informazioni finali",
    "Trasmissione\nverso i destinatari\ninterni ed esterni",
    "Presentazione\nin forma semplice,\nflessibile, personalizzata"
  ]
}
```

```schema
{
  "type": "flow",
  "title": "Il percorso di implementazione in ENTERPRISE-MEDIA S.p.A.",
  "steps": [
    {"label": "Fase 1 — Mappatura della reportistica", "detail": "interviste agli owner, analisi dei report, reingegnerizzazione del sistema"},
    {"label": "Fase 2 — Software selection", "detail": "Gartner Magic Quadrant e Forrester Wave; short list Qlik Sense, Tableau, Microsoft BI"},
    {"label": "Misurazione delle capabilities", "detail": "indicatori pesati per rilevanza; test dei tre software; analisi costi fissi e variabili"},
    {"label": "Fase 3 — Benchmark internazionale", "detail": "questionario a 18 broadcaster e concessionarie europee ed extra-europee"},
    {"label": "Scelta e acquisto", "detail": "Qlik Sense, per bilanciare esigenze degli utenti e necessità dell'IT"},
    {"label": "Razionalizzazione dell'informazione", "detail": "eliminazione di ridondanze, allineamento dei tempi, omogeneità dei criteri"}
  ]
}
```

```schema
{
  "type": "matrix",
  "title": "Il sistema informativo di ENTERPRISE-MEDIA prima della BI",
  "rows": ["Sistemi contabili", "Sistemi commerciali", "Anagrafiche e supporto", "Datawarehouse"],
  "cols": ["Contenuto", "Criticità"],
  "cells": [
    ["SAP per contabilità generale, credito, patrimonio e approvvigionamenti; Sipert per i costi del personale", "SAP gestito centralmente dalla controllante: omogeneità a scapito della specificità"],
    ["Magazzini di spazi pubblicitari misurati in secondi, distinti per mezzo; alimentano fatturazione e provvigioni", "Forte customizzazione dal 1998; strutture per mezzo che generano sovrabbondanza informativa"],
    ["Clienti, prodotti, venditori, agenti, Centri Media; anagrafica Nielsen recepita automaticamente", "Codifiche Nielsen diverse da quelle interne: necessario un lavoro di mappatura e confronto"],
    ["Quattro moduli: supporto vendite, analisi concorrenza, reporting e monitoraggio, analisi del credito", "Alcuni dati e flussi non sono tracciati: è la ragione principale dell'adozione della BI"]
  ]
}
```

```schema
{
  "type": "matrix",
  "title": "La software selection: che cosa distingue i tre candidati",
  "rows": ["Microsoft BI", "Qlik Sense", "Tableau"],
  "cols": ["Vocazione", "Adatto quando"],
  "cells": [
    ["BI centralizzata, governata dal dipartimento IT", "L'azienda vuole un presidio unico e procedure omogenee sul dato"],
    ["Autonomia dell'utente finale nella produzione dei report — scelto da ENTERPRISE-MEDIA", "Si cerca indipendenza dall'IT nell'esplorazione di trend e dati, bilanciata con le esigenze IT"],
    ["Autonomia dell'utente finale, forte enfasi sulla visualizzazione", "Priorità alla data discovery e agli output grafici interattivi"]
  ],
  "note": "Indicatori di valutazione pesati: scalabilità, dati strutturati e non, usabilità, modelli semantici condivisi, output grafici, fruibilità mobile, indipendenza dell'utente, funzioni ETL e indicizzazione."
}
```

```schema
{
  "type": "pyramid",
  "title": "I risultati del benchmark internazionale (18 rispondenti)",
  "levels": [
    {"label": "Autonomia dell'utenza finale", "detail": "Incremento sensibile in tutte le 11 imprese che hanno adottato la BI; autosufficienza totale nel 73% dei casi"},
    {"label": "Aree di utilizzo", "detail": "Vendite 45% · intera società 24% · Marketing 18% · Finanza 10% · altre funzioni 3%"},
    {"label": "Benefici misurabili", "detail": "Trasparenza fra dipartimenti, KPI condivisi, focus sui flussi finanziari, controllo dell'inventory, sinergie e riduzione dell'organico sul reporting"}
  ]
}
```

```schema
{
  "type": "hierarchy",
  "title": "Le tre prospettive evolutive della Business Intelligence",
  "root": "EVOLUZIONE DELLA BI",
  "branches": [
    {"label": "Text Mining", "children": ["Data mining su dati destrutturati", "Testi liberi e ambiguità linguistiche", "Semantic intelligence e lemmatizzazione"]},
    {"label": "Agile BI", "children": ["Metodologia agile applicata ai progetti di BI", "Requisiti e progettazione sovrapposti allo sviluppo", "Cicli di consegna più rapidi, basso Total Change Cost"]},
    {"label": "Social BI", "children": ["Relazioni e legami sommersi fra clienti", "Percezione dell'impresa e opinion leader", "Segmentazione e marketing virale", "Fedeltà dei clienti ad alto valore, basso rischio"]}
  ]
}
```

```schema
{
  "type": "flow",
  "title": "Perché il progetto è nato: dalle criticità agli obiettivi",
  "steps": [
    {"label": "Informazione ridondante e non univoca", "detail": "report che misurano le stesse variabili con criteri diversi; documenti mal utilizzati e mai condivisi"},
    {"label": "Tempi non allineati ai decisori", "detail": "produzione troppo lunga rispetto alla dinamicità del mercato pubblicitario"},
    {"label": "Ecosistema digitale iper-connesso", "detail": "fine del palinsesto lineare; utente al centro di media integrati e circolazione orizzontale"},
    {"label": "Mappatura e reingegnerizzazione", "detail": "categorizzare tutti i report, individuare sovrapposizioni, duplicazioni e lacune"},
    {"label": "Reportistica integrata e univoca", "detail": "«la stessa cosa», guardata con lo «stesso occhio», senza sacrificare la specializzazione"},
    {"label": "Analytics predittive e data discovery", "detail": "controllo ex ante sulle dinamiche di interesse, azioni correttive immediate"}
  ]
}
```
