# Strategia Blackjack Implementata

## 📋 Panoramica
Implementazione completa della strategia di Blackjack con **deviazioni europee** basate sul True Count, inclusa la possibilità di **arresa (surrender)**.

## 🎯 Strategie Implementate

### 1. ARRESA (SURRENDER) - SE PERMESSA
La strategia di arresa è stata completamente implementata con le seguenti regole:

#### Mani da Arrendersi:
- **16 vs 9**: Arrenditi con True Count >= **4+**
- **16 vs 10**: Arrenditi con True Count >= **0+**
- **16 vs A**: Arrenditi sempre (strategia di base)
- **15 vs 9**: Arrenditi con True Count >= **2+**
- **15 vs 10**: Arrenditi con True Count >= **-1**
- **15 vs A**: Arrenditi con True Count >= **-1**

> **Assicurazione**: Prenderla dal True Count **3+**

### 2. DEVIAZIONI STRATEGIA BASE (COPPIE PURE)

#### Stand vs Hit:
- **17 vs A**: Stand sempre
- **16 vs 7**: Stand con TC >= **4+**
- **16 vs 8**: Stand con TC >= **4+**
- **15 vs 7**: Stand con TC >= **3+**
- **13 vs 2**: Stand con TC >= **-1**
- **12 vs 2**: Stand con TC >= **3+**
- **12 vs 3**: Stand con TC >= **2+**
- **12 vs 4**: Stand con TC >= **0**

#### Raddoppi:
- **11 vs A**: Raddoppia con TC >= **4+**
- **10 vs 10**: Raddoppia con TC >= **1+**
- **10 vs A**: Raddoppia con TC >= **1+**
- **9 vs 2**: Raddoppia con TC >= **1+**
- **9 vs 7**: Raddoppia con TC >= **3+**

### 3. DEVIAZIONI COPPIE CON ASSO (SOFT HANDS)

#### Soft 19 (A,8):
- **vs 4**: Raddoppia con TC >= **3+**
- **vs 5**: Raddoppia con TC >= **1+**
- **vs 6**: Raddoppia con TC >= **4+**

#### Soft 17 (A,6):
- **vs 2**: Raddoppia con TC >= **1+**

### 4. STRATEGIA SPLIT

#### Split Coppie:
- **10,10 vs 4**: Split con TC >= **6+**
- **10,10 vs 5**: Split con TC >= **5+**
- **10,10 vs 6**: Split con TC >= **4+**
- **9,9 vs 7**: Split con TC >= **6+**

### 5. BET SPREAD (Sistema di Puntate)

Basato su:
- **Bankroll**: 20.000€
- **Betting Unit**: 50€
- **Minimo Tavolo**: 10€

#### Tabella Puntate per True Count:

| True Count | Azione | Puntata | Unità |
|------------|--------|---------|-------|
| <= -2 | 🚪 Lascia tavolo | 10€ | - |
| -1 a 0 | Minimo tavolo | 10€ | 0.2x |
| 1 | Punta normale | 50€ | 1x |
| 2 | Aumenta puntata | 100€ | 2x |
| 3 | Aumenta puntata | 150€ | 3x |
| 4 | Aumenta puntata | 200€ | 4x |
| 5+ | ⚡ Massima puntata | 250€ | 5x |

## 🎮 Funzionalità dell'Applicazione

### Interfaccia Utente:
1. **Conteggio Carte (Hi-Lo System)**
   - Running Count
   - True Count
   - Carte rimanenti
   - Carte viste

2. **Suggerimento Puntata**
   - Visualizzazione dell'importo consigliato
   - Indicazione di quando lasciare il tavolo
   - Colori visivi (rosso/arancione/verde)

3. **Suggerimento Strategia**
   - Azione consigliata (Hit, Stand, Double, Split, Surrender)
   - Descrizione dell'azione
   - Indicazione deviazione dalla strategia base
   - Emoji visivi per ogni azione

4. **Selezione Carte**
   - Carta del banco
   - Le tue carte
   - Altre carte al tavolo
   - Codice colore per valore Hi-Lo

### Legenda Colori Carte:
- 🟢 **Verde chiaro** (2-6): Carte basse +1
- 🟡 **Oro** (7-9): Carte neutre 0
- 🔴 **Rosso chiaro** (10-A): Carte alte -1

## 📊 Sistema Hi-Lo

### Valori Carte:
- **+1**: 2, 3, 4, 5, 6
- **0**: 7, 8, 9
- **-1**: 10, J, Q, K, A

### Calcolo True Count:
```
True Count = Running Count / Mazzi Rimanenti
```

## 🎯 Emoji Azioni

- 👊 **HIT**: Chiedi carta
- ✋ **STAND**: Stai
- 💰 **DOUBLE**: Raddoppia
- ✂️ **SPLIT**: Dividi coppia
- 🏳️ **SURRENDER**: Arrenditi

## ⚡ Indicatori Situazione

- 🟢 **TC >= 2**: Situazione favorevole - Aumenta puntata
- 🟡 **TC 0-1**: Situazione neutra - Puntata normale
- 🔴 **TC < 0**: Situazione sfavorevole - Puntata minima o lascia tavolo

## 📝 Note Importanti

1. **Surrender**: L'opzione è disponibile solo se permessa dal casinò
2. **Raddoppio dopo Split**: Alcune deviazioni assumono questa regola
3. **Assicurazione**: Prendere solo con TC >= 3+
4. **Gestione Bankroll**: Rispettare sempre le unità di puntata consigliate

## 🚀 Come Usare

1. Imposta il numero di mazzi
2. Seleziona "Carta Banco" e clicca sulla carta del dealer
3. Seleziona "Le Mie Carte" e clicca sulle tue carte
4. Seleziona "Altre Carte Tavolo" per tracciare carte di altri giocatori
5. Segui i suggerimenti di strategia e puntata
6. Usa "Nuova Mano" per resettare la mano corrente

---
**Versione**: 2.0 - Deviazioni Europee Complete con Surrender
**Ultima Modifica**: 23 Dicembre 2025
