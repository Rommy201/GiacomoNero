# ♠️ Blackjack Pro - Mobile Edition

Applicazione professionale di assistenza al Blackjack con conteggio carte (Hi-Lo System), strategia ottimale europea e gestione bankroll.

## 🎯 Caratteristiche Principali

- **Conteggio Carte Hi-Lo**: Running Count e True Count in tempo reale
- **Strategia Ottimale**: Include tutte le deviazioni europee e opzione di arresa
- **Gestione Bankroll**: Tracciamento completo di profitti, perdite e statistiche
- **Bet Spread Intelligente**: Suggerimenti di puntata basati sul True Count
- **Interface Mobile-First**: Ottimizzata per smartphone (420x920px)
- **Design Moderno**: Grafica scura con colori intuitivi

## 📱 Interfaccia Mobile

L'applicazione è completamente ottimizzata per l'uso su smartphone con:
- ✅ Layout compatto e scrollabile
- ✅ Bottoni touch-friendly (grandi e ben spaziati)
- ✅ Informazioni essenziali sempre visibili
- ✅ Colori che indicano situazioni favorevoli/sfavorevoli
- ✅ Setup collassabile per risparmiare spazio
- ✅ Dimensioni ottimizzate: 420x920 pixel (portrait mode)

## 🎮 Guida Rapida

### Setup Iniziale
1. Clicca su **"⚙️ SETUP"** per espandere le opzioni
2. Imposta il **numero di mazzi** (1-8)
3. Inserisci il tuo **bankroll iniziale** (es: 1000€)
4. Imposta il **minimo del tavolo** (es: 10€)
5. Clicca **"Conferma"** per salvare

### Durante il Gioco
1. **Seleziona modalità**: 
   - 🎴 **Banco** - Carta scoperta del dealer
   - 🃏 **Mie** - Le tue carte
   - 🎯 **Tavolo** - Altre carte visibili
2. Clicca sulla carta del banco
3. Clicca sulle tue carte (si passa automaticamente a "Tavolo" dopo 2 carte)
4. Leggi il **suggerimento di strategia** (grande e chiaro)
5. Nota la **puntata suggerita** (basata sul True Count)

### Dopo la Mano
1. Clicca sul **risultato** appropriato:
   - ✅ **VINTO** - Vittoria normale (+1x)
   - ❌ **PERSO** - Sconfitta normale (-1x)
   - ➖ **PAREGGIO** - Nessun cambio
   - ⭐ **BLACKJACK** - Blackjack naturale (+1.5x)
   - **2xW** / **2xL** - Raddoppio vinto/perso (±2x)
   - 🏳️ **ARRESA** - Surrender (-0.5x)
2. Clicca **"🔄 NUOVA MANO"** per ricominciare

## 📊 Indicatori Visivi

### Colori Carte
- 🟢 **Verde scuro** (2-6): Carte basse +1 (favorevoli)
- 🟡 **Oro scuro** (7-9): Carte neutre 0
- 🔴 **Rosso scuro** (10-A): Carte alte -1 (sfavorevoli)

### Colori True Count
- 🟢 **Verde brillante** (TC ≥ 2): Situazione MOLTO favorevole
- 🟡 **Arancione** (TC 0-1): Situazione neutra
- 🔴 **Rosso** (TC < 0): Situazione sfavorevole

### Suggerimento Puntata
- 🚪 **"ESCI!"** (Rosso): Lascia il tavolo (TC ≤ -2)
- 🟡 **"minimo"** (Arancione): Puntata minima (TC < 1)
- ⚡ **Verde** (Verde): Aumenta puntata! (TC ≥ 1)

### Bankroll
- 🟢 **Verde**: In profitto
- 🟡 **Arancione**: In perdita ma < 50%
- 🔴 **Rosso**: Perdita > 50% del bankroll iniziale

## 🃏 Strategia Implementata

### Azioni Base
- **👊 HIT**: Chiedi carta
- **✋ STAND**: Stai
- **💰 DOUBLE**: Raddoppia (poi HIT se non permesso)
- **✂️ SPLIT**: Dividi coppia
- **🏳️ SURRENDER**: Arrenditi (poi HIT se non permesso)

### Deviazioni dal True Count
- **Mani Hard**: 16, 15, 13, 12, 11, 10, 9 con deviazioni specifiche
- **Mani Soft**: A,8 e A,6 con deviazioni per raddoppi
- **Split**: 10,10 e 9,9 con deviazioni
- **Surrender**: 16 vs 9/10/A e 15 vs 9/10/A con soglie TC specifiche

## 💰 Sistema Bet Spread

Basato sul True Count e personalizzabile:

