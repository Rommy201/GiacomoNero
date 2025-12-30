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
                    if dealer_card in ['2', '3', '4', '5', '6', '7', '8', '9']:
                        strategy[key] = 'DOUBLE'
                    else:
                        strategy[key] = 'HIT'
                
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
                if player_total >= 20:
                    strategy[key] = 'STAND'
                
                #Soft 19: DOUBLE contro 6, STAND altrimenti
                elif player_total == 19:
                    if dealer_card == '6':
                        strategy[key] = 'DOUBLE'
                    else:
                        strategy[key] = 'STAND'
                
                # Soft 18: DOUBLE contro 3-6, STAND contro 2,7,8, HIT contro 9,10,A
                elif player_total == 18:
                    if dealer_card in ['2', '3', '4', '5', '6']:
                        strategy[key] = 'DOUBLE'
                    elif dealer_card in ['7', '8']:
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
        
    def get_suggestion(self, player_total, dealer_card, is_soft=False, is_pair=False, true_count=0, num_cards=2):
        """
        Ottieni il suggerimento strategico
        
        Args:
            player_total: totale della mano del giocatore
            dealer_card: carta scoperta del dealer
            is_soft: True se la mano contiene un asso contato come 11
            is_pair: True se le prime due carte sono uguali
            true_count: True Count corrente per aggiustamenti
            num_cards: numero di carte nella mano del giocatore
            
        Returns:
            dict: {'action': str, 'description': str}
        """
        # Arrotonda il True Count a 1 decimale per evitare problemi di floating point
        true_count = round(true_count, 1)
        
        # Normalizza la carta del dealer
        if dealer_card in ['J', 'Q', 'K']:
            dealer_card = '10'
            
        # Se il giocatore ha 21, sempre STAND
        if player_total == 21:
            # Blackjack solo con 2 carte
            if num_cards == 2:
                description = 'Hai 21! Blackjack!'
            else:
                description = 'Hai 21!'
            return {
                'action': 'STAND',
                'description': description
            }
        
        # Se il giocatore ha più di 21, hai sballato
        if player_total > 21:
            return {
                'action': 'BUST',
                'description': 'Sballato!'
            }
        
        action = None
        pair_card = None
        adjusted_split = False
        
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
            
            # Applica deviazioni di split basate sul True Count
            action, adjusted_split = self._adjust_split_for_count(action, pair_card, dealer_card, true_count)
        
        # Se non è coppia o non abbiamo split, usa strategia soft/hard
        if not action or action not in ['SPLIT']:
            if is_soft:
                key = (player_total, dealer_card)
                action = self.soft_strategy.get(key, 'HIT')
            else:
                key = (player_total, dealer_card)
                action = self.hard_strategy.get(key, 'HIT')
        
        # Aggiustamenti basati sul True Count (per non-split)
        action, adjusted, fallback_action = self._adjust_for_count(action, player_total, dealer_card, true_count, is_soft, num_cards)
        
        # IMPORTANTE: Se hai più di 2 carte, non puoi raddoppiare
        # (SURRENDER viene gestito dentro _adjust_for_count)
        if num_cards > 2 and action == 'DOUBLE':
            action = 'HIT'  # Sostituisci DOUBLE con HIT
            adjusted = True
        
        # Combina gli adjusted flags
        adjusted = adjusted or adjusted_split
        
        # Controlla se suggerire l'assicurazione
        insurance_suggestion = None
        if dealer_card == 'A' and true_count >= 3:
            insurance_suggestion = f"ASSICURAZIONE: Sì (TC={true_count:.1f} >= 3)"
        
        # Genera descrizione
        description = self._get_action_description(action, player_total, dealer_card, adjusted, true_count, fallback_action)
        
        # Aggiungi suggerimento assicurazione alla descrizione se presente
        if insurance_suggestion:
            description = insurance_suggestion + "\n\n" + description
        
        return {
            'action': action,
            'description': description,
            'insurance': insurance_suggestion
        }
    
    def _adjust_split_for_count(self, action, pair_card, dealer_card, true_count):
        """
        Aggiusta la strategia di split in base al True Count
        Basato sulla tabella "SPLITTARE" delle deviazioni europee
        
        Returns:
            tuple: (action, adjusted) dove adjusted è True se la strategia è stata modificata
        """
        adjusted = False
        
        # 10,10 (T,T) vs 4: Split con TC >= 6+
        if pair_card == '10' and dealer_card == '4' and true_count >= 6:
            action = 'SPLIT'
            adjusted = True
        
        # 10,10 (T,T) vs 5: Split con TC >= 5+
        if pair_card == '10' and dealer_card == '5' and true_count >= 5:
            action = 'SPLIT'
            adjusted = True
        
        # 10,10 (T,T) vs 6: Split con TC >= 4+
        if pair_card == '10' and dealer_card == '6' and true_count >= 4:
            action = 'SPLIT'
            adjusted = True
        return action, adjusted
        
    def _adjust_for_count(self, action, player_total, dealer_card, true_count, is_soft, num_cards=2):
        """
        Aggiusta la strategia in base al True Count (Deviazioni Europee)
        
        Args:
            num_cards: numero di carte nella mano (SURRENDER valido solo con 2 carte)
        
        Returns:
            tuple: (action, adjusted, fallback_action) dove:
                - action: l'azione principale suggerita
                - adjusted: True se la strategia è stata modificata
                - fallback_action: azione alternativa se SURRENDER non è disponibile
        """
        adjusted = False
        fallback_action = None
        original_action = action
        
        # Solo per mani hard (non soft)
        if not is_soft:
            # ===== SURRENDER (RESA) - Solo con esattamente 2 carte =====
            if num_cards == 2:
                # 17 vs A: Arrenditi sempre (strategia di base)
                if player_total == 17 and dealer_card == 'A':
                    fallback_action = original_action
                    action = 'SURRENDER'
                    adjusted = True

                # 16 vs 8: Arrenditi con TC >= 4+
                if player_total == 16 and dealer_card == '8' and true_count >= 4:
                    fallback_action = original_action
                    action = 'SURRENDER'
                    adjusted = True

                # 16 vs 9: Arrenditi con TC >= 0+
                if player_total == 16 and dealer_card == '9' and true_count >= 0:
                    fallback_action = original_action
                    action = 'SURRENDER'
                    adjusted = True
                
                # 16 vs 10: Arrenditi con TC >= 0+
                if player_total == 16 and dealer_card == '10':
                    fallback_action = original_action
                    action = 'SURRENDER'
                    adjusted = True
                
                # 16 vs A: Arrenditi sempre (strategia di base)
                if player_total == 16 and dealer_card == 'A':
                    fallback_action = original_action
                    action = 'SURRENDER'
                    adjusted = True
                    
                # 15 vs 9: Arrenditi con TC >= 2+
                if player_total == 15 and dealer_card == '9' and true_count >= 2:
                    fallback_action = original_action
                    action = 'SURRENDER'
                    adjusted = True
                
                # 15 vs 10: Arrenditi con TC >= 0
                if player_total == 15 and dealer_card == '10' and true_count >= 0:
                    fallback_action = original_action
                    action = 'SURRENDER'
                    adjusted = True
                
                # 15 vs A: Arrenditi con TC >= -1
                if player_total == 15 and dealer_card == 'A' and true_count >= -1:
                    fallback_action = original_action
                    action = 'SURRENDER'
                    adjusted = True
            
            # ===== DEVIAZIONI STRATEGIA BASE (COPPIE PURE) =====
            
            
            # 16 vs 9: Stand con TC >= 4+
            if player_total == 16 and dealer_card == '9' and true_count >= 4:
                if action == 'HIT' or (action == 'SURRENDER' and fallback_action == 'HIT'):
                    if action == 'SURRENDER':
                        fallback_action = 'STAND'
                    else:
                        action = 'STAND'
                        adjusted = True
            
            # 16 vs 10: Stand con TC > 0+
            if player_total == 16 and dealer_card == '10' and true_count > 0:
                if action == 'HIT' or (action == 'SURRENDER' and fallback_action == 'HIT'):
                    if action == 'SURRENDER':
                        fallback_action = 'STAND'
                    else:
                        action = 'STAND'
                        adjusted = True
                    
            # 15 vs 10: Stand con TC >= 3+
            if player_total == 15 and dealer_card == '10' and true_count >= 3:
                if action == 'HIT' or (action == 'SURRENDER' and fallback_action == 'HIT'):
                    if action == 'SURRENDER':
                        fallback_action = 'STAND'
                    else:
                        action = 'STAND'
                        adjusted = True
            
            # 13 vs 2: Stand con TC <= -1
            if player_total == 13 and dealer_card == '2' and true_count <= -1:
                if action == 'STAND':
                    action = 'HIT'
                    adjusted = True
            
            # 12 vs 2: Stand con TC >= 3+
            if player_total == 12 and dealer_card == '2' and true_count >= 3:
                if action == 'HIT':
                    action = 'STAND'
                    adjusted = True
                    
            # 12 vs 3: Stand con TC >= 2+
            if player_total == 12 and dealer_card == '3' and true_count >= 2:
                if action == 'HIT':
                    action = 'STAND'
                    adjusted = True
            
            # 12 vs 4: Hit con TC < 0
            if player_total == 12 and dealer_card == '4' and true_count < 0:
                if action == 'STAND':
                    action = 'HIT'
                    adjusted = True
            
            # 11 vs 10: Raddoppia con TC >= 4+
            if player_total == 11 and dealer_card == '10' and true_count >= 4:
                if action == 'HIT':
                    action = 'DOUBLE'
                    adjusted = True
            
            # 10 vs 9: Hit con TC <= -1
            if player_total == 10 and dealer_card == '9' and true_count <= -1:
                if action == 'DOUBLE':
                    action = 'HIT'
                    adjusted = True
            
            # 9 vs 2: Raddoppia con TC >= 1+
            if player_total == 9 and dealer_card == '2' and true_count >= 1:
                if action == 'HIT':
                    action = 'DOUBLE'
                    adjusted = True
            
            # 9 vs 7: Raddoppia con TC >= 3+
            if player_total == 9 and dealer_card == '7' and true_count >= 3:
                if action == 'HIT':
                    action = 'DOUBLE'
                    adjusted = True
        
        # ===== DEVIAZIONI PER COPPIE CON ASSO =====
        else:  # is_soft = True
            # A,8 vs 4: Raddoppia con TC >= 3+
            if player_total == 19 and dealer_card == '4' and true_count >= 3:
                if action == 'STAND':
                    action = 'DOUBLE'
                    adjusted = True
            
            # A,8 vs 5: Raddoppia con TC >= 1+
            if player_total == 19 and dealer_card == '5' and true_count >= 1:
                if action == 'STAND':
                    action = 'DOUBLE'
                    adjusted = True
            
            # A,8 vs 6: Stand con TC < 0
            if player_total == 19 and dealer_card == '6' and true_count < 0:
                if action == 'DOUBLE':
                    action = 'STAND'
                    adjusted = True
            
            # A,6 vs 2: Raddoppia con TC >= 1+
            if player_total == 17 and dealer_card == '2' and true_count >= 1:
                if action == 'HIT':
                    action = 'DOUBLE'
                    adjusted = True
        
        return action, adjusted, fallback_action
        
    def _get_action_description(self, action, player_total, dealer_card, adjusted, true_count, fallback_action=None):
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
            # Mostra l'azione alternativa se surrender non è disponibile
            if fallback_action:
                fallback_desc = descriptions.get(fallback_action, 'chiedi carta')
                desc += f"\nSe non puoi arrenderti: {fallback_desc}"
            else:
                desc += "\nSe non puoi arrenderti, chiedi carta"
            
        return desc
