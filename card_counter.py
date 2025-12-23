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
        
        Returns:
            int: Moltiplicatore suggerito (1-8x)
        """
        true_count = self.get_true_count()
        
        if true_count < 1:
            return 1  # Puntata minima
        elif true_count < 2:
            return 2
        elif true_count < 3:
            return 4
        elif true_count < 4:
            return 6
        else:
            return 8  # Puntata massima
            
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
            'bet_multiplier': self.get_bet_multiplier()
        }
