# Capitolo 11 — L'analisi delle varianze a supporto del controllo di gestione
**Autrice:** Elena Giovannoni · **Parte:** Metodologie, strumenti ed esperienze

**In una frase:** scomporre uno scostamento globale nelle sue cause elementari serve a rispondere a una sola domanda — *di chi è la responsabilità, e su quale leva si può intervenire*.

## Obiettivi di apprendimento
Saper determinare e analizzare le varianze nei costi variabili, nei costi fissi, nel costo dei servizi tecnici e nei ricavi.

## Concetti chiave
- **Ciclo elementare di controllo** — tre momenti: definizione di standard; misurazione dei risultati rispetto agli standard; interventi correttivi sulla base della divergenza.
- **Varianza (o scostamento)** — **VAR = Vs − Ve**, differenza fra risultato atteso (standard, budget o risultato storico di riferimento) e risultato effettivo.
- **Varianza globale vs elementare** — le elementari derivano dalla scomposizione delle globali e forniscono le informazioni sulle **cause** e sulle **responsabilità**.
- **Varianza favorevole / sfavorevole** — per i costi: favorevole se **CS > CE** (VAR > 0). Per i ricavi il segno si legge al contrario: uno scostamento **negativo** significa ricavi effettivi superiori ai programmati, quindi **favorevole**.
- **Sotto/sopra-assorbimento dei costi fissi** — se il volume effettivo è minore del programmato i costi fissi unitari sono superiori a quelli di budget (*sotto-assorbimento*); se è maggiore, sono inferiori (*sopra-assorbimento*).

## Sviluppo

### 11.1-11.2 Che cosa fa e che cosa non fa l'analisi delle varianze
È «la manifestazione più saliente del controllo budgetario» (Bocchino). Consente valutazioni su quattro piani: andamento effettivo rispetto al desiderato; **cause** degli scostamenti; **attribuzione delle responsabilità**; provvedimenti correttivi.

**Cinque condizioni di efficacia:** *tempestività* (le disfunzioni vanno segnalate subito, per consentire azioni immediate); *periodicità* (verifiche a intervalli brevi); *omogeneità* dei dati, nei valori e nella rappresentazione formale; *analiticità*; presenza sia a **livello globale che elementare**.

**Tre limiti dichiarati:** l'uso prevalentemente quantitativo-monetario; la **scarsa selettività** rispetto alle variabili critiche; la minore efficacia in condizioni di instabilità.

> **L'avvertenza finale dell'autrice:** *«l'analisi delle varianze non deve limitarsi all'attribuzione delle responsabilità ma deve anche coinvolgere il management allo scopo di individuare le più opportune operazioni correttive».*

**Le sei operazioni del processo:** confronto atteso/effettivo → determinazione della varianza globale → scomposizione in varianze elementari → analisi delle elementari → individuazione delle cause e delle responsabilità → individuazione dei provvedimenti correttivi.

**L'albero della scomposizione.** Lo scostamento globale fra reddito programmato ed effettivo si scompone in varianze nei **ricavi**, nei **costi fissi** e nei **costi variabili**. A loro volta: i ricavi in volume, mix e prezzo di vendita; i costi fissi per tipologia di costo; i costi variabili in materie prime dirette, manodopera diretta e spese generali variabili — ciascuna riconducibile a variazioni di **volume**, **prezzo di acquisto** ed **efficienza**.

### 11.3 La varianza nei costi variabili

**Materie prime.** **VARm = (psm × Qsm) − (pem × Qem)**.
La stessa varianza può essere espressa in funzione dei **tre fattori** da cui dipende il costo totale di una risorsa: *volume dell'output*, *efficienza di impiego dell'input* (quantità fisica necessaria per unità di produzione) e *prezzo unitario dell'input*:

> (volume standard × consumo unitario standard × psm) − (volume effettivo × consumo unitario effettivo × pem)

**Perché questa seconda formulazione conta:** esprime le quantità in funzione del volume di output, e serve a **isolare la variazione di volume, che fa variare i costi variabili senza comportare necessariamente un peggioramento o un miglioramento in termini di efficienza**.

**Manodopera diretta** — stessa logica, con le ore al posto delle quantità e il salario orario al posto del prezzo.

### 11.4 La varianza nei costi fissi
Nella maggior parte dei casi **non è ulteriormente scomponibile**, perché non è determinabile uno standard unitario fisico. Si può però calcolare la **varianza di volume o di assorbimento**:

> **Costo fisso a budget − [(costo fisso a budget / volume a budget) × volume effettivo]**

*Esempio del capitolo (Tommy S.r.l.):* costi fissi a budget 10.000 €, volume a budget 100 stufe.
- Volume effettivo 90 → 10.000 − (100 × 90) = **+1.000 €: sotto-assorbimento**.
- Volume effettivo 110 → 10.000 − (100 × 110) = **−1.000 €: sopra-assorbimento**.

