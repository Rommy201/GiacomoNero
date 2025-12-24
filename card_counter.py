"""
Sistema di Card Counting per Blackjack
Implementa il Hi-Lo System
"""


class CardCounter:
    """
    Card Counter con sistema Hi-Lo:
    - Carte basse (2-6): +1
    - Carte neutre (7-9): 0
    - Carte alte (10, J, Q, K, A): -1
    """
    
    def __init__(self):
        self.running_count = 0
        self.decks_remaining = 6
        self.cards_seen = 0
        self.total_cards = 312  # 6 mazzi * 52 carte
        self.cards_by_value = {}  # Traccia quante carte di ogni valore sono uscite
        self._init_card_tracking()
        
        # Gestione bankroll
        self.initial_bankroll = 100  # Bankroll iniziale in euro
        self.current_bankroll = 100
        self.table_minimum = 5  # Minimo del tavolo in euro
        self.betting_unit = 10  # Unità di puntata base
        self.hands_played = 0
        self.hands_won = 0
        self.hands_lost = 0
        self.hands_pushed = 0
        
    def _init_card_tracking(self):
        """Inizializza il tracking delle carte per valore"""
        # Ogni valore: A, 2-9 (4 carte per mazzo), 10/J/Q/K (16 carte per mazzo)
        for value in ['A', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.cards_by_value[value] = 0
        # 10, J, Q, K sono raggruppati come "10"
        for value in ['10', 'J', 'Q', 'K']:
            self.cards_by_value[value] = 0
    
    def set_decks(self, decks):
        """Imposta il numero di mazzi rimanenti"""
        self.decks_remaining = decks
        self.total_cards = decks * 52
        self._init_card_tracking()
        
    def reset(self):
        """Reset del conteggio"""
        self.running_count = 0
        self.cards_seen = 0
        self._init_card_tracking()
    
    def set_bankroll(self, amount):
        """Imposta il bankroll iniziale"""
        self.initial_bankroll = amount
        self.current_bankroll = amount
        self.hands_played = 0
        self.hands_won = 0
        self.hands_lost = 0
        self.hands_pushed = 0
    
    def set_table_minimum(self, minimum):
        """Imposta il minimo del tavolo"""
        self.table_minimum = minimum
        # Calcola betting unit come 5% del bankroll o minimo*2, quello maggiore
        suggested_unit = max(self.initial_bankroll * 0.025, minimum * 2)
        self.betting_unit = suggested_unit
    
    def record_hand_result(self, result, bet_amount):
        """Registra il risultato di una mano
        
        Args:
            result: 'win', 'loss', 'push', 'blackjack', 'double_win', 'double_loss'
            bet_amount: importo della puntata
        """
        self.hands_played += 1
        
        if result == 'win':
            self.current_bankroll += bet_amount
            self.hands_won += 1
        elif result == 'loss':
            self.current_bankroll -= bet_amount
            self.hands_lost += 1
        elif result == 'push':
            self.hands_pushed += 1
            # Nessun cambio al bankroll
        elif result == 'blackjack':
            # Blackjack paga 3:2
            self.current_bankroll += bet_amount * 1.5
            self.hands_won += 1
        elif result == 'double_win':
            # Raddoppio vinto
            self.current_bankroll += bet_amount * 2
            self.hands_won += 1
        elif result == 'double_loss':
            # Raddoppio perso
            self.current_bankroll -= bet_amount * 2
            self.hands_lost += 1
        elif result == 'surrender':
            # Arresa - perdi metà puntata
            self.current_bankroll -= bet_amount * 0.5
            self.hands_lost += 1
    
    def get_profit_loss(self):
        """Ottieni profitto o perdita corrente"""
        return self.current_bankroll - self.initial_bankroll
    
    def get_win_rate(self):
        """Calcola percentuale di vittoria"""
        if self.hands_played == 0:
            return 0
        return (self.hands_won / self.hands_played) * 100
        
    def add_card(self, card):
        """
        Aggiungi una carta al conteggio
        
        Args:
            card: stringa rappresentante la carta ('A', '2'-'10', 'J', 'Q', 'K')
        """
        value = self._get_card_value(card)
        self.running_count += value
        self.cards_seen += 1
        
        # Traccia la carta uscita
        if card in self.cards_by_value:
            self.cards_by_value[card] += 1
    
    def remove_card(self, card):
        """
        Rimuovi una carta dal conteggio (per undo)
        
        Args:
            card: stringa rappresentante la carta ('A', '2'-'10', 'J', 'Q', 'K')
        """
        value = self._get_card_value(card)
        self.running_count -= value
        self.cards_seen -= 1
        
        # Rimuovi tracciamento carta
        if card in self.cards_by_value and self.cards_by_value[card] > 0:
            self.cards_by_value[card] -= 1
        
    def _get_card_value(self, card):
        """
        Ottieni il valore della carta per il conteggio Hi-Lo
        
        Args:
            card: stringa rappresentante la carta
            
        Returns:
            int: +1, 0, o -1 secondo il sistema Hi-Lo
        """
        # Carte basse (2-6): +1
        if card in ['2', '3', '4', '5', '6']:
            return 1
        
        # Carte neutre (7-9): 0
        elif card in ['7', '8', '9']:
            return 0
        
        # Carte alte (10, J, Q, K, A): -1
        elif card in ['10', 'J', 'Q', 'K', 'A']:
            return -1
        
        return 0
        
    def get_running_count(self):
        """Ottieni il running count corrente"""
        return self.running_count
        
    def get_true_count(self):
        """
        Calcola il True Count dividendo il Running Count per i mazzi rimanenti
        
        Returns:
            float: True Count
        """
        if self.decks_remaining <= 0:
            return 0
        
        # Stima i mazzi rimanenti basandosi sulle carte viste
        cards_per_deck = 52
        decks_used = self.cards_seen / cards_per_deck
        estimated_decks_remaining = max(self.decks_remaining - decks_used, 0.5)
        
        return self.running_count / estimated_decks_remaining
        
    def update_decks_remaining(self, decks):
        """Aggiorna manualmente i mazzi rimanenti"""
        self.decks_remaining = decks
        
    def get_advantage(self):
        """
        Calcola il vantaggio percentuale approssimativo basato sul True Count
        
        Returns:
            float: Percentuale di vantaggio (positivo = favorevole al giocatore)
        """
        true_count = self.get_true_count()
        # Ogni punto di True Count vale circa 0.5% di vantaggio
        return true_count * 0.5
        
    def should_increase_bet(self):
        """
        Suggerisce se aumentare la puntata
        
        Returns:
            bool: True se il True Count è favorevole (>= 2)
        """
        return self.get_true_count() >= 2
        
    def get_bet_multiplier(self):
        """
        Suggerisce un moltiplicatore per la puntata basato sul True Count
        Usa i valori personalizzati di betting unit e minimo tavolo
        
        Returns:
            dict: {
                'multiplier': float,  # Moltiplicatore della betting unit
                'bet_amount': float,  # Importo suggerito in euro
                'action': str         # 'LEAVE' o 'BET' o 'MIN_BET'
            }
        """
        true_count = self.get_true_count()
        
        # Tabella Bet Spread basata sul True Count
        if true_count <= -2:
            # Lasciare il tavolo o puntata minima
            return {
                'multiplier': 0,
                'bet_amount': self.table_minimum,
                'action': 'LEAVE',
                'description': f'Lascia il tavolo (TC sfavorevole) - {self.table_minimum:.0f}€'
            }
        elif true_count < 1:
            # Minimo del tavolo
            multiplier = self.table_minimum / self.betting_unit
            return {
                'multiplier': multiplier,
                'bet_amount': self.table_minimum,
                'action': 'MIN_BET',
                'description': f'Minimo del tavolo - {self.table_minimum:.0f}€'
            }
        elif true_count < 2:
            # 1 unità
            return {
                'multiplier': 1,
                'bet_amount': self.betting_unit,
                'action': 'BET',
                'description': f'1 unità - {self.betting_unit:.0f}€'
            }
        elif true_count < 3:
            # 2 unità
            return {
                'multiplier': 2,
                'bet_amount': self.betting_unit * 2,
                'action': 'BET',
                'description': f'2 unità - {self.betting_unit * 2:.0f}€'
            }
        elif true_count < 4:
            # 3 unità
            return {
                'multiplier': 3,
                'bet_amount': self.betting_unit * 3,
                'action': 'BET',
                'description': f'3 unità - {self.betting_unit * 3:.0f}€'
            }
        elif true_count < 5:
            # 4 unità
            return {
                'multiplier': 4,
                'bet_amount': self.betting_unit * 4,
                'action': 'BET',
                'description': f'4 unità - {self.betting_unit * 4:.0f}€'
            }
        else:  # TC >= 5
            # 5+ unità
            return {
                'multiplier': 5,
                'bet_amount': self.betting_unit * 5,
                'action': 'BET',
                'description': f'5+ unità - {self.betting_unit * 5:.0f}€'
            }
            
    def get_cards_remaining(self):
        """Ottieni il numero di carte rimanenti"""
        return self.total_cards - self.cards_seen
    
    def get_cards_remaining_by_value(self, card):
        """Ottieni quante carte di un certo valore rimangono"""
        cards_per_deck = 4 if card not in ['10', 'J', 'Q', 'K'] else 4
        if card in ['J', 'Q', 'K']:
            # Per figure, conta tutte come "10"
            total_available = int(self.decks_remaining) * 16  # 4 per ogni figura
            used = sum(self.cards_by_value.get(v, 0) for v in ['10', 'J', 'Q', 'K'])
        else:
            total_available = int(self.decks_remaining) * cards_per_deck
            used = self.cards_by_value.get(card, 0)
        
        return max(0, total_available - used)
    
    def get_stats(self):
        """
        Ottieni statistiche complete del conteggio
        
        Returns:
            dict: Dizionario con tutte le statistiche
        """
        return {
            'running_count': self.running_count,
            'true_count': self.get_true_count(),
            'cards_seen': self.cards_seen,
            'cards_remaining': self.get_cards_remaining(),
            'decks_remaining': self.decks_remaining,
            'advantage': self.get_advantage(),
            'bet_multiplier': self.get_bet_multiplier(),
            'current_bankroll': self.current_bankroll,
            'profit_loss': self.get_profit_loss(),
            'hands_played': self.hands_played,
            'hands_won': self.hands_won,
            'hands_lost': self.hands_lost,
            'win_rate': self.get_win_rate()
        }