| True Count | Azione | Moltiplicatore |
|------------|--------|----------------|
| ≤ -2 | 🚪 Esci | Minimo tavolo |
| -1 a 0 | Punta minimo | Minimo tavolo |
| 1 | Punta normale | 1x unit |
| 2 | Aumenta | 2x unit |
| 3 | Aumenta | 3x unit |
| 4 | Aumenta | 4x unit |
| ≥ 5 | ⚡ MAX | 5x unit |

**Betting Unit** viene calcolata automaticamente come 2.5% del bankroll o minimo tavolo × 2 (il maggiore).

## 📈 Statistiche Tracciate

L'app traccia in tempo reale:
- 💰 **Bankroll corrente**
- 📊 **Profitto/Perdita** (con segno +/-)
- 🎯 **Mani giocate** (Vittorie-Perdite)
- 📈 **Win Rate** (percentuale)
- 🔢 **Running Count** e **True Count**
- 🃏 **Carte viste** e **carte rimanenti**

## 💾 Requisiti Tecnici

```
Python 3.6 o superiore
tkinter (incluso in Python standard)
```

## 🚀 Installazione e Avvio

```bash
# Clona o scarica il progetto
cd GiacomoNero

# Avvia l'applicazione
python main.py
```

L'applicazione si aprirà in una finestra 420×920 pixel, perfetta per smartphone!

## 🎨 Design Mobile-First

### Caratteristiche UX
- **Setup Collassabile**: Clicca "⚙️ SETUP" per nascondere/mostrare
- **Scroll Fluido**: Layout scrollabile per contenuti lunghi
- **Feedback Visivo**: Animazioni sui bottoni premuti
- **Nessun Popup**: Feedback inline per evitare interruzioni
- **Testo Grande**: Font ottimizzati per leggibilità su piccolo schermo
- **Spazi Touch**: Margini generosi tra i bottoni

### Palette Colori
- **Background**: Blu scuro (#0a0e27, #1a1f3a)
- **Accenti Oro**: #ffd700 per titoli e highlight
- **Successo**: #00ff00 (verde brillante)
- **Avviso**: #ff4444 (rosso)
- **Neutro**: #ffaa00 (arancione)

## ⚙️ Funzionalità Avanzate

### Conteggio Hi-Lo
Il sistema Hi-Lo assegna valori alle carte:
- **+1**: 2, 3, 4, 5, 6 (carte basse)
- **0**: 7, 8, 9 (carte neutre)
- **-1**: 10, J, Q, K, A (carte alte)

**True Count** = Running Count ÷ Mazzi Rimanenti

Maggiore è il True Count, più è favorevole la situazione per il giocatore.

### Gestione Bankroll
- **Protezione**: Warning visivo se perdi > 50%
- **Unit Sizing**: Automatico basato sul tuo bankroll
- **Tracking Completo**: Ogni mano viene registrata
- **Statistiche**: Win rate e profitti sempre visibili

## ⚠️ Disclaimer

- ⚖️ Questa applicazione è **solo per scopi educativi**
- 🎰 Il conteggio carte **non è illegale** ma può essere vietato dai casinò
- 💵 Gioca sempre **responsabilmente** e rispetta il tuo bankroll
- 📚 Le strategie sono basate su **probabilità matematiche**
- 🚫 Non garantiamo vincite - il Blackjack include sempre un elemento di fortuna

## 🔧 Troubleshooting

**La finestra è troppo grande/piccola?**
- L'app è ottimizzata per 420×920 pixel (smartphone portrait)
- Modifica `window_width` e `window_height` in `main.py` se necessario

**I bottoni sono troppo piccoli?**
- Aumenta il parametro `width` e `height` nei bottoni
- Font size modificabile nei parametri `font=("Arial", XX)`

**Colori non leggibili?**
- Modifica i colori nei parametri `bg` e `fg` dei widget

## 📞 Supporto e Contributi

Per problemi, suggerimenti o contributi:
- Apri una issue su GitHub
- Invia una pull request
- Contatta gli sviluppatori

## 📚 Risorse Utili

- [Strategia di Base Blackjack](https://wizardofodds.com/games/blackjack/strategy/calculator/)
- [Hi-Lo Card Counting](https://www.blackjackapprenticeship.com/how-to-count-cards/)
- [Bankroll Management](https://www.blackjackinfo.com/blackjack-bankroll-management/)

---

**Versione**: 3.0 Mobile Edition  
**Ultima Modifica**: 23 Dicembre 2025  
**Licenza**: MIT  
**Autore**: GiacomoNero Team

Buona fortuna al tavolo! 🍀♠️♥️♣️♦️
