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
        window_height = 850
        
        # Centra la finestra
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#0f1419')
        
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
        
        # Tracciamento per undo
        self.last_operation = None  # {'type': 'dealer'|'player'|'player_split'|'table', 'card': 'A'}
        
        # Modalità selezione: 'dealer', 'player', 'table'
        self.selection_mode = tk.StringVar(value='dealer')
        
        self.setup_ui()
        
    def show_toast(self, message, duration=2000, bg_color='#2d5f2e'):
        """Mostra una notifica toast temporanea"""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)  # Rimuove bordi finestra
        
        # Posiziona in alto al centro
        toast_width = 350
        toast_height = 60
        x = (self.root.winfo_x() + self.root.winfo_width() // 2) - (toast_width // 2)
        y = self.root.winfo_y() + 50
        toast.geometry(f"{toast_width}x{toast_height}+{x}+{y}")
        
        # Stile
        toast.configure(bg=bg_color)
        label = tk.Label(
            toast,
            text=message,
            bg=bg_color,
            fg='#ffffff',
            font=("Arial", 11, "bold"),
            wraplength=330,
            justify='center'
        )
        label.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Chiudi automaticamente dopo duration millisecondi
        toast.after(duration, toast.destroy)
        
    def setup_ui(self):
        # Header moderno con gradiente
        header = tk.Frame(self.root, bg='#1a1f2e', height=45)
        header.pack(fill='x', padx=0, pady=0)
        
        # Linea decorativa superiore
        top_line = tk.Frame(header, bg='#ffd700', height=3)
        top_line.pack(fill='x')
        
        tk.Label(
            header, 
            text="♠️ BLACKJACK PRO ♣️", 
            font=("Segoe UI", 14, "bold"),
            bg='#1a1f2e',
            fg='#ffd700'
        ).pack(pady=5)
        
        # Container scrollabile
        canvas = tk.Canvas(self.root, bg='#0f1419', highlightthickness=0)
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
        
        setup_header = tk.Frame(scrollable_frame, bg='#1e2433', cursor='hand2', relief='flat', bd=0)
        setup_header.pack(fill='x', padx=5, pady=(5, 0))
        setup_header.bind('<Button-1>', lambda e: self.toggle_setup())
        
        tk.Label(
            setup_header,
            text="⚙️ SETUP",
            font=("Segoe UI", 12, "bold"),
            bg='#1e2433',
            fg='#a0aec0'
        ).pack(side='left', padx=10, pady=8)
        
        self.setup_arrow = tk.Label(
            setup_header,
            text="▼",
            font=("Segoe UI", 10),
            bg='#1e2433',
            fg='#a0aec0'
        )
        self.setup_arrow.pack(side='right', padx=10)
        
        # Setup content (collapsibile)
        self.setup_content = tk.Frame(scrollable_frame, bg='#1a1f2e')
        
        # Mazzi in riga singola
        deck_row = tk.Frame(self.setup_content, bg='#1a1f2e')
        deck_row.pack(fill='x', padx=10, pady=5)
        
        tk.Label(deck_row, text="Mazzi:", font=("Segoe UI", 9), bg='#1a1f2e', fg='#a0aec0').pack(side='left')
        self.deck_var = tk.StringVar(value="6")
        tk.Spinbox(deck_row, from_=1, to=8, textvariable=self.deck_var, width=3, font=("Segoe UI", 9)).pack(side='left', padx=5)
        tk.Button(deck_row, text="Set", command=self.set_decks, bg='#4299e1', fg='#fff', font=("Segoe UI", 8, "bold"), padx=8, pady=2, relief='flat').pack(side='left', padx=2)
        tk.Button(deck_row, text="Reset", command=self.reset_count, bg='#f56565', fg='#fff', font=("Segoe UI", 8, "bold"), padx=8, pady=2, relief='flat').pack(side='left', padx=2)
        
        # Bankroll in riga singola
        bank_row = tk.Frame(self.setup_content, bg='#1a1f2e')
        bank_row.pack(fill='x', padx=10, pady=5)
        
        tk.Label(bank_row, text="Bankroll €:", font=("Segoe UI", 9), bg='#1a1f2e', fg='#a0aec0').pack(side='left')
        self.bankroll_var = tk.StringVar(value="1000")
        tk.Entry(bank_row, textvariable=self.bankroll_var, width=6, font=("Segoe UI", 9)).pack(side='left', padx=5)
        
        tk.Label(bank_row, text="Min €:", font=("Segoe UI", 9), bg='#1a1f2e', fg='#a0aec0').pack(side='left', padx=(10, 0))
        self.min_bet_var = tk.StringVar(value="10")
        tk.Entry(bank_row, textvariable=self.min_bet_var, width=4, font=("Segoe UI", 9)).pack(side='left', padx=5)
        
        tk.Button(bank_row, text="Conferma", command=self.set_bankroll, bg='#48bb78', fg='#fff', font=("Segoe UI", 8, "bold"), padx=10, pady=2, relief='flat').pack(side='left', padx=5)
        
        # Conteggio in card moderna con bordi arrotondati
        count_card = tk.Frame(scrollable_frame, bg='#1e2433', relief='flat', bd=0)
        count_card.pack(fill='x', padx=5, pady=3)
        
        # Bordo superiore colorato
        tk.Frame(count_card, bg='#4ecdc4', height=3).pack(fill='x')
        
        tk.Label(count_card, text="📊 CONTEGGIO", font=("Segoe UI", 10, "bold"), bg='#1e2433', fg='#4ecdc4').pack(pady=(5, 3))
        
        # Container per layout a due colonne
        two_col_container = tk.Frame(count_card, bg='#1e2433')
        two_col_container.pack(fill='x', padx=5, pady=(0, 5))
        
        # Colonna sinistra: Griglia compatta 2x2 per contatori principali
        count_grid = tk.Frame(two_col_container, bg='#1e2433')
        count_grid.pack(side='left', padx=(5, 2))
        
        self.create_counter_display(count_grid, "Running", "0", 0, 0, '#4ecdc4')
        self.create_counter_display(count_grid, "True", "0.0", 0, 1, '#ff6b6b')
        self.create_counter_display(count_grid, "Carte", "312", 1, 0, '#95e1d3')
        self.create_counter_display(count_grid, "Viste", "0", 1, 1, '#9896f1')
        
        # Colonna destra: Bankroll info moderna
        bank_info = tk.Frame(two_col_container, bg='#252b3b', relief='flat', bd=0)
        bank_info.pack(side='left', fill='both', expand=True, padx=(2, 5))
        
        bank_row1 = tk.Frame(bank_info, bg='#252b3b')
        bank_row1.pack(fill='x', pady=2)
        
        tk.Label(bank_row1, text="💰", font=("Segoe UI", 12), bg='#252b3b').pack(side='left', padx=5)
        self.bankroll_label = tk.Label(bank_row1, text="1000€", font=("Segoe UI", 14, "bold"), bg='#252b3b', fg='#48bb78')
        self.bankroll_label.pack(side='left')
        
        self.profit_label = tk.Label(bank_row1, text="(+0€)", font=("Segoe UI", 11), bg='#252b3b', fg='#a0aec0')
        self.profit_label.pack(side='left', padx=5)
        
        bank_row2 = tk.Frame(bank_info, bg='#252b3b')
        bank_row2.pack(fill='x', pady=2)
        
        tk.Label(bank_row2, text="🎯", font=("Segoe UI", 10), bg='#252b3b').pack(side='left', padx=5)
        self.hands_label = tk.Label(bank_row2, text="0 mani", font=("Segoe UI", 9), bg='#252b3b', fg='#a0aec0')
        self.hands_label.pack(side='left')
        
        self.winrate_label = tk.Label(bank_row2, text="• 0% WR", font=("Segoe UI", 9), bg='#252b3b', fg='#a0aec0')
        self.winrate_label.pack(side='left', padx=10)
        
        # Puntata suggerita integrata
        bank_row3 = tk.Frame(bank_info, bg='#252b3b')
        bank_row3.pack(fill='x', pady=(5, 2))
        
        tk.Label(bank_row3, text="💎", font=("Segoe UI", 10), bg='#252b3b').pack(side='left', padx=5)
        self.bet_suggestion_label = tk.Label(
            bank_row3,
            text="Minimo tavolo - 10€",
            font=("Segoe UI", 10, "bold"),
            bg='#252b3b',
            fg='#f6ad55'
        )
        self.bet_suggestion_label.pack(side='left')
        
        # Selezione modalità e griglia carte in layout orizzontale
        cards_section = tk.Frame(scrollable_frame, bg='#1e2433')
        cards_section.pack(fill='x', padx=5, pady=3)
        
        # Bordo superiore colorato
        tk.Frame(cards_section, bg='#9896f1', height=3).pack(fill='x')
        
        tk.Label(cards_section, text="🃏 SELEZIONA CARTA", font=("Segoe UI", 10, "bold"), bg='#1e2433', fg='#9896f1').pack(pady=(5, 3))
        
        # Container per layout a due colonne (modalità + carte)
        cards_container = tk.Frame(cards_section, bg='#1e2433')
        cards_container.pack(fill='x', padx=5, pady=(0, 5))
        
        # Colonna sinistra: Modalità e Annulla
        mode_column = tk.Frame(cards_container, bg='#1e2433')
        mode_column.pack(side='left', padx=(0, 5))
        
        # Dealer button
        dealer_btn = tk.Radiobutton(
            mode_column, text="🂠\nBANCO", variable=self.selection_mode, value='dealer',
            font=("Segoe UI", 9, "bold"), bg='#c53030', fg='#fff', selectcolor='#9b2c2c',
            activebackground='#9b2c2c', activeforeground='#fff',
            indicatoron=0, width=7, padx=5, pady=8, justify='center',
            relief='flat', bd=0, highlightthickness=0
        )
        dealer_btn.pack(pady=2)
        
        # Player button
        player_btn = tk.Radiobutton(
            mode_column, text="🂡\nMIE", variable=self.selection_mode, value='player',
            font=("Segoe UI", 9, "bold"), bg='#2f855a', fg='#fff', selectcolor='#276749',
            activebackground='#276749', activeforeground='#fff',
            indicatoron=0, width=7, padx=5, pady=8, justify='center',
            relief='flat', bd=0, highlightthickness=0
        )
        player_btn.pack(pady=2)
        
        # Table button
        table_btn = tk.Radiobutton(
            mode_column, text="🎲\nTAVOLO", variable=self.selection_mode, value='table',
            font=("Segoe UI", 9, "bold"), bg='#d69e2e', fg='#fff', selectcolor='#b7791f',
            activebackground='#b7791f', activeforeground='#fff',
            indicatoron=0, width=7, padx=5, pady=8, justify='center',
            relief='flat', bd=0, highlightthickness=0
        )
        table_btn.pack(pady=2)
        
        # Bottone Annulla con stile coerente agli altri
        self.undo_btn = tk.Button(
            mode_column,
            text="↺\nANNULLA",
            command=self.undo_last_card,
            bg='#805ad5',
            fg='#ffffff',
            font=("Segoe UI", 9, "bold"),
            width=7,
            padx=5,
            pady=8,
            relief='flat',
            bd=0,
            state='disabled',
            disabledforeground='#cbd5e0',
            cursor='hand2',
            justify='center'
        )
        self.undo_btn.pack(pady=2)
        
        # Colonna destra: Griglia carte compatta e touch-friendly
        cards_grid = tk.Frame(cards_container, bg='#1e2433')
        cards_grid.pack(side='left', fill='x', expand=True)
        
        # Riga 1: A, 2-6
        row1 = tk.Frame(cards_grid, bg='#1e2433')
        row1.pack(pady=1)
        for card in ['A', '2', '3', '4', '5', '6']:
            self.create_card_button_mobile(row1, card)
        
        # Riga 2: 7-Q
        row2 = tk.Frame(cards_grid, bg='#1e2433')
        row2.pack(pady=1)
        for card in ['7', '8', '9', '10', 'J', 'Q']:
            self.create_card_button_mobile(row2, card)
        
        # Riga 3: K
        row3 = tk.Frame(cards_grid, bg='#1e2433')
        row3.pack(pady=1)
        self.create_card_button_mobile(row3, 'K')
        
        # Container per MANO e AZIONE affiancate
        game_info_container = tk.Frame(scrollable_frame, bg='#0f1419')
        game_info_container.pack(fill='x', padx=5, pady=3)
        
        # Colonna sinistra: Display mano corrente
        hand_card = tk.Frame(game_info_container, bg='#1e2433', relief='flat', bd=0, width=210)
        hand_card.pack(side='left', fill='both', expand=True, padx=(0, 2))
        
        # Bordo superiore colorato
        tk.Frame(hand_card, bg='#ff6b6b', height=3).pack(fill='x')
        
        tk.Label(hand_card, text="🎰 MANO", font=("Segoe UI", 9, "bold"), bg='#1e2433', fg='#ff6b6b').pack(pady=(3, 1))
        
        dealer_frame = tk.Frame(hand_card, bg='#252b3b', relief='flat', bd=0)
        dealer_frame.pack(fill='x', padx=5, pady=(1, 0))
        
        tk.Label(dealer_frame, text="Banco:", font=("Segoe UI", 8), bg='#252b3b', fg='#ff6b6b').pack(side='left', padx=3)
        self.dealer_display = tk.Label(dealer_frame, text="?", font=("Segoe UI", 10), bg='#252b3b', fg='#ff6b6b', wraplength=120)
        self.dealer_display.pack(side='left', padx=3, pady=1)
        
        self.dealer_total_label = tk.Label(hand_card, text="", font=("Segoe UI", 10, "bold"), bg='#1e2433', fg='#ff6b6b')
        self.dealer_total_label.pack(pady=0)
        
        player_frame = tk.Frame(hand_card, bg='#252b3b', relief='flat', bd=0)
        player_frame.pack(fill='x', padx=5, pady=(0, 1))
        
        tk.Label(player_frame, text="Mano 1:", font=("Segoe UI", 8), bg='#252b3b', fg='#4ecdc4').pack(side='left', padx=3)
        self.player_cards_label = tk.Label(player_frame, text="-", font=("Segoe UI", 10), bg='#252b3b', fg='#ffffff', wraplength=120)
        self.player_cards_label.pack(side='left', padx=3, pady=2)
        
        self.player_total_label = tk.Label(hand_card, text="Tot: -", font=("Segoe UI", 11, "bold"), bg='#1e2433', fg='#4ecdc4')
        self.player_total_label.pack(pady=2)
        
        # Frame per mano split (inizialmente nascosto)
        self.split_frame = tk.Frame(hand_card, bg='#252b3b', relief='flat', bd=0)
        
        tk.Label(self.split_frame, text="Mano 2:", font=("Segoe UI", 8), bg='#252b3b', fg='#95e1d3').pack(side='left', padx=3)
        self.player_cards_split_label = tk.Label(self.split_frame, text="-", font=("Segoe UI", 10), bg='#252b3b', fg='#ffffff', wraplength=120)
        self.player_cards_split_label.pack(side='left', padx=3, pady=2)
        
        self.player_split_total_label = tk.Label(hand_card, text="", font=("Segoe UI", 11, "bold"), bg='#1e2433', fg='#95e1d3')
        
        # Bottone per switchare mano attiva (nascosto inizialmente)
        self.switch_hand_btn = tk.Button(
            hand_card,
            text="🔀 Mano 2",
            command=self.switch_split_hand,
            bg='#4299e1',
            fg='#ffffff',
            font=("Segoe UI", 8, "bold"),
            padx=5,
            pady=2,
            relief='flat',
            bd=0,
            cursor='hand2'
        )
        
        # Bottone per attivare split
        self.activate_split_btn = tk.Button(
            hand_card,
            text="✂️ SPLIT",
            command=self.activate_split,
            bg='#805ad5',
            fg='#ffffff',
            font=("Segoe UI", 8, "bold"),
            padx=5,
            pady=2,
            relief='flat',
            bd=0,
            cursor='hand2'
        )
        
        self.other_players_label = tk.Label(hand_card, text="Tavolo: -", font=("Segoe UI", 7), bg='#1e2433', fg='#718096', wraplength=200)
        self.other_players_label.pack(pady=(1, 3))
        
        # Colonna destra: Strategia
        strategy_card = tk.Frame(game_info_container, bg='#1e2433', relief='flat', bd=0, width=210)
        strategy_card.pack(side='left', fill='both', expand=True, padx=(2, 0))
        
        # Bordo superiore colorato
        tk.Frame(strategy_card, bg='#48bb78', height=3).pack(fill='x')
        
        tk.Label(strategy_card, text="💡 AZIONE", font=("Segoe UI", 9, "bold"), bg='#1e2433', fg='#48bb78').pack(pady=(3, 2))
        
        self.strategy_label = tk.Label(
            strategy_card,
            text="Aspetto carte...",
            font=("Segoe UI", 11, "bold"),
            bg='#1e2433',
            fg='#ffffff',
            wraplength=190,
            justify='center'
        )
        self.strategy_label.pack(pady=(0, 5), padx=5, fill='both', expand=True)
        
        # Risultati in griglia compatta
        result_card = tk.Frame(scrollable_frame, bg='#1e2433')
        result_card.pack(fill='x', padx=5, pady=3)
        
        # Bordo superiore colorato
        tk.Frame(result_card, bg='#f6ad55', height=3).pack(fill='x')
        
        tk.Label(result_card, text="🎲 RISULTATO", font=("Segoe UI", 9, "bold"), bg='#1e2433', fg='#f6ad55').pack(pady=(3, 2))
        
        # Input puntata effettiva
        bet_input_frame = tk.Frame(result_card, bg='#1e2433')
        bet_input_frame.pack(pady=(0, 3))
        
        tk.Label(bet_input_frame, text="Puntata €:", font=("Segoe UI", 8), bg='#1e2433', fg='#a0aec0').pack(side='left', padx=(0, 3))
        self.actual_bet_var = tk.StringVar(value="10")
        self.actual_bet_entry = tk.Entry(
            bet_input_frame,
            textvariable=self.actual_bet_var,
            width=6,
            font=("Segoe UI", 9),
            justify='center'
        )
        self.actual_bet_entry.pack(side='left')
        
        res_grid1 = tk.Frame(result_card, bg='#1e2433')
        res_grid1.pack(pady=2)
        
        self.create_result_button(res_grid1, "✅", "win", '#2d5f2e', 0, 0)
        self.create_result_button(res_grid1, "❌", "loss", '#7d2e2e', 0, 1)
        self.create_result_button(res_grid1, "➖", "push", '#3a3a5f', 0, 2)
        self.create_result_button(res_grid1, "⭐", "blackjack", '#7d5f2e', 0, 3)
        
        res_grid2 = tk.Frame(result_card, bg='#1e2433')
        res_grid2.pack(pady=2)
        
        self.create_result_button(res_grid2, "2xW", "double_win", '#2d5f2e', 0, 0)
        self.create_result_button(res_grid2, "2xL", "double_loss", '#7d2e2e', 0, 1)
        self.create_result_button(res_grid2, "🏳️", "surrender", '#5f5a77', 0, 2)
        
        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Inizializza
        self.update_count_display()
    
    def create_counter_display(self, parent, label, value, row, col, color):
        """Crea un display moderno per contatori con gradiente simulato"""
        frame = tk.Frame(parent, bg='#1a1f2e', relief='flat', bd=0, width=90, height=48)
        frame.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
        frame.grid_propagate(False)
        
        # Bordo colorato superiore
        tk.Frame(frame, bg=color, height=2).pack(fill='x')
        
        tk.Label(frame, text=label, font=("Segoe UI", 7), bg='#1a1f2e', fg='#a0aec0').pack(pady=(2, 0))
        
        label_widget = tk.Label(frame, text=value, font=("Segoe UI", 13, "bold"), bg='#1a1f2e', fg=color)
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
        """Crea bottone carta ottimizzato per mobile con design moderno"""
        
        # Colori moderni basati sul valore
        if card in ['2', '3', '4', '5', '6']:
            color = '#38a169'  # Verde acceso
            hover_color = '#2f855a'
        elif card in ['7', '8', '9']:
            color = '#ecc94b'  # Giallo oro
            hover_color = '#d69e2e'
        else:
            color = '#e53e3e'  # Rosso acceso
            hover_color = '#c53030'
        
        btn = tk.Button(
            parent,
            text=card,
            command=lambda: self.card_clicked(card),
            bg=color,
            fg='#ffffff',
            font=("Segoe UI", 13, "bold"),
            width=4,
            height=1,
            relief='flat',
            bd=0,
            cursor='hand2',
            activebackground=hover_color,
            activeforeground='#ffffff'
        )
        btn.pack(side='left', padx=1, pady=1)
        
        # Effetto hover
        def on_enter(e):
            btn.config(bg=hover_color)
        
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def create_result_button(self, parent, text, result, color, row, col):
        """Crea bottone risultato con design moderno"""
        # Colori più vivaci e moderni
        color_map = {
            '#2d5f2e': '#38a169',  # Verde
            '#7d2e2e': '#e53e3e',  # Rosso
            '#3a3a5f': '#4a5568',  # Grigio
            '#7d5f2e': '#d69e2e',  # Oro
            '#5f5a77': '#805ad5'   # Viola
        }
        modern_color = color_map.get(color, color)
        
        btn = tk.Button(
            parent,
            text=text,
            command=lambda: self.record_result(result),
            bg=modern_color,
            fg='#ffffff',
            font=("Segoe UI", 10, "bold"),
            width=8,
            height=1,
            relief='flat',
            bd=0,
            cursor='hand2',
            padx=5,
            pady=8
        )
        btn.grid(row=row, column=col, padx=2, pady=1)
        
        # Hover effect
        original_color = modern_color
        def on_enter(e):
            # Colore più scuro per hover
            hover_colors = {
                '#38a169': '#2f855a',
                '#e53e3e': '#c53030',
                '#4a5568': '#2d3748',
                '#d69e2e': '#b7791f',
                '#805ad5': '#6b46c1'
            }
            btn.config(bg=hover_colors.get(original_color, original_color))
        
        def on_leave(e):
            btn.config(bg=original_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
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
        
        # Traccia operazione per undo
        self.last_operation = {'type': 'dealer', 'card': card}
        self.undo_btn.config(state='normal')
        
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
            # Traccia operazione per undo
            self.last_operation = {'type': 'player_split', 'card': card}
        else:
            self.player_cards.append(card)
            # Traccia operazione per undo
            self.last_operation = {'type': 'player', 'card': card}
        
        self.undo_btn.config(state='normal')
            
        self.card_counter.add_card(card)
        self.update_player_display()
        self.update_count_display()
        self.update_suggestion()
    
    def add_table_card_direct(self, card):
        """Aggiungi una carta vista al tavolo (non del giocatore)"""
        self.other_players_cards.append(card)
        
        # Traccia operazione per undo
        self.last_operation = {'type': 'table', 'card': card}
        self.undo_btn.config(state='normal')
        
        self.card_counter.add_card(card)
        self.update_count_display()
        self.update_other_players_display()
    
    def undo_last_card(self):
        """Annulla l'ultima carta inserita"""
        if not self.last_operation:
            return
        
        op_type = self.last_operation['type']
        card = self.last_operation['card']
        
        # Rimuovi carta dalla lista appropriata
        if op_type == 'dealer' and self.dealer_cards:
            self.dealer_cards.pop()
            if not self.dealer_cards:
                self.dealer_card = None
            self.update_dealer_display()
        elif op_type == 'player' and self.player_cards:
            self.player_cards.pop()
            self.update_player_display()
        elif op_type == 'player_split' and self.player_cards_split:
            self.player_cards_split.pop()
            self.update_player_display()
        elif op_type == 'table' and self.other_players_cards:
            self.other_players_cards.pop()
            self.update_other_players_display()
        
        # Sottrai carta dal conteggio
        self.card_counter.remove_card(card)
        self.update_count_display()
        self.update_suggestion()
        
        # Reset undo
        self.last_operation = None
        self.undo_btn.config(state='disabled')
    
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
        
        # Traccia operazione per undo
        self.last_operation = {'type': 'table', 'card': card}
        self.undo_btn.config(state='normal')
        
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
        self.show_toast(f"Impostati {decks} mazzi", bg_color='#2d5f7d')
    
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
            
            self.show_toast(
                f"Bankroll: {bankroll:.0f}€ | Min: {minimum:.0f}€ | Unit: {self.card_counter.betting_unit:.0f}€",
                duration=2500,
                bg_color='#2d5f7d'
            )
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori numerici validi")
        
    def reset_count(self):
        self.card_counter.reset()
        self.update_count_display()
        self.show_toast("Conteggio resettato", bg_color='#7d4e2e')
    
    def record_result(self, result):
        """Registra il risultato della mano"""
        # Usa la puntata inserita dall'utente
        try:
            actual_bet = float(self.actual_bet_var.get())
            if actual_bet <= 0:
                messagebox.showerror("Errore", "La puntata deve essere maggiore di 0")
                return
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un valore numerico valido per la puntata")
            return
        
        # Registra il risultato
        self.card_counter.record_hand_result(result, actual_bet)
        
        # Mostra messaggio di conferma
        result_messages = {
            'win': f"✅ Vittoria! +{actual_bet:.0f}€",
            'loss': f"❌ Sconfitta. -{actual_bet:.0f}€",
            'push': f"➖ Pareggio. Puntata restituita",
            'blackjack': f"⭐ BLACKJACK! +{actual_bet * 1.5:.0f}€",
            'double_win': f"💰 Raddoppio vinto! +{actual_bet * 2:.0f}€",
            'double_loss': f"💸 Raddoppio perso. -{actual_bet * 2:.0f}€",
            'surrender': f"🏳️ Arresa. -{actual_bet * 0.5:.0f}€"
        }
        
        # Colori in base al risultato
        result_colors = {
            'win': '#2d5f2e',
            'loss': '#7d2e2e',
            'push': '#3a3a5f',
            'blackjack': '#7d5f2e',
            'double_win': '#2d5f2e',
            'double_loss': '#7d2e2e',
            'surrender': '#5f5a77'
        }
        
        self.show_toast(
            result_messages.get(result, "Risultato registrato"),
            duration=2500,
            bg_color=result_colors.get(result, '#2d5f7d')
        )
        
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
            # Aggiorna il campo input con la puntata suggerita
            self.actual_bet_var.set(f"{self.current_bet:.0f}")
        
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
        self.last_operation = None
        
        # Aggiorna il campo puntata con la puntata suggerita per la nuova mano
        bet_info = self.card_counter.get_bet_multiplier()
        self.actual_bet_var.set(f"{bet_info['bet_amount']:.0f}")
        
        # Nascondi UI split
        self.split_frame.pack_forget()
        self.player_split_total_label.pack_forget()
        self.switch_hand_btn.pack_forget()
        self.activate_split_btn.pack_forget()
        
        # Disabilita bottone annulla
        self.undo_btn.config(state='disabled')
        
        self.update_dealer_display()
        self.update_player_display()
        self.update_other_players_display()
        self.selection_mode.set('dealer')
        self.strategy_label.config(text="Aspetto carte...")


def main():
    root = tk.Tk()
    app = BlackjackAssistant(root)
    root.mainloop()


if __name__ == "__main__":
    main()