### 11.5 La varianza nel costo dei servizi tecnici
I costi dei servizi tecnici («spese generali tecniche») possono essere fissi (ammortamento di impianti e macchinari), variabili (forza motrice pagata a consumo) o misti. **Sono una voce rilevante nelle aziende di servizi, informatica, elettronica e nuove tecnologie**, dove questa analisi diventa fondamentale.

> Varianza = (**tasso unitario di assorbimento** × volume effettivo) − ammontare effettivamente sostenuto
> dove **tasso unitario di assorbimento = spese generali tecniche standard / volume di produzione standard**

Le spese generali tecniche si suddividono in: quelle **concernenti le materie** (accessorie o secondarie di lavorazione, combustibili, lubrificanti); quelle **concernenti il lavoro** (salari agli addetti a pulizie, trasporti interni, mensa, infermeria, magazzino); quelle **diverse** (illuminazione, riscaldamento, acqua, gas, telefono).

### 11.7 Le cause elementari — la scomposizione

**Nel costo delle materie prime, tre componenti:**

| Varianza | Formula | Origine | Responsabilità |
|---|---|---|---|
| **Di quantità (efficienza produttiva)** | VARm(q) = psm × (Qsm − Qem) | Interna, **controllabile** | Direzione tecnica |
| **Di prezzo di acquisto** | VARm(p) = Qsm × (psm − pem) | **Esterna, per lo più non controllabile** | Ufficio acquisti |
| **Congiunta** | VARm(c) = Δq × Δp | Compresenza delle due | — |

*Il metodo di isolamento:* per calcolare la varianza di quantità si **ipotizza che non esista varianza di prezzo** (psm = pem); per la varianza di prezzo si ipotizza che non esista varianza di quantità (Qsm = Qem). La **varianza congiunta** è ciò che resta: il prodotto fra la varianza unitaria di prezzo e la quantità eccedente quella standard.

**Nel costo della manodopera diretta, per analogia:**
- **Varianza di tempo (o di efficienza produttiva)** — dalla divergenza fra ore effettive e ore standard: **VARmd(h) = psmd × (hs − he)**. Origine **interna e controllabile**, responsabilità della **direzione tecnica**.
- **Varianza di tasso salariale** — dallo scostamento fra salario orario standard ed effettivo.
- **Varianza congiunta**.

### 11.6 e 11.8 La varianza nei ricavi

**Azienda monoprodotto — due componenti:**
> **Varianza di volume** = (volume standard × prezzo standard) − (volume effettivo × prezzo standard)
> **Varianza di prezzo** = (volume effettivo × prezzo standard) − (volume effettivo × prezzo effettivo)

*Esempio:* budget 3.000 unità a 14 €, consuntivo 2.500 a 13,9 €. Varianza totale 7.250 € = varianza di volume 7.000 € + varianza di prezzo 250 €.

*Caso Red S.r.l.:* budget 90.000 scatolette a 1 €, consuntivo 110.000 a 0,9 €. Varianza totale **−9.000 € (favorevole)**, scomposta in varianza di volume −20.000 € e varianza di prezzo +11.000 €. **La lettura è istruttiva:** il maggior volume ha più che compensato il prezzo più basso.

**Azienda pluriprodotto — tre componenti**, da determinare **per ciascun modello**. La sequenza è a cascata: si isola prima il volume tenendo fermi mix e prezzo standard, poi il mix tenendo fermo il prezzo standard, infine il prezzo.

> **Volume** = (volume programmato × % mix standard × prezzo standard) − (volume effettivo × % mix standard × prezzo standard)
> **Mix** = (volume effettivo × % mix standard × prezzo standard) − (volume effettivo × % mix effettivo × prezzo standard)
> **Prezzo** = (volume effettivo × % mix effettivo × prezzo standard) − (volume effettivo × % mix effettivo × prezzo effettivo)

