"""
Blackjack Assistant - Applicazione di supporto per il gioco del Blackjack
con card counting e suggerimenti strategici
"""

import tkinter as tk
from tkinter import ttk, messagebox
from card_counter import CardCounter
from strategy import BlackjackStrategy


class BlackjackAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Assistant")
        self.root.geometry("900x800")
        self.root.configure(bg='#0d1b2a')
        
        self.card_counter = CardCounter()
        self.strategy = BlackjackStrategy()
        
        self.player_cards = []
        self.dealer_card = None
        self.other_players_cards = []  # Lista di carte di altri giocatori
        self.current_bet = 0  # Puntata corrente della mano
        
        # Modalità selezione: 'dealer', 'player', 'table'
        self.selection_mode = tk.StringVar(value='dealer')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Titolo
        title = tk.Label(
            self.root, 
            text="♠ BLACKJACK ASSISTANT ♣", 
            font=("Arial", 24, "bold"),
            bg='#0d1b2a',
            fg='#00ff00'
        )
        title.pack(pady=15)
        
        # Frame per setup iniziale
        setup_frame = tk.LabelFrame(
            self.root, 
            text="Setup Tavolo", 
            font=("Arial", 11, "bold"),
            bg='#1b263b',
            fg='#ffffff',
            padx=15,
            pady=10
        )
        setup_frame.pack(padx=20, pady=5, fill='x')
        
        # Numero mazzi
        deck_frame = tk.Frame(setup_frame, bg='#1b263b')
        deck_frame.pack(fill='x', pady=5)
        
        tk.Label(
            deck_frame, 
            text="Mazzi rimanenti:", 
            font=("Arial", 10),
            bg='#1b263b',
            fg='#ffffff'
        ).pack(side='left')
        
        self.deck_var = tk.StringVar(value="6")
        deck_spin = tk.Spinbox(
            deck_frame, 
            from_=1, 
            to=8, 
            textvariable=self.deck_var,
            width=5,
            font=("Arial", 10)
        )
        deck_spin.pack(side='left', padx=10)
        
        tk.Button(
            deck_frame,
            text="Imposta",
            command=self.set_decks,
            bg='#415a77',
            fg='#ffffff',
            font=("Arial", 9, "bold"),
            padx=15
        ).pack(side='left', padx=5)
        
        tk.Button(
            deck_frame,
            text="Reset Conteggio",
            command=self.reset_count,
            bg='#e63946',
            fg='#ffffff',
            font=("Arial", 9, "bold"),
            padx=15
        ).pack(side='left', padx=5)
        
        # Setup Bankroll e Minimo Tavolo
        bankroll_frame = tk.Frame(setup_frame, bg='#1b263b')
        bankroll_frame.pack(fill='x', pady=5)
        
        tk.Label(
            bankroll_frame,
            text="Bankroll Iniziale (€):",
            font=("Arial", 10),
            bg='#1b263b',
            fg='#ffffff'
        ).pack(side='left')
        
        self.bankroll_var = tk.StringVar(value="1000")
        tk.Entry(
            bankroll_frame,
            textvariable=self.bankroll_var,
            width=10,
            font=("Arial", 10)
        ).pack(side='left', padx=10)
        
        tk.Label(
            bankroll_frame,
            text="Minimo Tavolo (€):",
            font=("Arial", 10),
            bg='#1b263b',
            fg='#ffffff'
        ).pack(side='left', padx=(20, 0))
        
        self.min_bet_var = tk.StringVar(value="10")
        tk.Entry(
            bankroll_frame,
            textvariable=self.min_bet_var,
            width=10,
            font=("Arial", 10)
        ).pack(side='left', padx=10)
        
        tk.Button(
            bankroll_frame,
            text="Imposta Bankroll",
            command=self.set_bankroll,
            bg='#06a77d',
            fg='#ffffff',
            font=("Arial", 9, "bold"),
            padx=15
        ).pack(side='left', padx=5)
        
        # Conteggio corrente
        self.count_frame = tk.LabelFrame(
            self.root,
            text="Conteggio Carte (Hi-Lo System)",
            font=("Arial", 11, "bold"),
            bg='#1b263b',
            fg='#ffffff',
            padx=15,
            pady=10
        )
        self.count_frame.pack(padx=20, pady=5, fill='x')
        
        count_display = tk.Frame(self.count_frame, bg='#1b263b')
        count_display.pack()
        
        tk.Label(
            count_display,
            text="Running Count:",
            font=("Arial", 10),
            bg='#1b263b',
            fg='#ffffff'
        ).grid(row=0, column=0, padx=10, sticky='e')
        
        self.running_count_label = tk.Label(
            count_display,
            text="0",
            font=("Arial", 14, "bold"),
            bg='#1b263b',
            fg='#00ff00',
            width=8
        )
        self.running_count_label.grid(row=0, column=1, padx=10)
        
        tk.Label(
            count_display,
            text="True Count:",
            font=("Arial", 10),
            bg='#1b263b',
            fg='#ffffff'
        ).grid(row=1, column=0, padx=10, sticky='e')
        
        self.true_count_label = tk.Label(
            count_display,
            text="0.0",
            font=("Arial", 14, "bold"),
            bg='#1b263b',
            fg='#ffaa00',
            width=8
        )
        self.true_count_label.grid(row=1, column=1, padx=10)
        
        tk.Label(
            count_display,
            text="Carte Rimanenti:",
            font=("Arial", 10),
            bg='#1b263b',
            fg='#ffffff'
        ).grid(row=0, column=2, padx=10, sticky='e')
        
        self.cards_remaining_label = tk.Label(
            count_display,
            text="312",
            font=("Arial", 14, "bold"),
            bg='#1b263b',
            fg='#4ecdc4',
            width=8
        )
        self.cards_remaining_label.grid(row=0, column=3, padx=10)
        
        tk.Label(
            count_display,
            text="Carte Viste:",
            font=("Arial", 10),
            bg='#1b263b',
            fg='#ffffff'
        ).grid(row=1, column=2, padx=10, sticky='e')
        
        self.cards_seen_label = tk.Label(
            count_display,
            text="0",
            font=("Arial", 14, "bold"),
            bg='#1b263b',
            fg='#e0e0e0',
            width=8
        )
        self.cards_seen_label.grid(row=1, column=3, padx=10)
        
        # Separatore
        tk.Frame(self.count_frame, bg='#415a77', height=2).pack(fill='x', pady=10)
        
        # Display Bankroll
        bankroll_display = tk.Frame(self.count_frame, bg='#1b263b')
        bankroll_display.pack()
        
        tk.Label(
            bankroll_display,
            text="Bankroll:",
            font=("Arial", 10),
            bg='#1b263b',
            fg='#ffffff'
        ).grid(row=0, column=0, padx=10, sticky='e')
        
        self.bankroll_label = tk.Label(
            bankroll_display,
            text="1000€",
            font=("Arial", 14, "bold"),
            bg='#1b263b',
            fg='#00ff00',
            width=12
        )
        self.bankroll_label.grid(row=0, column=1, padx=10)
        
        tk.Label(
            bankroll_display,
            text="Profitto/Perdita:",
            font=("Arial", 10),
            bg='#1b263b',
            fg='#ffffff'
        ).grid(row=1, column=0, padx=10, sticky='e')
        
        self.profit_label = tk.Label(
            bankroll_display,
            text="0€",
            font=("Arial", 14, "bold"),
            bg='#1b263b',
            fg='#e0e0e0',
            width=12
        )
        self.profit_label.grid(row=1, column=1, padx=10)
        
        tk.Label(
            bankroll_display,
            text="Mani Giocate:",
            font=("Arial", 10),
            bg='#1b263b',
            fg='#ffffff'
        ).grid(row=0, column=2, padx=10, sticky='e')
        
        self.hands_label = tk.Label(
            bankroll_display,
            text="0 (0V / 0P)",
            font=("Arial", 14, "bold"),
            bg='#1b263b',
            fg='#4ecdc4',
            width=15
        )
        self.hands_label.grid(row=0, column=3, padx=10)
        
        tk.Label(
            bankroll_display,
            text="Win Rate:",
            font=("Arial", 10),
            bg='#1b263b',
            fg='#ffffff'
        ).grid(row=1, column=2, padx=10, sticky='e')
        
        self.winrate_label = tk.Label(
            bankroll_display,
            text="0%",
            font=("Arial", 14, "bold"),
            bg='#1b263b',
            fg='#e0e0e0',
            width=15
        )
        self.winrate_label.grid(row=1, column=3, padx=10)
        
        # Frame per Bet Spread
        bet_frame = tk.LabelFrame(
            self.root,
            text="💰 SUGGERIMENTO PUNTATA",
            font=("Arial", 11, "bold"),
            bg='#1b263b',
            fg='#ffd700',
            padx=15,
            pady=10
        )
        bet_frame.pack(padx=20, pady=5, fill='x')
        
        self.bet_suggestion_label = tk.Label(
            bet_frame,
            text="Puntata: Minimo del tavolo (10€)",
            font=("Arial", 13, "bold"),
            bg='#1b263b',
            fg='#ffffff',
            wraplength=800
        )
        self.bet_suggestion_label.pack(pady=5)
        
        # Frame selezione modalità
        mode_frame = tk.LabelFrame(
            self.root,
            text="📍 Seleziona Destinazione Carta",
            font=("Arial", 11, "bold"),
            bg='#1b263b',
            fg='#ffffff',
            padx=15,
            pady=10
        )
        mode_frame.pack(padx=20, pady=5, fill='x')
        
        mode_buttons_frame = tk.Frame(mode_frame, bg='#1b263b')
        mode_buttons_frame.pack()
        
        # Radio buttons per selezione modalità
        tk.Radiobutton(
            mode_buttons_frame,
            text="🎴 Carta Banco",
            variable=self.selection_mode,
            value='dealer',
            font=("Arial", 11, "bold"),
            bg='#1b263b',
            fg='#ff6b6b',
            selectcolor='#415a77',
            activebackground='#1b263b',
            activeforeground='#ff6b6b',
            indicatoron=0,
            width=15,
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Radiobutton(
            mode_buttons_frame,
            text="🃏 Le Mie Carte",
            variable=self.selection_mode,
            value='player',
            font=("Arial", 11, "bold"),
            bg='#1b263b',
            fg='#4ecdc4',
            selectcolor='#415a77',
            activebackground='#1b263b',
            activeforeground='#4ecdc4',
            indicatoron=0,
            width=15,
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Radiobutton(
            mode_buttons_frame,
            text="🎯 Altre Carte Tavolo",
            variable=self.selection_mode,
            value='table',
            font=("Arial", 11, "bold"),
            bg='#1b263b',
            fg='#ffaa00',
            selectcolor='#415a77',
            activebackground='#1b263b',
            activeforeground='#ffaa00',
            indicatoron=0,
            width=15,
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        # Frame per bottoni carte
        cards_frame = tk.LabelFrame(
            self.root,
            text="🎴 Clicca sulla Carta",
            font=("Arial", 11, "bold"),
            bg='#1b263b',
            fg='#ffffff',
            padx=15,
            pady=10
        )
        cards_frame.pack(padx=20, pady=5, fill='x')
        
        # Griglia di bottoni carte
        cards_grid = tk.Frame(cards_frame, bg='#1b263b')
        cards_grid.pack()
        
        # Prima riga: A, 2-7
        row1 = tk.Frame(cards_grid, bg='#1b263b')
        row1.pack(pady=5)
        
        cards_row1 = ['A', '2', '3', '4', '5', '6', '7']
        for card in cards_row1:
            self.create_card_button(row1, card)
        
        # Seconda riga: 8, 9, 10, J, Q, K
        row2 = tk.Frame(cards_grid, bg='#1b263b')
        row2.pack(pady=5)
        
        cards_row2 = ['8', '9', '10', 'J', 'Q', 'K']
        for card in cards_row2:
            self.create_card_button(row2, card)
        
        # Frame mano corrente - display
        hand_frame = tk.LabelFrame(
            self.root,
            text="Mano Corrente",
            font=("Arial", 11, "bold"),
            bg='#1b263b',
            fg='#ffffff',
            padx=15,
            pady=10
        )
        hand_frame.pack(padx=20, pady=5, fill='x')
        
        # Display carta dealer
        dealer_display_frame = tk.Frame(hand_frame, bg='#1b263b')
        dealer_display_frame.pack(fill='x', pady=5)
        
        tk.Label(
            dealer_display_frame,
            text="Carta Banco:",
            font=("Arial", 10, "bold"),
            bg='#1b263b',
            fg='#ffffff'
        ).pack(side='left')
        
        self.dealer_display = tk.Label(
            dealer_display_frame,
            text="❓",
            font=("Arial", 18, "bold"),
            bg='#1b263b',
            fg='#ff6b6b',
            width=8
        )
        self.dealer_display.pack(side='left', padx=20)
        
        # Display carte giocatore
        self.player_cards_label = tk.Label(
            hand_frame,
            text="Le tue carte: -",
            font=("Arial", 11),
            bg='#1b263b',
            fg='#ffffff'
        )
        self.player_cards_label.pack(pady=5)
        
        self.player_total_label = tk.Label(
            hand_frame,
            text="Totale: -",
            font=("Arial", 13, "bold"),
            bg='#1b263b',
            fg='#4ecdc4'
        )
        self.player_total_label.pack(pady=5)
        
        # Separatore
        tk.Frame(hand_frame, bg='#415a77', height=2).pack(fill='x', pady=10)
        
        # Display carte altri giocatori
        tk.Label(
            hand_frame,
            text="Carte Altri Giocatori (al tavolo):",
            font=("Arial", 10, "bold"),
            bg='#1b263b',
            fg='#ffaa00'
        ).pack(pady=3)
        
        self.other_players_label = tk.Label(
            hand_frame,
            text="Nessuna carta tracciata",
            font=("Arial", 10),
            bg='#1b263b',
            fg='#aaaaaa',
            wraplength=700
        )
        self.other_players_label.pack(pady=3)
        
        tk.Button(
            hand_frame,
            text="🔄 Nuova Mano",
            command=self.new_hand,
            bg='#f77f00',
            fg='#ffffff',
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        ).pack(pady=10)
        
        # Suggerimento strategia
        self.strategy_frame = tk.LabelFrame(
            self.root,
            text="💡 SUGGERIMENTO STRATEGIA",
            font=("Arial", 12, "bold"),
            bg='#1b263b',
            fg='#00ff00',
            padx=15,
            pady=10
        )
        self.strategy_frame.pack(padx=20, pady=5, fill='both', expand=True)
        
        self.strategy_label = tk.Label(
            self.strategy_frame,
            text="Seleziona 'Carta Banco' e clicca sulla carta del dealer\nPoi seleziona 'Le Mie Carte' e clicca sulle tue carte",
            font=("Arial", 13, "bold"),
            bg='#1b263b',
            fg='#ffffff',
            wraplength=800,
            justify='center'
        )
        self.strategy_label.pack(expand=True)
        
        # Frame per registrare risultato mano
        result_frame = tk.LabelFrame(
            self.root,
            text="🎲 RISULTATO MANO",
            font=("Arial", 12, "bold"),
            bg='#1b263b',
            fg='#ffd700',
            padx=15,
            pady=10
        )
        result_frame.pack(padx=20, pady=5, fill='x')
        
        # Display puntata corrente
        self.current_bet_label = tk.Label(
            result_frame,
            text="Puntata Corrente: Non impostata",
            font=("Arial", 11, "bold"),
            bg='#1b263b',
            fg='#ffaa00'
        )
        self.current_bet_label.pack(pady=5)
        
        # Bottoni risultato
        buttons_frame = tk.Frame(result_frame, bg='#1b263b')
        buttons_frame.pack(pady=5)
        
        tk.Button(
            buttons_frame,
            text="✅ VINTO",
            command=lambda: self.record_result('win'),
            bg='#06a77d',
            fg='#ffffff',
            font=("Arial", 10, "bold"),
            width=12,
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame,
            text="❌ PERSO",
            command=lambda: self.record_result('loss'),
            bg='#e63946',
            fg='#ffffff',
            font=("Arial", 10, "bold"),
            width=12,
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame,
            text="🔄 PAREGGIO",
            command=lambda: self.record_result('push'),
            bg='#415a77',
            fg='#ffffff',
            font=("Arial", 10, "bold"),
            width=12,
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        # Seconda riga di bottoni
        buttons_frame2 = tk.Frame(result_frame, bg='#1b263b')
        buttons_frame2.pack(pady=5)
        
        tk.Button(
            buttons_frame2,
            text="⭐ BLACKJACK!",
            command=lambda: self.record_result('blackjack'),
            bg='#f77f00',
            fg='#ffffff',
            font=("Arial", 10, "bold"),
            width=12,
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame2,
            text="💰 DOPPIO VINTO",
            command=lambda: self.record_result('double_win'),
            bg='#06a77d',
            fg='#ffffff',
            font=("Arial", 10, "bold"),
            width=14,
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame2,
            text="💥 DOPPIO PERSO",
            command=lambda: self.record_result('double_loss'),
            bg='#e63946',
            fg='#ffffff',
            font=("Arial", 10, "bold"),
            width=14,
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame2,
            text="🏳️ ARRESA",
            command=lambda: self.record_result('surrender'),
            bg='#778da9',
            fg='#ffffff',
            font=("Arial", 10, "bold"),
            width=12,
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        # Inizializza conteggio
        self.update_count_display()
    
    def create_card_button(self, parent, card):
        """Crea un bottone per una carta"""
        # Simboli per le carte
        card_symbols = {
            'A': '🂡',
            '2': '🂢',
            '3': '🂣',
            '4': '🂤',
            '5': '🂥',
            '6': '🂦',
            '7': '🂧',
            '8': '🂨',
            '9': '🂩',
            '10': '🂪',
            'J': '🂫',
            'Q': '🂭',
            'K': '🂮'
        }
        
        # Colori basati sul valore Hi-Lo
        if card in ['2', '3', '4', '5', '6']:
            color = '#90ee90'  # Verde chiaro (carte basse +1)
        elif card in ['7', '8', '9']:
            color = '#ffd700'  # Oro (carte neutre 0)
        else:  # 10, J, Q, K, A
            color = '#ff6b6b'  # Rosso chiaro (carte alte -1)
        
        btn = tk.Button(
            parent,
            text=f"{card_symbols.get(card, card)}\n{card}",
            command=lambda: self.card_clicked(card),
            bg=color,
            fg='#000000',
            font=("Arial", 16, "bold"),
            width=4,
            height=2,
            relief='raised',
            borderwidth=3,
            cursor='hand2'
        )
        btn.pack(side='left', padx=3)
        
        # Effetto hover
        def on_enter(e):
            btn['background'] = '#ffffff'
        
        def on_leave(e):
            btn['background'] = color
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def card_clicked(self, card):
        """Gestisce il click su una carta"""
        mode = self.selection_mode.get()
        
        if mode == 'dealer':
            self.set_dealer_card_direct(card)
        elif mode == 'player':
            self.add_player_card_direct(card)
        elif mode == 'table':
            self.add_table_card_direct(card)
    
    def set_dealer_card_direct(self, card):
        """Imposta la carta del dealer"""
        self.dealer_card = card
        
        card_symbols = {
            'A': '🂡', '2': '🂢', '3': '🂣', '4': '🂤', '5': '🂥',
            '6': '🂦', '7': '🂧', '8': '🂨', '9': '🂩', '10': '🂪',
            'J': '🂫', 'Q': '🂭', 'K': '🂮'
        }
        
        self.dealer_display.config(text=f"{card_symbols.get(card, card)} {card}")
        self.card_counter.add_card(card)
        self.update_count_display()
        self.update_suggestion()
        
        # Feedback visivo
        self.dealer_display.config(bg='#2d5016')
        self.root.after(200, lambda: self.dealer_display.config(bg='#1b263b'))
    
    def add_player_card_direct(self, card):
        """Aggiungi una carta al giocatore"""
        self.player_cards.append(card)
        self.card_counter.add_card(card)
        self.update_player_display()
        self.update_count_display()
        self.update_suggestion()
        
        # Auto-switch a 'table' dopo 2 carte
        if len(self.player_cards) >= 2:
            self.selection_mode.set('table')
    
    def add_table_card_direct(self, card):
        """Aggiungi una carta vista al tavolo (non del giocatore)"""
        self.other_players_cards.append(card)
        self.card_counter.add_card(card)
        self.update_count_display()
        self.update_other_players_display()
        
        # Feedback visivo temporaneo
        temp_label = tk.Label(
            self.root,
            text=f"✓ {card}",
            font=("Arial", 12, "bold"),
            bg='#0d1b2a',
            fg='#00ff00'
        )
        temp_label.place(relx=0.5, rely=0.3, anchor='center')
        self.root.after(500, temp_label.destroy)
        
    def set_decks(self):
        decks = int(self.deck_var.get())
        self.card_counter.set_decks(decks)
        messagebox.showinfo("Info", f"Impostati {decks} mazzi")
    
    def set_bankroll(self):
        try:
            bankroll = float(self.bankroll_var.get())
            minimum = float(self.min_bet_var.get())
            
            if bankroll <= 0 or minimum <= 0:
                messagebox.showerror("Errore", "I valori devono essere positivi")
                return
            
            if minimum > bankroll:
                messagebox.showerror("Errore", "Il minimo del tavolo non può essere maggiore del bankroll")
                return
                
            self.card_counter.set_bankroll(bankroll)
            self.card_counter.set_table_minimum(minimum)
            self.update_count_display()
            
            messagebox.showinfo(
                "Info", 
                f"Bankroll: {bankroll:.0f}€\nMinimo Tavolo: {minimum:.0f}€\nBetting Unit: {self.card_counter.betting_unit:.0f}€"
            )
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori numerici validi")
        
    def reset_count(self):
        self.card_counter.reset()
        self.update_count_display()
        messagebox.showinfo("Info", "Conteggio resettato")
    
    def record_result(self, result):
        """Registra il risultato della mano"""
        if self.current_bet == 0:
            messagebox.showwarning("Attenzione", "Nessuna puntata impostata per questa mano!\nLa puntata viene impostata automaticamente quando selezioni le carte.")
            return
        
        # Registra il risultato
        self.card_counter.record_hand_result(result, self.current_bet)
        
        # Mostra messaggio di conferma
        result_messages = {
            'win': f"Vittoria! +{self.current_bet:.0f}€",
            'loss': f"Sconfitta. -{self.current_bet:.0f}€",
            'push': "Pareggio. Puntata restituita",
            'blackjack': f"BLACKJACK! +{self.current_bet * 1.5:.0f}€",
            'double_win': f"Raddoppio vinto! +{self.current_bet * 2:.0f}€",
            'double_loss': f"Raddoppio perso. -{self.current_bet * 2:.0f}€",
            'surrender': f"Arresa. -{self.current_bet * 0.5:.0f}€"
        }
        
        # Aggiorna display
        self.update_count_display()
        
        # Reset puntata corrente
        self.current_bet = 0
        self.current_bet_label.config(text="Puntata Corrente: Non impostata", fg='#ffaa00')
        
        messagebox.showinfo("Risultato Registrato", result_messages.get(result, "Registrato"))
    
    # Rimuovi i vecchi metodi set_dealer_card, add_player_card, add_table_card
    # perché ora usiamo i metodi _direct
        
    def update_other_players_display(self):
        """Aggiorna il display delle carte degli altri giocatori"""
        if self.other_players_cards:
            card_symbols = {
                'A': '🂡', '2': '🂢', '3': '🂣', '4': '🂤', '5': '🂥',
                '6': '🂦', '7': '🂧', '8': '🂨', '9': '🂩', '10': '🂪',
                'J': '🂫', 'Q': '🂭', 'K': '🂮'
            }
            
            # Raggruppa le carte per tipo
            from collections import Counter
            card_counts = Counter(self.other_players_cards)
            
            cards_display = " ".join([
                f"{card_symbols.get(card, card)}{card}" + 
                (f"×{count}" if count > 1 else "")
                for card, count in card_counts.items()
            ])
            
            self.other_players_label.config(
                text=f"{cards_display} (Totale: {len(self.other_players_cards)} carte)",
                fg='#ffaa00'
            )
        else:
            self.other_players_label.config(
                text="Nessuna carta tracciata",
                fg='#aaaaaa'
            )
    
    def update_player_display(self):
        if self.player_cards:
            # Usa simboli delle carte
            card_symbols = {
                'A': '🂡', '2': '🂢', '3': '🂣', '4': '🂤', '5': '🂥',
                '6': '🂦', '7': '🂧', '8': '🂨', '9': '🂩', '10': '🂪',
                'J': '🂫', 'Q': '🂭', 'K': '🂮'
            }
            
            cards_display = " ".join([f"{card_symbols.get(c, c)}{c}" for c in self.player_cards])
            self.player_cards_label.config(text=f"Le tue carte: {cards_display}")
            
            total, soft = self.calculate_hand_value(self.player_cards)
            total_str = f"Totale: {total}"
            if soft:
                total_str += " (soft)"
            self.player_total_label.config(text=total_str)
        else:
            self.player_cards_label.config(text="Le tue carte: -")
            self.player_total_label.config(text="Totale: -")
            
    def calculate_hand_value(self, cards):
        """Calcola il valore della mano e se è soft (con asso contato come 11)"""
        total = 0
        aces = 0
        
        for card in cards:
            if card in ['J', 'Q', 'K']:
                total += 10
            elif card == 'A':
                aces += 1
                total += 11
            else:
                total += int(card)
        
        # Gestione assi
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
            
        soft = (aces > 0 and total <= 21)
        return total, soft
        
    def update_count_display(self):
        running = self.card_counter.get_running_count()
        true = self.card_counter.get_true_count()
        cards_remaining = self.card_counter.get_cards_remaining()
        cards_seen = self.card_counter.cards_seen
        
        self.running_count_label.config(text=str(running))
        self.true_count_label.config(text=f"{true:.1f}")
        self.cards_remaining_label.config(text=str(cards_remaining))
        self.cards_seen_label.config(text=str(cards_seen))
        
        # Aggiorna bankroll display
        bankroll = self.card_counter.current_bankroll
        profit = self.card_counter.get_profit_loss()
        hands = self.card_counter.hands_played
        wins = self.card_counter.hands_won
        losses = self.card_counter.hands_lost
        winrate = self.card_counter.get_win_rate()
        
        self.bankroll_label.config(text=f"{bankroll:.0f}€")
        
        # Colora profitto/perdita
        if profit > 0:
            profit_color = '#00ff00'
            profit_text = f"+{profit:.0f}€"
        elif profit < 0:
            profit_color = '#ff4444'
            profit_text = f"{profit:.0f}€"
        else:
            profit_color = '#e0e0e0'
            profit_text = f"{profit:.0f}€"
        
        self.profit_label.config(text=profit_text, fg=profit_color)
        self.hands_label.config(text=f"{hands} ({wins}V / {losses}P)")
        self.winrate_label.config(text=f"{winrate:.1f}%")
        
        # Colora bankroll in base alla situazione
        if bankroll < self.card_counter.initial_bankroll * 0.5:
            bankroll_color = '#ff4444'  # Rosso se perso più del 50%
        elif bankroll > self.card_counter.initial_bankroll:
            bankroll_color = '#00ff00'  # Verde se in profitto
        else:
            bankroll_color = '#ffaa00'  # Arancione se in perdita ma < 50%
        
        self.bankroll_label.config(fg=bankroll_color)
        
        # Colora in base al true count
        if true >= 2:
            color = '#00ff00'  # Verde - favorevole
        elif true >= 0:
            color = '#ffaa00'  # Arancione - neutro
        else:
            color = '#ff4444'  # Rosso - sfavorevole
            
        self.true_count_label.config(fg=color)
        
        # Aggiorna suggerimento bet spread
        bet_info = self.card_counter.get_bet_multiplier()
        
        bet_text = f"💰 {bet_info['description']}"
        
        if bet_info['action'] == 'LEAVE':
            bet_color = '#ff4444'  # Rosso
            bet_text += "\n🚪 Situazione sfavorevole - Considera di lasciare il tavolo"
        elif bet_info['action'] == 'MIN_BET':
            bet_color = '#ffaa00'  # Arancione
        else:  # BET
            bet_color = '#00ff00'  # Verde
            bet_text += "\n⚡ Situazione favorevole!"
        
        self.bet_suggestion_label.config(text=bet_text, fg=bet_color)
        
    def update_suggestion(self):
        if not self.dealer_card or not self.player_cards:
            return
        
        player_total, is_soft = self.calculate_hand_value(self.player_cards)
        true_count = self.card_counter.get_true_count()
        
        # Imposta la puntata corrente se non è ancora stata impostata
        if self.current_bet == 0:
            bet_info = self.card_counter.get_bet_multiplier()
            self.current_bet = bet_info['bet_amount']
            self.current_bet_label.config(
                text=f"Puntata Corrente: {self.current_bet:.0f}€",
                fg='#00ff00'
            )
        
        # Verifica se è una coppia
        is_pair = len(self.player_cards) == 2 and self.player_cards[0] == self.player_cards[1]
        
        suggestion = self.strategy.get_suggestion(
            player_total,
            self.dealer_card,
            is_soft,
            is_pair,
            true_count
        )
        
        # Emoji per le azioni
        action_emoji = {
            'HIT': '👊',
            'STAND': '✋',
            'DOUBLE': '💰',
            'SPLIT': '✂️',
            'SURRENDER': '🏳️'
        }
        
        emoji = action_emoji.get(suggestion['action'], '❓')
        text = f"{emoji} {suggestion['action']}\n\n{suggestion['description']}"
        
        # Colora in base al true count
        if true_count >= 2:
            text += f"\n\n⚡ True Count alto (+{true_count:.1f}) - Situazione favorevole!"
        elif true_count <= -2:
            text += f"\n\n⚠️ True Count basso ({true_count:.1f}) - Cautela!"
            
        self.strategy_label.config(text=text)
        
    def new_hand(self):
        self.player_cards = []
        self.dealer_card = None
        self.other_players_cards = []
        self.current_bet = 0
        self.dealer_display.config(text="❓")
        self.update_player_display()
        self.update_other_players_display()
        self.selection_mode.set('dealer')
        self.current_bet_label.config(text="Puntata Corrente: Non impostata", fg='#ffaa00')
        self.strategy_label.config(
            text="Seleziona 'Carta Banco' e clicca sulla carta del dealer\nPoi seleziona 'Le Mie Carte' e clicca sulle tue carte"
        )


def main():
    root = tk.Tk()
    app = BlackjackAssistant(root)
    root.mainloop()


if __name__ == "__main__":
    main()
