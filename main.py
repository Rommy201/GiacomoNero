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
        self.root.title("♠️ Blackjack Pro")
        
        # Dimensioni ottimizzate per smartphone (portrait mode)
        window_width = 420
        window_height = 920
        
        # Centra la finestra
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#0a0e27')
        
        # Rendi la finestra non ridimensionabile per mantenere il layout
        self.root.resizable(False, False)
        
        self.card_counter = CardCounter()
        self.strategy = BlackjackStrategy()
        
        self.player_cards = []
        self.player_cards_split = []  # Seconda mano dopo split
        self.dealer_card = None
        self.dealer_cards = []  # Lista completa carte del banco
        self.other_players_cards = []  # Lista di carte di altri giocatori
        self.current_bet = 0  # Puntata corrente della mano
        self.is_split_hand = False  # Flag per indicare se è una mano splittata
        self.current_split_hand = 1  # 1 o 2 - quale mano stiamo giocando
        
        # Modalità selezione: 'dealer', 'player', 'table'
        self.selection_mode = tk.StringVar(value='dealer')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header compatto
        header = tk.Frame(self.root, bg='#1a1f3a', height=60)
        header.pack(fill='x', padx=0, pady=0)
        
        tk.Label(
            header, 
            text="♠️ BLACKJACK PRO ♣️", 
            font=("Arial", 18, "bold"),
            bg='#1a1f3a',
            fg='#ffd700'
        ).pack(pady=8)
        
        # Container scrollabile
        canvas = tk.Canvas(self.root, bg='#0a0e27', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#0a0e27')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Setup compatto in accordion style
        self.setup_collapsed = tk.BooleanVar(value=True)
        
        setup_header = tk.Frame(scrollable_frame, bg='#1a1f3a', cursor='hand2')
        setup_header.pack(fill='x', padx=5, pady=(5, 0))
        setup_header.bind('<Button-1>', lambda e: self.toggle_setup())
        
        tk.Label(
            setup_header,
            text="⚙️ SETUP",
            font=("Arial", 12, "bold"),
            bg='#1a1f3a',
            fg='#ffffff'
        ).pack(side='left', padx=10, pady=8)
        
        self.setup_arrow = tk.Label(
            setup_header,
            text="▼",
            font=("Arial", 10),
            bg='#1a1f3a',
            fg='#ffffff'
        )
        self.setup_arrow.pack(side='right', padx=10)
        
        # Setup content (collapsibile)
        self.setup_content = tk.Frame(scrollable_frame, bg='#151a35')
        
        # Mazzi in riga singola
        deck_row = tk.Frame(self.setup_content, bg='#151a35')
        deck_row.pack(fill='x', padx=10, pady=5)
        
        tk.Label(deck_row, text="Mazzi:", font=("Arial", 9), bg='#151a35', fg='#aaa').pack(side='left')
        self.deck_var = tk.StringVar(value="6")
        tk.Spinbox(deck_row, from_=1, to=8, textvariable=self.deck_var, width=3, font=("Arial", 9)).pack(side='left', padx=5)
        tk.Button(deck_row, text="Set", command=self.set_decks, bg='#2a3f5f', fg='#fff', font=("Arial", 8, "bold"), padx=8, pady=2).pack(side='left', padx=2)
        tk.Button(deck_row, text="Reset", command=self.reset_count, bg='#7d2e2e', fg='#fff', font=("Arial", 8, "bold"), padx=8, pady=2).pack(side='left', padx=2)
        
        # Bankroll in riga singola
        bank_row = tk.Frame(self.setup_content, bg='#151a35')
        bank_row.pack(fill='x', padx=10, pady=5)
        
        tk.Label(bank_row, text="Bankroll €:", font=("Arial", 9), bg='#151a35', fg='#aaa').pack(side='left')
        self.bankroll_var = tk.StringVar(value="1000")
        tk.Entry(bank_row, textvariable=self.bankroll_var, width=6, font=("Arial", 9)).pack(side='left', padx=5)
        
        tk.Label(bank_row, text="Min €:", font=("Arial", 9), bg='#151a35', fg='#aaa').pack(side='left', padx=(10, 0))
        self.min_bet_var = tk.StringVar(value="10")
        tk.Entry(bank_row, textvariable=self.min_bet_var, width=4, font=("Arial", 9)).pack(side='left', padx=5)
        
        tk.Button(bank_row, text="Conferma", command=self.set_bankroll, bg='#2d5f2e', fg='#fff', font=("Arial", 8, "bold"), padx=10, pady=2).pack(side='left', padx=5)
        
        # Conteggio in card compatta
        count_card = tk.Frame(scrollable_frame, bg='#1a1f3a', relief='raised', bd=2)
        count_card.pack(fill='x', padx=5, pady=5)
        
        tk.Label(count_card, text="📊 CONTEGGIO", font=("Arial", 11, "bold"), bg='#1a1f3a', fg='#ffd700').pack(pady=(8, 5))
        
        # Griglia compatta 2x2 per contatori principali
        count_grid = tk.Frame(count_card, bg='#1a1f3a')
        count_grid.pack(pady=5)
        
        self.create_counter_display(count_grid, "Running", "0", 0, 0, '#4ecdc4')
        self.create_counter_display(count_grid, "True", "0.0", 0, 1, '#ff6b6b')
        self.create_counter_display(count_grid, "Carte", "312", 1, 0, '#95e1d3')
        self.create_counter_display(count_grid, "Viste", "0", 1, 1, '#9896f1')
        
        # Bankroll info compatta
        bank_info = tk.Frame(count_card, bg='#151a35', relief='sunken', bd=1)
        bank_info.pack(fill='x', padx=10, pady=(5, 8))
        
        bank_row1 = tk.Frame(bank_info, bg='#151a35')
        bank_row1.pack(fill='x', pady=2)
        
        tk.Label(bank_row1, text="💰", font=("Arial", 12), bg='#151a35').pack(side='left', padx=5)
        self.bankroll_label = tk.Label(bank_row1, text="1000€", font=("Arial", 14, "bold"), bg='#151a35', fg='#00ff00')
        self.bankroll_label.pack(side='left')
        
        self.profit_label = tk.Label(bank_row1, text="(+0€)", font=("Arial", 11), bg='#151a35', fg='#aaa')
        self.profit_label.pack(side='left', padx=5)
        
        bank_row2 = tk.Frame(bank_info, bg='#151a35')
        bank_row2.pack(fill='x', pady=2)
        
        tk.Label(bank_row2, text="🎯", font=("Arial", 10), bg='#151a35').pack(side='left', padx=5)
        self.hands_label = tk.Label(bank_row2, text="0 mani", font=("Arial", 9), bg='#151a35', fg='#aaa')
        self.hands_label.pack(side='left')
        
        self.winrate_label = tk.Label(bank_row2, text="• 0% WR", font=("Arial", 9), bg='#151a35', fg='#aaa')
        self.winrate_label.pack(side='left', padx=10)
        
        # Suggerimento puntata prominente
        bet_card = tk.Frame(scrollable_frame, bg='#2a1f3d', relief='raised', bd=3)
        bet_card.pack(fill='x', padx=5, pady=5)
        
        tk.Label(bet_card, text="💎 PUNTATA SUGGERITA", font=("Arial", 10, "bold"), bg='#2a1f3d', fg='#ffd700').pack(pady=(8, 2))
        
        self.bet_suggestion_label = tk.Label(
            bet_card,
            text="Minimo tavolo - 10€",
            font=("Arial", 16, "bold"),
            bg='#2a1f3d',
            fg='#ffffff',
            wraplength=380
        )
        self.bet_suggestion_label.pack(pady=(0, 8))
        
        # Selezione modalità compatta con pulsanti touch-friendly
        mode_card = tk.Frame(scrollable_frame, bg='#1a1f3a')
        mode_card.pack(fill='x', padx=5, pady=5)
        
        tk.Label(mode_card, text="🎴 SELEZIONA CARTA", font=("Arial", 10, "bold"), bg='#1a1f3a', fg='#ffffff').pack(pady=(8, 5))
        
        mode_buttons = tk.Frame(mode_card, bg='#1a1f3a')
        mode_buttons.pack(pady=5)
        
        tk.Radiobutton(
            mode_buttons, text="🎴 Banco", variable=self.selection_mode, value='dealer',
            font=("Arial", 9, "bold"), bg='#5d2e46', fg='#fff', selectcolor='#7d3e56',
            activebackground='#5d2e46', indicatoron=0, width=11, padx=5, pady=8
        ).pack(side='left', padx=2)
        
        tk.Radiobutton(
            mode_buttons, text="🃏 Mie", variable=self.selection_mode, value='player',
            font=("Arial", 9, "bold"), bg='#2e5d4f', fg='#fff', selectcolor='#3e7d6f',
            activebackground='#2e5d4f', indicatoron=0, width=11, padx=5, pady=8
        ).pack(side='left', padx=2)
        
        tk.Radiobutton(
            mode_buttons, text="🎯 Tavolo", variable=self.selection_mode, value='table',
            font=("Arial", 9, "bold"), bg='#5d532e', fg='#fff', selectcolor='#7d6f3e',
            activebackground='#5d532e', indicatoron=0, width=11, padx=5, pady=8
        ).pack(side='left', padx=2)
        
        # Griglia carte compatta e touch-friendly
        cards_card = tk.Frame(scrollable_frame, bg='#1a1f3a')
        cards_card.pack(fill='x', padx=5, pady=5)
        
        # Riga 1: A, 2-6
        row1 = tk.Frame(cards_card, bg='#1a1f3a')
        row1.pack(pady=2)
        for card in ['A', '2', '3', '4', '5', '6']:
            self.create_card_button_mobile(row1, card)
        
        # Riga 2: 7-Q
        row2 = tk.Frame(cards_card, bg='#1a1f3a')
        row2.pack(pady=2)
        for card in ['7', '8', '9', '10', 'J', 'Q']:
            self.create_card_button_mobile(row2, card)
        
        # Riga 3: K
        row3 = tk.Frame(cards_card, bg='#1a1f3a')
        row3.pack(pady=2)
        self.create_card_button_mobile(row3, 'K')
        
        # Display mano corrente compatto
        hand_card = tk.Frame(scrollable_frame, bg='#151a35', relief='ridge', bd=2)
        hand_card.pack(fill='x', padx=5, pady=5)
        
        tk.Label(hand_card, text="🎰 MANO", font=("Arial", 10, "bold"), bg='#151a35', fg='#ffd700').pack(pady=(5, 2))
        
        dealer_frame = tk.Frame(hand_card, bg='#1a1f3a', relief='solid', bd=1)
        dealer_frame.pack(fill='x', padx=10, pady=3)
        
        tk.Label(dealer_frame, text="Banco:", font=("Arial", 9), bg='#1a1f3a', fg='#ff6b6b').pack(side='left', padx=5)
        self.dealer_display = tk.Label(dealer_frame, text="?", font=("Arial", 11), bg='#1a1f3a', fg='#ff6b6b', wraplength=250)
        self.dealer_display.pack(side='left', padx=5, pady=3)
        
        self.dealer_total_label = tk.Label(hand_card, text="", font=("Arial", 11, "bold"), bg='#151a35', fg='#ff6b6b')
        self.dealer_total_label.pack(pady=2)
        
        player_frame = tk.Frame(hand_card, bg='#1a1f3a', relief='solid', bd=1)
        player_frame.pack(fill='x', padx=10, pady=3)
        
        tk.Label(player_frame, text="Mano 1:", font=("Arial", 9), bg='#1a1f3a', fg='#4ecdc4').pack(side='left', padx=5)
        self.player_cards_label = tk.Label(player_frame, text="-", font=("Arial", 11), bg='#1a1f3a', fg='#ffffff', wraplength=250)
        self.player_cards_label.pack(side='left', padx=5, pady=3)
        
        self.player_total_label = tk.Label(hand_card, text="Tot: -", font=("Arial", 12, "bold"), bg='#151a35', fg='#4ecdc4')
        self.player_total_label.pack(pady=3)
        
        # Frame per mano split (inizialmente nascosto)
        self.split_frame = tk.Frame(hand_card, bg='#1a1f3a', relief='solid', bd=1)
        
        tk.Label(self.split_frame, text="Mano 2:", font=("Arial", 9), bg='#1a1f3a', fg='#95e1d3').pack(side='left', padx=5)
        self.player_cards_split_label = tk.Label(self.split_frame, text="-", font=("Arial", 11), bg='#1a1f3a', fg='#ffffff', wraplength=250)
        self.player_cards_split_label.pack(side='left', padx=5, pady=3)
        
        self.player_split_total_label = tk.Label(hand_card, text="", font=("Arial", 12, "bold"), bg='#151a35', fg='#95e1d3')
        
        # Bottone per switchare mano attiva (nascosto inizialmente)
        self.switch_hand_btn = tk.Button(
            hand_card,
            text="🔀 Passa a Mano 2",
            command=self.switch_split_hand,
            bg='#3a5f7d',
            fg='#ffffff',
            font=("Arial", 9, "bold"),
            padx=10,
            pady=3
        )
        
        # Bottone per attivare split
        self.activate_split_btn = tk.Button(
            hand_card,
            text="✂️ SPLIT",
            command=self.activate_split,
            bg='#5d3e7d',
            fg='#ffffff',
            font=("Arial", 9, "bold"),
            padx=10,
            pady=3
        )
        
        self.other_players_label = tk.Label(hand_card, text="Tavolo: -", font=("Arial", 8), bg='#151a35', fg='#888', wraplength=360)
        self.other_players_label.pack(pady=(2, 5))
        
        # Strategia prominente
        strategy_card = tk.Frame(scrollable_frame, bg='#1f3a1a', relief='raised', bd=3)
        strategy_card.pack(fill='x', padx=5, pady=5)
        
        tk.Label(strategy_card, text="💡 AZIONE", font=("Arial", 11, "bold"), bg='#1f3a1a', fg='#ffd700').pack(pady=(8, 2))
        
        self.strategy_label = tk.Label(
            strategy_card,
            text="Aspetto carte...",
            font=("Arial", 13, "bold"),
            bg='#1f3a1a',
            fg='#ffffff',
            wraplength=380,
            justify='center'
        )
        self.strategy_label.pack(pady=(0, 8), padx=10)
        
        # Puntata corrente
        bet_current_card = tk.Frame(scrollable_frame, bg='#3a2a1a', relief='solid', bd=2)
        bet_current_card.pack(fill='x', padx=5, pady=5)
        
        self.current_bet_label = tk.Label(
            bet_current_card,
            text="Puntata: -",
            font=("Arial", 11, "bold"),
            bg='#3a2a1a',
            fg='#ffd700'
        )
        self.current_bet_label.pack(pady=8)
        
        # Risultati in griglia compatta
        result_card = tk.Frame(scrollable_frame, bg='#1a1f3a')
        result_card.pack(fill='x', padx=5, pady=5)
        
        tk.Label(result_card, text="🎲 RISULTATO", font=("Arial", 10, "bold"), bg='#1a1f3a', fg='#ffd700').pack(pady=(5, 3))
        
        res_grid1 = tk.Frame(result_card, bg='#1a1f3a')
        res_grid1.pack(pady=2)
        
        self.create_result_button(res_grid1, "✅", "win", '#2d5f2e', 0, 0)
        self.create_result_button(res_grid1, "❌", "loss", '#7d2e2e', 0, 1)
        self.create_result_button(res_grid1, "➖", "push", '#3a3a5f', 0, 2)
        
        res_grid2 = tk.Frame(result_card, bg='#1a1f3a')
        res_grid2.pack(pady=2)
        
        self.create_result_button(res_grid2, "⭐", "blackjack", '#7d5f2e', 0, 0)
        self.create_result_button(res_grid2, "2xW", "double_win", '#2d5f2e', 0, 1)
        self.create_result_button(res_grid2, "2xL", "double_loss", '#7d2e2e', 0, 2)
        
        res_grid3 = tk.Frame(result_card, bg='#1a1f3a')
        res_grid3.pack(pady=2)
        
        self.create_result_button(res_grid3, "🏳️", "surrender", '#5f5a77', 0, 0)
        
        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Inizializza
        self.update_count_display()
    
    def create_counter_display(self, parent, label, value, row, col, color):
        """Crea un display compatto per contatori"""
        frame = tk.Frame(parent, bg='#151a35', relief='solid', bd=1, width=90, height=55)
        frame.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
        frame.grid_propagate(False)
        
        tk.Label(frame, text=label, font=("Arial", 8), bg='#151a35', fg='#aaa').pack(pady=(3, 0))
        
        label_widget = tk.Label(frame, text=value, font=("Arial", 13, "bold"), bg='#151a35', fg=color)
        label_widget.pack()
        
        # Salva riferimenti
        if label == "Running":
            self.running_count_label = label_widget
        elif label == "True":
            self.true_count_label = label_widget
        elif label == "Carte":
            self.cards_remaining_label = label_widget
        elif label == "Viste":
            self.cards_seen_label = label_widget
    
    def create_card_button_mobile(self, parent, card):
        """Crea bottone carta ottimizzato per mobile"""
        card_symbols = {
            'A': '🂡', '2': '🂢', '3': '🂣', '4': '🂤', '5': '🂥',
            '6': '🂦', '7': '🂧', '8': '🂨', '9': '🂩', '10': '🂪',
            'J': '🂫', 'Q': '🂭', 'K': '🂮'
        }
        
        if card in ['2', '3', '4', '5', '6']:
            color = '#4a7c59'  # Verde
        elif card in ['7', '8', '9']:
            color = '#7c6a3a'  # Oro
        else:
            color = '#7c3a3a'  # Rosso
        
        btn = tk.Button(
            parent,
            text=f"{card}",
            command=lambda: self.card_clicked(card),
            bg=color,
            fg='#ffffff',
            font=("Arial", 13, "bold"),
            width=4,
            height=1,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        btn.pack(side='left', padx=2, pady=2)
        
        def on_press(e):
            btn.config(relief='sunken')
        
        def on_release(e):
            btn.config(relief='raised')
        
        btn.bind("<ButtonPress-1>", on_press)
        btn.bind("<ButtonRelease-1>", on_release)
    
    def create_result_button(self, parent, text, result, color, row, col):
        """Crea bottone risultato compatto"""
        btn = tk.Button(
            parent,
            text=text,
            command=lambda: self.record_result(result),
            bg=color,
            fg='#ffffff',
            font=("Arial", 11, "bold"),
            width=10,
            height=2,
            relief='raised',
            bd=2
        )
        btn.grid(row=row, column=col, padx=3, pady=2)
    
    def toggle_setup(self):
        """Toggle setup panel visibility"""
        if self.setup_collapsed.get():
            self.setup_content.pack(fill='x', padx=0, pady=0, after=self.setup_content.master.winfo_children()[0])
            self.setup_arrow.config(text="▲")
            self.setup_collapsed.set(False)
        else:
            self.setup_content.pack_forget()
            self.setup_arrow.config(text="▼")
            self.setup_collapsed.set(True)
    
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
        """Aggiunge una carta al banco (prima o successive)"""
        # Se è la prima carta, imposta anche dealer_card per la strategia
        if not self.dealer_cards:
            self.dealer_card = card
            self.dealer_cards = [card]
        else:
            self.dealer_cards.append(card)
        
        self.update_dealer_display()
        self.card_counter.add_card(card)
        self.update_count_display()
        
        # Aggiorna suggerimento solo se è la prima carta
        if len(self.dealer_cards) == 1:
            self.update_suggestion()
        
        # Feedback visivo
        original_bg = self.dealer_display.cget('bg')
        self.dealer_display.config(bg='#3d5026')
        self.root.after(150, lambda: self.dealer_display.config(bg=original_bg))
    
    def add_player_card_direct(self, card):
        """Aggiungi una carta al giocatore"""
        if self.is_split_hand and self.current_split_hand == 2:
            self.player_cards_split.append(card)
        else:
            self.player_cards.append(card)
            
        self.card_counter.add_card(card)
        self.update_player_display()
        self.update_count_display()
        self.update_suggestion()
    
    def activate_split(self):
        """Attiva modalità split"""
        if len(self.player_cards) == 2:
            # Prendi una carta e mettila nella mano 2
            self.player_cards_split = [self.player_cards.pop()]
            self.is_split_hand = True
            self.current_split_hand = 1
            
            # Mostra UI split
            self.split_frame.pack(fill='x', padx=10, pady=3)
            self.player_split_total_label.pack(pady=3)
            self.switch_hand_btn.pack(pady=3)
            self.activate_split_btn.pack_forget()
            
            self.update_player_display()
            self.update_suggestion()
    
    def switch_split_hand(self):
        """Passa da una mano all'altra"""
        if self.current_split_hand == 1:
            self.current_split_hand = 2
            self.switch_hand_btn.config(text="🔀 Passa a Mano 1", bg='#3a7d5f')
        else:
            self.current_split_hand = 1
            self.switch_hand_btn.config(text="🔀 Passa a Mano 2", bg='#3a5f7d')
        
        self.update_suggestion()
    
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
        
        # Reset automatico per nuova mano
        self.new_hand()
    
    # Rimuovi i vecchi metodi set_dealer_card, add_player_card, add_table_card
    # perché ora usiamo i metodi _direct
        
    def update_other_players_display(self):
        """Aggiorna il display delle carte degli altri giocatori"""
        if self.other_players_cards:
            from collections import Counter
            card_counts = Counter(self.other_players_cards)
            
            cards_display = " ".join([
                f"{card}" + (f"×{count}" if count > 1 else "")
                for card, count in card_counts.items()
            ])
            
            self.other_players_label.config(
                text=f"Tavolo: {cards_display}",
                fg='#aaa'
            )
        else:
            self.other_players_label.config(
                text="Tavolo: -",
                fg='#888'
            )
    
    def update_dealer_display(self):
        """Aggiorna il display delle carte del banco"""
        if self.dealer_cards:
            cards_display = " ".join(self.dealer_cards)
            self.dealer_display.config(text=cards_display)
            
            total, soft = self.calculate_hand_value(self.dealer_cards)
            total_str = f"Tot: {total}"
            if soft:
                total_str += " (S)"
            self.dealer_total_label.config(text=total_str)
        else:
            self.dealer_display.config(text="?")
            self.dealer_total_label.config(text="")
    
    def update_player_display(self):
        # Mano 1
        if self.player_cards:
            cards_display = " ".join(self.player_cards)
            self.player_cards_label.config(text=cards_display)
            
            total, soft = self.calculate_hand_value(self.player_cards)
            total_str = f"Tot: {total}"
            if soft:
                total_str += " (S)"
            self.player_total_label.config(text=total_str)
        else:
            self.player_cards_label.config(text="-")
            self.player_total_label.config(text="Tot: -")
        
        # Mano 2 (se split attivo)
        if self.is_split_hand:
            if self.player_cards_split:
                cards_display = " ".join(self.player_cards_split)
                self.player_cards_split_label.config(text=cards_display)
                
                total, soft = self.calculate_hand_value(self.player_cards_split)
                total_str = f"Tot: {total}"
                if soft:
                    total_str += " (S)"
                self.player_split_total_label.config(text=total_str)
            else:
                self.player_cards_split_label.config(text="-")
                self.player_split_total_label.config(text="")
        
        # Mostra/nascondi bottone split
        if len(self.player_cards) == 2 and not self.is_split_hand:
            # Controlla se è una coppia
            if self.player_cards[0][0] == self.player_cards[1][0]:
                self.activate_split_btn.pack(pady=3)
            else:
                self.activate_split_btn.pack_forget()
        else:
            self.activate_split_btn.pack_forget()
            
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
        pushes = self.card_counter.hands_pushed
        winrate = self.card_counter.get_win_rate()
        
        self.bankroll_label.config(text=f"{bankroll:.0f}€")
        
        # Colora profitto/perdita
        if profit > 0:
            profit_color = '#00ff00'
            profit_text = f"(+{profit:.0f}€)"
        elif profit < 0:
            profit_color = '#ff4444'
            profit_text = f"({profit:.0f}€)"
        else:
            profit_color = '#aaa'
            profit_text = f"(±0€)"
        
        self.profit_label.config(text=profit_text, fg=profit_color)
        self.hands_label.config(text=f"{hands} ({wins}V-{losses}P-{pushes}Pa)")
        self.winrate_label.config(text=f"• {winrate:.1f}% WR")
        
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
        
        # Aggiorna suggerimento bet spread (più compatto)
        bet_info = self.card_counter.get_bet_multiplier()
        
        if bet_info['action'] == 'LEAVE':
            bet_text = f"🚪 {bet_info['bet_amount']:.0f}€ (ESCI!)"
            bet_color = '#ff4444'
        elif bet_info['action'] == 'MIN_BET':
            bet_text = f"{bet_info['bet_amount']:.0f}€ (minimo)"
            bet_color = '#ffaa00'
        else:  # BET
            bet_text = f"{bet_info['bet_amount']:.0f}€ ⚡"
            bet_color = '#00ff00'
        
        self.bet_suggestion_label.config(text=bet_text, fg=bet_color)
        
    def update_suggestion(self):
        if not self.dealer_card:
            return
            
        # Determina quale mano usare per il suggerimento
        if self.is_split_hand:
            if self.current_split_hand == 1:
                active_hand = self.player_cards
            else:
                active_hand = self.player_cards_split
        else:
            active_hand = self.player_cards
        
        if not active_hand:
            return
        
        player_total, is_soft = self.calculate_hand_value(active_hand)
        true_count = self.card_counter.get_true_count()
        
        # Imposta la puntata corrente se non è ancora stata impostata
        if self.current_bet == 0:
            bet_info = self.card_counter.get_bet_multiplier()
            self.current_bet = bet_info['bet_amount']
            self.current_bet_label.config(
                text=f"Puntata: {self.current_bet:.0f}€",
                fg='#00ff00'
            )
        
        # Verifica se è una coppia
        is_pair = len(active_hand) == 2 and active_hand[0] == active_hand[1]
        
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
        
        # Testo compatto per mobile
        text = f"{emoji} {suggestion['action']}"
        
        # Aggiungi solo descrizione essenziale
        if suggestion['action'] == 'DOUBLE':
            text += "\n(altrimenti HIT)"
        elif suggestion['action'] == 'SURRENDER':
            text += "\n(altrimenti HIT)"
        elif suggestion['action'] == 'SPLIT':
            text += "\nDividi coppia"
            
        self.strategy_label.config(text=text)
        
    def new_hand(self):
        self.player_cards = []
        self.player_cards_split = []
        self.is_split_hand = False
        self.current_split_hand = 1
        self.dealer_card = None
        self.dealer_cards = []
        self.other_players_cards = []
        self.current_bet = 0
        
        # Nascondi UI split
        self.split_frame.pack_forget()
        self.player_split_total_label.pack_forget()
        self.switch_hand_btn.pack_forget()
        self.activate_split_btn.pack_forget()
        
        self.update_dealer_display()
        self.update_player_display()
        self.update_other_players_display()
        self.selection_mode.set('dealer')
        self.current_bet_label.config(text="Puntata: -", fg='#ffd700')
        self.strategy_label.config(text="Aspetto carte...")


def main():
    root = tk.Tk()
    app = BlackjackAssistant(root)
    root.mainloop()


if __name__ == "__main__":
    main()