**La varianza di mix** esprime lo scostamento dovuto alla suddivisione del volume totale delle vendite fra i diversi modelli. *Caso Gabry S.r.l. (giocattoli):* il volume complessivo effettivo coincide esattamente con quello programmato — 600 giocattoli — eppure i ricavi differiscono, perché sono cambiati il mix (tricicli dal 33,3% al 50,0%, cavalli a dondolo dal 16,7% all'8,3%) e i prezzi. **È il caso che dimostra perché la varianza di mix va isolata: senza di essa, uno scostamento a volumi invariati resterebbe inspiegato.**

## Punti da ricordare
- La varianza di quantità/tempo è interna e controllabile, quella di prezzo/tasso salariale è esterna: attribuire la seconda alla produzione è un errore ricorrente.
- Il segno della varianza si legge in modo opposto su costi e ricavi: sui ricavi il negativo è una buona notizia.
- La varianza di volume nei costi variabili non è di per sé un giudizio sull'efficienza: separarla è il primo passo di ogni analisi corretta.
- I costi fissi non hanno standard unitari fisici, quindi la loro scomposizione si ferma alla varianza di assorbimento.
- L'analisi che si esaurisce nell'attribuire colpe fallisce il proprio scopo: deve produrre azioni correttive.

```schema
{"type":"cycle","title":"Il ciclo elementare di controllo",
 "nodes":["1. Definizione degli obiettivi\ne degli standard","2. Decisioni\nle scelte più opportune al conseguimento","3. Azioni\ne risultati conseguiti","4. Rilevazione del divario\nfeedback fra obiettivi e risultati","5. Provvedimenti correttivi\nsulle azioni, sulle decisioni o sugli obiettivi"]}
```

```schema
{"type":"hierarchy","title":"L'albero di scomposizione della varianza globale","root":"SCOSTAMENTO DEL REDDITO",
 "branches":[
  {"label":"VARIANZA NEI RICAVI","children":["Di volume","Di mix (solo pluriprodotto)","Di prezzo di vendita"]},
  {"label":"VARIANZA NEI COSTI FISSI","children":["Per tipologia di costo","Varianza di volume o di assorbimento","Non ulteriormente scomponibile: manca lo standard unitario fisico"]},
  {"label":"VARIANZA NEI COSTI VARIABILI","children":["Materie prime dirette","Manodopera diretta","Spese generali variabili"]},
  {"label":"Cause elementari dei costi variabili","children":["Di volume","Di prezzo di acquisto / tasso salariale","Di efficienza (quantità o tempo)","Congiunta"]}]}
```

```schema
{"type":"compare","title":"Le cause elementari nei costi variabili: origine e responsabilità",
 "columns":["Formula","Origine","Responsabilità"],
 "rows":[
  ["MATERIE — varianza di quantità","psm × (Qsm − Qem)","Interna, controllabile","Direzione tecnica"],
  ["MATERIE — varianza di prezzo","Qsm × (psm − pem)","Esterna, per lo più non controllabile","Ufficio acquisti"],
  ["MATERIE — varianza congiunta","Δq × Δp","Compresenza delle due","—"],
  ["MOD — varianza di tempo","psmd × (hs − he)","Interna, controllabile","Direzione tecnica"],
  ["MOD — varianza di tasso salariale","hs × (psmd − pemd)","Esterna","Direzione del personale"],
  ["COSTI FISSI — varianza di assorbimento","CF − (CF/volume budget × volume effettivo)","Dipende dal volume realizzato","Direzione / area commerciale"]]}
```

```schema
{"type":"flow","title":"La scomposizione della varianza nei ricavi (azienda pluriprodotto)",
 "note":"Ogni passaggio tiene fermo ciò che precede: è questo che rende attribuibile ciascuna causa.",
 "steps":[
  {"label":"Varianza di VOLUME","detail":"si fa variare solo il volume complessivo\nmix e prezzo restano standard"},
  {"label":"Varianza di MIX","detail":"volume effettivo, si fa variare la composizione\nil prezzo resta standard"},
  {"label":"Varianza di PREZZO","detail":"volume e mix effettivi\nsi fa variare solo il prezzo"}]}
```

```schema
{"type":"matrix","title":"Come leggere il segno della varianza",
 "xaxis":["Su una voce di COSTO","Su una voce di RICAVO"],
 "yaxis":["Varianza NEGATIVA (Vs < Ve)","Varianza POSITIVA (Vs > Ve)"],
 "quadrants":[
  {"pos":"tl","label":"FAVOREVOLE","detail":"Costo effettivo inferiore allo standard"},
  {"pos":"tr","label":"SFAVOREVOLE","detail":"Ricavi effettivi inferiori ai programmati"},
  {"pos":"bl","label":"SFAVOREVOLE","detail":"Costo effettivo superiore allo standard"},
  {"pos":"br","label":"FAVOREVOLE","detail":"Ricavi effettivi superiori ai programmati"}]}
```

```schema
{"type":"flow","title":"Le sei operazioni dell'analisi delle varianze",
 "steps":[
  {"label":"1. Confronto","detail":"risultato atteso vs risultato conseguito"},
  {"label":"2. Varianza globale","detail":"VAR = Vs − Ve"},
  {"label":"3. Scomposizione","detail":"in varianze elementari"},
  {"label":"4. Analisi","detail":"delle varianze elementari"},
  {"label":"5. Cause e responsabilità","detail":"interne/controllabili vs esterne"},
  {"label":"6. Provvedimenti correttivi","detail":"il vero scopo dell'analisi"}]}
```
