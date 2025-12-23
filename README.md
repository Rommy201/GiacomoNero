# 🃏 Blackjack Assistant

Applicazione Python con interfaccia grafica per supportare il gioco del Blackjack con card counting e suggerimenti strategici in tempo reale.

## 📋 Funzionalità

- **Card Counting** con sistema Hi-Lo
- **Running Count** e **True Count** in tempo reale
- **Suggerimenti strategici** basati sulla strategia di base ottimale
- **Aggiustamenti dinamici** della strategia in base al conteggio carte
- **Interfaccia grafica** intuitiva e facile da usare
- **Supporto multi-mazzo** (1-8 mazzi)

## 🚀 Come Usare

### Installazione

1. Assicurati di avere Python 3.7 o superiore installato
2. Tkinter è incluso nella maggior parte delle installazioni Python

```bash
python --version  # Verifica versione Python
```

### Avvio

```bash
python main.py
```

## 📖 Guida all'Uso

### Setup Iniziale

1. **Imposta i mazzi**: Specifica quanti mazzi sono in gioco (tipicamente 6 o 8 nei casinò)
2. Il conteggio parte da 0

### Durante il Gioco

1. **Carta del Banco**: Seleziona e imposta la carta scoperta del dealer
2. **Le tue carte**: Aggiungi le tue carte una alla volta
3. **Altre carte al tavolo**: Se vedi carte di altri giocatori, aggiungile al conteggio con "Aggiungi Altra Carta"
4. **Leggi il suggerimento**: L'app ti dirà cosa fare (Hit, Stand, Double, Split)

### Azioni

- **👊 HIT**: Chiedi un'altra carta
- **✋ STAND**: Mantieni la mano attuale
- **💰 DOUBLE**: Raddoppia la puntata (ricevi una sola carta)
- **✂️ SPLIT**: Dividi una coppia in due mani
- **🏳️ SURRENDER**: Arrenditi (recuperi metà puntata)

### Card Counting

#### Sistema Hi-Lo

- **Carte basse (2-6)**: +1
- **Carte neutre (7-9)**: 0
- **Carte alte (10-K, A)**: -1

#### Running Count vs True Count

- **Running Count**: Somma di tutte le carte viste
- **True Count**: Running Count diviso per i mazzi rimanenti stimati
- **Importanza**: Il True Count è più accurato per decisioni strategiche

#### Interpretazione

- **TC > +2**: Situazione favorevole (più carte alte nel mazzo)
- **TC = 0**: Situazione neutra
- **TC < -2**: Situazione sfavorevole (più carte basse nel mazzo)

### Nuova Mano

Clicca "Nuova Mano" per resettare la mano corrente mantenendo il conteggio

### Reset Conteggio

Usa "Reset Conteggio" quando:
- Inizia un nuovo shoe
- Il mazzo viene mescolato
- Vuoi ricominciare da zero

## 🎯 Strategia

L'applicazione implementa:

1. **Strategia di Base Ottimale** del Blackjack
2. **Gestione Mani Soft** (con Asso contato come 11)
3. **Strategia per Coppie** (quando splittare)
4. **Aggiustamenti per True Count** (deviazioni dalla strategia base)

### Modifiche per Card Counting

Con True Count alto (≥ +2):
- Più aggressivo nel raddoppiare
- Più disposto ad assicurarsi
- Modifica alcune decisioni limite

Con True Count basso (≤ -2):
- Più conservativo
- Evita di raddoppiare in situazioni borderline

## 📊 Struttura del Progetto

```
GiacomoNero/
├── main.py           # Interfaccia grafica principale
├── card_counter.py   # Logica card counting (Hi-Lo)
├── strategy.py       # Tabelle strategia base
├── requirements.txt  # Dipendenze
└── README.md         # Questa guida
```

## ⚠️ Note Legali

Questa applicazione è **solo per scopo educativo e di pratica**.

- Il card counting è legale ma i casinò possono rifiutare il servizio
- L'uso di dispositivi elettronici ai tavoli è **illegale** in molte giurisdizioni
- Usa questa app **solo per studio** o gioco privato

## 🔮 Sviluppi Futuri

Possibili miglioramenti:

- [ ] Statistiche delle mani giocate
- [ ] Grafico del conteggio nel tempo
- [ ] Supporto per varianti del Blackjack
- [ ] Modalità allenamento con quiz
- [ ] Export delle sessioni in CSV
- [ ] Versione mobile (Kivy o web app)
- [ ] Suggerimenti per la dimensione delle puntate

## 📝 Licenza

Progetto personale - Uso educativo

## 🤝 Contributi

Suggerimenti e miglioramenti sono benvenuti!

---

**Buona fortuna ai tavoli! 🎰**
