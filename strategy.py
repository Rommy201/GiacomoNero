"""
Tabella strategia base del Blackjack con modifiche basate sul card counting
"""


class BlackjackStrategy:
    """
    Strategia di base del Blackjack con aggiustamenti basati sul True Count
    """
    
    def __init__(self):
        # Tabella strategia di base per mani hard (senza assi)
        self.hard_strategy = self._init_hard_strategy()
        
        # Tabella strategia per mani soft (con asso)
        self.soft_strategy = self._init_soft_strategy()
        
        # Tabella strategia per coppie
        self.pair_strategy = self._init_pair_strategy()
        
    def _init_hard_strategy(self):
        """
        Strategia di base per mani hard
        Chiave: (totale_giocatore, carta_dealer)
        Valore: azione ('HIT', 'STAND', 'DOUBLE', 'SURRENDER')
        """
        strategy = {}
        
        # Per ogni totale del giocatore da 5 a 21
        for player_total in range(5, 22):
            for dealer_card in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']:
                key = (player_total, dealer_card)
                
                # 17-21: sempre STAND
                if player_total >= 17:
                    strategy[key] = 'STAND'
                
                # 13-16: STAND contro 2-6, HIT contro 7-A
                elif player_total >= 13:
                    if dealer_card in ['2', '3', '4', '5', '6']:
                        strategy[key] = 'STAND'
                    else:
                        strategy[key] = 'HIT'
                
                # 12: HIT contro 2-3, STAND contro 4-6, HIT contro 7-A
                elif player_total == 12:
                    if dealer_card in ['4', '5', '6']:
                        strategy[key] = 'STAND'
                    else:
                        strategy[key] = 'HIT'
                
                # 11: sempre DOUBLE (o HIT se non possibile)
                elif player_total == 11:
                    strategy[key] = 'DOUBLE'
                
                # 10: DOUBLE contro 2-9, HIT contro 10-A
                elif player_total == 10:
                    if dealer_card in ['2', '3', '4', '5', '6', '7', '8', '9']:
                        strategy[key] = 'DOUBLE'
                    else:
                        strategy[key] = 'HIT'
                
                # 9: DOUBLE contro 3-6, HIT altrimenti
                elif player_total == 9:
                    if dealer_card in ['3', '4', '5', '6']:
                        strategy[key] = 'DOUBLE'
                    else:
                        strategy[key] = 'HIT'
                
                # 5-8: sempre HIT
                else:
                    strategy[key] = 'HIT'
        
        return strategy
        
    def _init_soft_strategy(self):
        """
        Strategia di base per mani soft (con asso contato come 11)
        """
        strategy = {}
        
        for player_total in range(13, 22):  # Soft 13 (A,2) a Soft 21 (A,10)
            for dealer_card in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']:
                key = (player_total, dealer_card)
                
                # Soft 19-21: sempre STAND
                if player_total >= 19:
                    strategy[key] = 'STAND'
                
                # Soft 18: DOUBLE contro 3-6, STAND contro 2,7,8, HIT contro 9,10,A
                elif player_total == 18:
                    if dealer_card in ['3', '4', '5', '6']:
                        strategy[key] = 'DOUBLE'
                    elif dealer_card in ['2', '7', '8']:
                        strategy[key] = 'STAND'
                    else:
                        strategy[key] = 'HIT'
                
                # Soft 17: DOUBLE contro 3-6, HIT altrimenti
                elif player_total == 17:
                    if dealer_card in ['3', '4', '5', '6']:
                        strategy[key] = 'DOUBLE'
                    else:
                        strategy[key] = 'HIT'
                
                # Soft 15-16: DOUBLE contro 4-6, HIT altrimenti
                elif player_total in [15, 16]:
                    if dealer_card in ['4', '5', '6']:
                        strategy[key] = 'DOUBLE'
                    else:
                        strategy[key] = 'HIT'
                
                # Soft 13-14: DOUBLE contro 5-6, HIT altrimenti
                else:
                    if dealer_card in ['5', '6']:
                        strategy[key] = 'DOUBLE'
                    else:
                        strategy[key] = 'HIT'
        
        return strategy
        
    def _init_pair_strategy(self):
        """
        Strategia di base per coppie
        """
        strategy = {}
        
        pairs = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        
        for pair_card in pairs:
            for dealer_card in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']:
                key = (pair_card, dealer_card)
                
                # Coppia di Assi: sempre SPLIT
                if pair_card == 'A':
                    strategy[key] = 'SPLIT'
                
                # Coppia di 10: mai SPLIT
                elif pair_card == '10':
                    strategy[key] = 'STAND'
                
                # Coppia di 9: SPLIT tranne contro 7, 10, A
                elif pair_card == '9':
                    if dealer_card in ['7', '10', 'A']:
                        strategy[key] = 'STAND'
                    else:
                        strategy[key] = 'SPLIT'
                
                # Coppia di 8: sempre SPLIT
                elif pair_card == '8':
                    strategy[key] = 'SPLIT'
                
                # Coppia di 7: SPLIT contro 2-7
                elif pair_card == '7':
                    if dealer_card in ['2', '3', '4', '5', '6', '7']:
                        strategy[key] = 'SPLIT'
                    else:
                        strategy[key] = 'HIT'
                
                # Coppia di 6: SPLIT contro 2-6
                elif pair_card == '6':
                    if dealer_card in ['2', '3', '4', '5', '6']:
                        strategy[key] = 'SPLIT'
                    else:
                        strategy[key] = 'HIT'
                
                # Coppia di 5: mai SPLIT, DOUBLE contro 2-9
                elif pair_card == '5':
                    if dealer_card in ['2', '3', '4', '5', '6', '7', '8', '9']:
                        strategy[key] = 'DOUBLE'
                    else:
                        strategy[key] = 'HIT'
                
                # Coppia di 4: SPLIT contro 5-6
                elif pair_card == '4':
                    if dealer_card in ['5', '6']:
                        strategy[key] = 'SPLIT'
                    else:
                        strategy[key] = 'HIT'
                
                # Coppia di 2,3: SPLIT contro 2-7
                else:  # '2' o '3'
                    if dealer_card in ['2', '3', '4', '5', '6', '7']:
                        strategy[key] = 'SPLIT'
                    else:
                        strategy[key] = 'HIT'
        
        return strategy
        
    def get_suggestion(self, player_total, dealer_card, is_soft=False, is_pair=False, true_count=0):
        """
        Ottieni il suggerimento strategico
        
        Args:
            player_total: totale della mano del giocatore
            dealer_card: carta scoperta del dealer
            is_soft: True se la mano contiene un asso contato come 11
            is_pair: True se le prime due carte sono uguali
            true_count: True Count corrente per aggiustamenti
            
        Returns:
            dict: {'action': str, 'description': str}
        """
        # Normalizza la carta del dealer
        if dealer_card in ['J', 'Q', 'K']:
            dealer_card = '10'
            
        # Se il giocatore ha 21, sempre STAND
        if player_total == 21:
            return {
                'action': 'STAND',
                'description': 'Hai 21! Blackjack!'
            }
        
        # Se il giocatore ha più di 21, hai sballato
        if player_total > 21:
            return {
                'action': 'BUST',
                'description': 'Sballato!'
            }
        
        action = None
        
        # Controlla prima se è una coppia (solo con 2 carte)
        if is_pair:
            # Determina quale carta nella coppia
            pair_value = player_total // 2
            if pair_value == 11:  # Coppia di assi
                pair_card = 'A'
            elif pair_value >= 10:
                pair_card = '10'
            else:
                pair_card = str(pair_value)
                
            key = (pair_card, dealer_card)
            action = self.pair_strategy.get(key, 'HIT')
        
        # Se non è coppia o non abbiamo split, usa strategia soft/hard
        if not action or action not in ['SPLIT']:
            if is_soft:
                key = (player_total, dealer_card)
                action = self.soft_strategy.get(key, 'HIT')
            else:
                key = (player_total, dealer_card)
                action = self.hard_strategy.get(key, 'HIT')
        
        # Aggiustamenti basati sul True Count
        action, adjusted = self._adjust_for_count(action, player_total, dealer_card, true_count, is_soft)
        
        # Genera descrizione
        description = self._get_action_description(action, player_total, dealer_card, adjusted, true_count)
        
        return {
            'action': action,
            'description': description
        }
        
    def _adjust_for_count(self, action, player_total, dealer_card, true_count, is_soft):
        """
        Aggiusta la strategia in base al True Count
        
        Returns:
            tuple: (action, adjusted) dove adjusted è True se la strategia è stata modificata
        """
        adjusted = False
        
        # Con True Count alto (>= 2), sii più aggressivo
        if true_count >= 2:
            # Assicura 16 contro 10 con TC >= 0 (già implementato come HIT)
            # Assicura 15 contro 10 con TC >= 4
            if player_total == 15 and dealer_card == '10' and true_count >= 4 and not is_soft:
                action = 'SURRENDER'
                adjusted = True
            
            # Raddoppia 10 contro 10 e A con TC alto
            if player_total == 10 and dealer_card in ['10', 'A'] and true_count >= 4:
                action = 'DOUBLE'
                adjusted = True
                
            # Raddoppia 11 sempre con TC alto
            if player_total == 11 and true_count >= 1:
                action = 'DOUBLE'
                adjusted = True
        
        # Con True Count basso (<= -2), sii più conservativo
        elif true_count <= -2:
            # Non raddoppiare con TC basso
            if action == 'DOUBLE' and true_count <= -1:
                action = 'HIT'
                adjusted = True
                
            # Stand su 12 contro 4-6 solo con TC neutro o positivo
            if player_total == 12 and dealer_card in ['4', '5', '6'] and true_count < 0:
                action = 'HIT'
                adjusted = True
        
        return action, adjusted
        
    def _get_action_description(self, action, player_total, dealer_card, adjusted, true_count):
        """Genera una descrizione dell'azione suggerita"""
        descriptions = {
            'HIT': 'Chiedi carta',
            'STAND': 'Stai',
            'DOUBLE': 'Raddoppia (poi chiedi una sola carta)',
            'SPLIT': 'Dividi la coppia in due mani separate',
            'SURRENDER': 'Arrenditi (recupera metà della puntata)',
            'BUST': 'Hai sballato - Hai perso'
        }
        
        desc = descriptions.get(action, 'Azione sconosciuta')
        
        if adjusted:
            desc += f"\n(Strategia modificata per TC={true_count:.1f})"
        
        # Aggiungi informazioni specifiche
        if action == 'DOUBLE':
            desc += "\nSe non puoi raddoppiare, chiedi carta"
        elif action == 'SURRENDER':
            desc += "\nSe non puoi arrenderti, chiedi carta"
            
        return desc
