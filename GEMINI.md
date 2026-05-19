# Agent Workflow Specification - pdf2cbz (Python Version)

Tu sei l'agente autonomo dedicato allo sviluppo, manutenzione e bug-fixing del progetto `pdf2cbz`. Il tuo obiettivo è risolvere il task assegnato in totale autonomia, garantendo la stabilità del codice esistente.

## 🛠️ Environment & Setup

Il progetto è un'applicazione Python. Prima di effettuare qualsiasi modifica o test, esegui i seguenti step di configurazione nel workspace per isolare l'ambiente:

1. **Creazione e attivazione Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Windows usa: venv\Scripts\activate

    Installazione Dipendenze:
    Bash

    pip install -r requirements.txt
    # Se presenti dipendenze di sviluppo o test:
    # pip install -r requirements-dev.txt o pip install -e .

   *Nota: Il tool manipola PDF e immagini (es. tramite `pdf2image`). Se noti errori legati a `poppler` non installato nel sistema, non tentare di usare `apt` o `brew`. Concentrati esclusivamente sulla logica del codice Python e sulla gestione dei pacchetti tramite pip.*

## 🧪 Verification Commands (Definition of Done)

Prima di dichiarare un task come completato con successo, DEVI eseguire rigorosamente questi comandi nell'ordine indicato. Se uno solo di questi comandi fallisce, il tuo task **non** è finito.

1. **Controllo Qualità e Tipo (Linter/Formattazione):**
   Esegui i tool di linting presenti nel progetto (es. `flake8`, `black`, o `mypy` se usati):
   ```bash
   #black --check .
   flake8 .
   

(Adatta il comando in base a cosa trovi installato nel file dei requisiti).

    Esecuzione Test Unitari:
    Bash

    pytest
    # Se pytest non è presente, usa il modulo nativo:
    # python -m unittest discover

   *Tutti i test devono ritornare un esito positivo (green) senza regressioni.*

## ⚠️ Regole di Ingaggio e Vincoli

Per evitare regressioni o modifiche distruttive, attieniti a queste linee guida:

- **Gestione dei File di Configurazione:** Non modificare `requirements.txt`, `setup.py` o `pyproject.toml` a meno che il task non richieda esplicitamente l'aggiunta o l'aggiornamento di una libreria.
- **Gestione dei File e Pulizia:** Trattandosi di un tool che estrae immagini da un PDF per poi zipparle in un `.cbz`, assicurati che il codice gestisca correttamente la pulizia delle cartelle temporanee (es. usando `tempfile` o svuotando le directory di lavoro) anche in caso di crash o eccezioni.
- **Robustezza ed Eccezioni:** Gestisci sempre gli errori tipici: PDF protetti da password, file corrotti, mancanza di permessi di scrittura nella cartella di destinazione.
- **Ciclo di Autocorrezione:** Se i test falliscono o il linter segnala errori, analizza l'output nel terminale, applica la correzione nel codice sorgente e riesegui i comandi di verifica.

## 📄 Output Richiesto

Una volta completato il task e superati tutti i comandi di verifica, genera un breve riepilogo in formato Markdown che descriva:
1. Quali file `.py` hai modificato.
2. Come hai risolto il problema o implementato la feature.
3. L'esito dell'esecuzione dei test (`pytest` / `unittest`).
